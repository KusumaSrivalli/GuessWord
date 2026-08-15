import os
import sys

# Ensure sibling modules in api/ are importable
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from datetime import datetime, timezone
import bcrypt
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import (
    JWTManager, create_access_token,
    jwt_required, get_jwt_identity, get_jwt
)

from word_validation import is_valid_word
from word_hints import get_word_hint

from models import (
    get_db, create_user, find_user_by_username, get_random_word,
    create_session, get_session, update_session,
    get_sessions_for_user_on_date, get_all_sessions
)

app = Flask(__name__)
CORS(app)

app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'default-secret-key')
jwt = JWTManager(app)


# ── Helpers ──────────────────────────────────────────────

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

def get_feedback(guess, target):
    feedback = ['grey'] * 5
    target_letters = list(target)
    guess_letters = list(guess)

    for i in range(5):
        if guess_letters[i] == target_letters[i]:
            feedback[i] = 'green'
            target_letters[i] = None
            guess_letters[i] = None

    for i in range(5):
        if guess_letters[i] is not None and guess_letters[i] in target_letters:
            idx = target_letters.index(guess_letters[i])
            feedback[i] = 'orange'
            target_letters[idx] = None

    return feedback


# ── Auth Endpoints ───────────────────────────────────────

@app.route('/api/auth/register', methods=['POST'])
def register():
    try:
        data = request.json or {}
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
    except Exception as e:
        return jsonify({'error': f'Database error: {str(e)}'}), 500


@app.route('/api/auth/login', methods=['POST'])
def login():
    try:
        data = request.json or {}
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
    except Exception as e:
        return jsonify({'error': f'Database error: {str(e)}'}), 500



# ── Game Endpoints ───────────────────────────────────────

@app.route('/api/game/start', methods=['POST'])
@jwt_required()
def start_game():
    username = get_jwt_identity()
    data = request.json or {}
    mode = data.get('mode', 'easy').lower()
    if mode not in ['easy', 'medium', 'hard']:
        mode = 'easy'

    date_str = datetime.now(timezone.utc).strftime('%Y-%m-%d')
    sessions_today = get_sessions_for_user_on_date(username, date_str)

    if len(sessions_today) >= 3:
        return jsonify({'error': 'Daily limit reached'}), 403

    target_word = get_random_word(mode)
    if not target_word:
        return jsonify({'error': 'No words available in database'}), 500

    hint = get_word_hint(target_word)
    user = find_user_by_username(username)
    session_id = create_session(user['_id'], username, target_word, date_str, mode=mode)

    time_limit = 300 if mode == 'medium' else 180 if mode == 'hard' else None

    return jsonify({
        'session_id': str(session_id),
        'mode': mode,
        'time_limit': time_limit,
        'hint': hint,
        'message': f'Game started in {mode.upper()} mode'
    }), 200


@app.route('/api/game/guess', methods=['POST'])
@jwt_required()
def make_guess():
    username = get_jwt_identity()

    data = request.json
    session_id = data.get('session_id')
    guess = data.get('guess', '').upper()

    if not session_id or len(guess) != 5 or not guess.isalpha():
        return jsonify({'error': 'Invalid guess or session_id'}), 400

    if not is_valid_word(guess):
        return jsonify({'error': 'Not in word list'}), 400

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

@app.route('/api/game/user-stats', methods=['GET'])
@jwt_required()
def get_user_stats():
    from datetime import timedelta
    current_user = get_jwt_identity()
    claims = get_jwt()

    target_user = request.args.get('target_user')
    if target_user and claims.get('role') == 'admin':
        username = target_user
    else:
        username = current_user

    db = get_db()
    sessions = list(db.sessions.find({'username': username}))

    total_games = len(sessions)
    total_wins = sum(1 for s in sessions if s.get('outcome') == 'won')
    win_rate = round((total_wins / total_games * 100), 1) if total_games > 0 else 0.0

    date_str_today = datetime.now(timezone.utc).strftime('%Y-%m-%d')

    sessions_today_map = {}
    for s in sessions:
        s_date = s.get('date')
        c_date = s['created_at'].strftime('%Y-%m-%d') if s.get('created_at') else None
        if s_date == date_str_today or c_date == date_str_today:
            sessions_today_map[str(s['_id'])] = s

    games_left_today = max(0, 3 - len(sessions_today_map))

    heatmap = []
    today_dt = datetime.now(timezone.utc)
    for i in range(29, -1, -1):
        day_dt = today_dt - timedelta(days=i)
        d_str = day_dt.strftime('%Y-%m-%d')
        label = day_dt.strftime('%b %d')

        day_games_map = {}
        for s in sessions:
            s_d = s.get('date')
            c_d = s['created_at'].strftime('%Y-%m-%d') if s.get('created_at') else None
            if s_d == d_str or c_d == d_str:
                day_games_map[str(s['_id'])] = s

        heatmap.append({'date': d_str, 'label': label, 'count': len(day_games_map)})

    current_streak = 0
    for i in range(30):
        d_str = (today_dt - timedelta(days=i)).strftime('%Y-%m-%d')
        day_games = sum(1 for s in sessions if s.get('date') == d_str or (s.get('created_at') and s['created_at'].strftime('%Y-%m-%d') == d_str))
        if day_games > 0:
            current_streak += 1
        else:
            if i == 0:
                continue
            break

    return jsonify({
        'username': username,
        'total_games': total_games,
        'total_wins': total_wins,
        'win_rate': f"{win_rate:.1f}%",
        'current_streak': current_streak,
        'games_left_today': games_left_today,
        'games_played_today': len(sessions_today_map),
        'heatmap': heatmap
    }), 200

@app.route('/api/admin/overview', methods=['GET'])
@jwt_required()
def admin_overview():
    claims = get_jwt()
    if claims.get('role') != 'admin':
        return jsonify({'error': 'Admin only'}), 403

    db = get_db()
    users = list(db.users.find({'role': 'player'}))
    sessions = list(db.sessions.find())

    total_users = len(users)
    total_games = len(sessions)
    total_wins = sum(1 for s in sessions if s.get('outcome') == 'won')

    daily_map = {}
    for s in sessions:
        d = s.get('date', 'Unknown')
        u = s.get('username', 'Unknown')
        if d not in daily_map:
            daily_map[d] = {}
        if u not in daily_map[d]:
            daily_map[d][u] = {'games_played': 0, 'games_won': 0}

        daily_map[d][u]['games_played'] += 1
        if s.get('outcome') == 'won':
            daily_map[d][u]['games_won'] += 1

    daily_report = []
    for d in sorted(daily_map.keys(), reverse=True):
        user_list = []
        for u, counts in daily_map[d].items():
            user_list.append({
                'username': u,
                'games_played': counts['games_played'],
                'games_won': counts['games_won']
            })
        daily_report.append({
            'date': d,
            'users_activity': user_list
        })

    user_names = [u['username'] for u in users]

    return jsonify({
        'total_users': total_users,
        'total_games': total_games,
        'total_wins': total_wins,
        'user_names': user_names,
        'daily_report': daily_report
    }), 200


# ── Report Endpoints ─────────────────────────────────────

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


# ── Local dev only ───────────────────────────────────────
if __name__ == '__main__':
    app.run(port=5000, debug=True)
