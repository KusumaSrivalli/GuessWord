import os
import re
from datetime import datetime, timezone
import bcrypt
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt
from bson import ObjectId

from models import (
    create_user, find_user_by_username, get_all_users, get_random_word,
    create_session, get_session, update_session, get_sessions_for_user_on_date,
    get_all_sessions
)

load_dotenv()

app = Flask(__name__)
CORS(app)

app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'default-secret-key')
jwt = JWTManager(app)

def serialize_doc(doc):
    if doc and '_id' in doc:
        doc['_id'] = str(doc['_id'])
    if doc and 'user_id' in doc:
        doc['user_id'] = str(doc['user_id'])
    return doc

def check_username(username):
    if len(username) < 5:
        return False
    if not username.isalpha():
        return False
    if not any(c.isupper() for c in username) or not any(c.islower() for c in username):
        return False
    return True

def check_password(password):
    if len(password) < 5:
        return False
    if not any(c.isalpha() for c in password):
        return False
    if not any(c.isdigit() for c in password):
        return False
    if not any(c in '$%*&' for c in password):
        return False
    return True

@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username', '')
    password = data.get('password', '')
    role = data.get('role', 'player')

    if role not in ['admin', 'player']:
        return jsonify({'error': 'Invalid role'}), 400

    if not check_username(username):
        return jsonify({'error': 'Username must be at least 5 letters and include both upper and lower case characters.'}), 400

    if not check_password(password):
        return jsonify({'error': 'Password must be at least 5 characters with letters, numbers, and one of $ % * &.'}), 400

    if find_user_by_username(username):
        return jsonify({'error': 'Username already exists'}), 400

    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    create_user(username, hashed_pw, role)

    return jsonify({'message': 'User registered successfully', 'user': {'username': username, 'role': role}}), 201

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username', '')
    password = data.get('password', '')

    user = find_user_by_username(username)
    if not user:
        return jsonify({'error': 'Invalid credentials'}), 401

    if not bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
        return jsonify({'error': 'Invalid credentials'}), 401

    token = create_access_token(
        identity=user['username'],
        additional_claims={'role': user['role']}
    )

    return jsonify({'token': token, 'user': {'username': user['username'], 'role': user['role']}}), 200

@app.route('/api/game/start', methods=['POST'])
@jwt_required()
def start_game():
    username = get_jwt_identity()
    
    date_str = datetime.now(timezone.utc).strftime('%Y-%m-%d')
    sessions_today = get_sessions_for_user_on_date(username, date_str)
    
    if len(sessions_today) >= 3:
        return jsonify({'error': 'Daily limit reached'}), 403
        
    target_word = get_random_word()
    if not target_word:
        return jsonify({'error': 'No words available in database'}), 500
        
    user = find_user_by_username(username)
    session_id = create_session(user['_id'], username, target_word, date_str)
    
    return jsonify({'session_id': str(session_id), 'message': 'Game started'}), 200

def get_feedback(guess, target):
    feedback = ['grey'] * 5
    target_letters = list(target)
    guess_letters = list(guess)
    
    # First pass: GREEN
    for i in range(5):
        if guess_letters[i] == target_letters[i]:
            feedback[i] = 'green'
            target_letters[i] = None
            guess_letters[i] = None
            
    # Second pass: ORANGE
    for i in range(5):
        if guess_letters[i] is not None:
            if guess_letters[i] in target_letters:
                idx = target_letters.index(guess_letters[i])
                feedback[i] = 'orange'
                target_letters[idx] = None
                
    return feedback

@app.route('/api/game/guess', methods=['POST'])
@jwt_required()
def make_guess():
    username = get_jwt_identity()
    
    data = request.json
    session_id = data.get('session_id')
    guess = data.get('guess', '').upper()
    
    if not session_id or len(guess) != 5 or not guess.isalpha():
        return jsonify({'error': 'Invalid guess or session_id'}), 400
        
    session = get_session(session_id)
    if not session:
        return jsonify({'error': 'Session not found'}), 404
        
    if session['username'] != username:
        return jsonify({'error': 'Unauthorized'}), 403
        
    if session['outcome'] is not None:
        return jsonify({'error': 'Game already finished'}), 400
        
    target_word = session['target_word']
    feedback = get_feedback(guess, target_word)
    
    guess_entry = {'guess': guess, 'feedback': feedback}
    new_guesses = session['guesses'] + [guess_entry]
    
    outcome = None
    if guess == target_word:
        outcome = 'won'
    elif len(new_guesses) >= 5:
        outcome = 'lost'
        
    update = {'guesses': new_guesses, 'outcome': outcome}
    if outcome:
        update['completed_at'] = datetime.now(timezone.utc)
        
    update_session(session_id, update)
    
    status = 'playing' if not outcome else outcome
    
    resp = {
        'feedback': feedback,
        'guesses': new_guesses,
        'status': status,
        'message': 'Guess processed'
    }
    if outcome:
        resp['target_word'] = target_word
        
    return jsonify(resp), 200

@app.route('/api/reports/daily', methods=['GET'])
@jwt_required()
def report_daily():
    claims = get_jwt()
    if claims.get('role') != 'admin':
        return jsonify({'error': 'Admin only'}), 403
        
    sessions = get_all_sessions()
    
    reports = {}
    for s in sessions:
        d = s['date']
        if d not in reports:
            reports[d] = {'num_users': set(), 'correct_guesses': 0}
        
        reports[d]['num_users'].add(s['username'])
        if s.get('outcome') == 'won':
            reports[d]['correct_guesses'] += 1
        
    result = []
    for d in sorted(reports.keys()):
        result.append({
            'date': d,
            'num_users': len(reports[d]['num_users']),
            'correct_guesses': reports[d]['correct_guesses']
        })
        
    return jsonify({'report': result}), 200

@app.route('/api/reports/user', methods=['GET'])
@jwt_required()
def report_user():
    claims = get_jwt()
    if claims.get('role') != 'admin':
        return jsonify({'error': 'Admin only'}), 403
        
    sessions = get_all_sessions()
    
    user_reports = {}
    for s in sessions:
        u = s['username']
        d = s['date']
        
        if u not in user_reports:
            user_reports[u] = {}
        if d not in user_reports[u]:
            user_reports[u][d] = {'words_tried': 0, 'correct_guesses': 0}
            
        user_reports[u][d]['words_tried'] += 1
        if s.get('outcome') == 'won':
            user_reports[u][d]['correct_guesses'] += 1
        
    result = []
    for u, dates in user_reports.items():
        rows = []
        for d in sorted(dates.keys()):
            rows.append({
                'date': d,
                'words_tried': dates[d]['words_tried'],
                'correct_guesses': dates[d]['correct_guesses']
            })
        result.append({
            'username': u,
            'rows': rows
        })
        
    return jsonify({'report': result}), 200

if __name__ == '__main__':
    app.run(port=5000, debug=True)
