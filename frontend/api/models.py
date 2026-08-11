import os
import certifi
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime

_client = None
_db = None

def get_db():
    global _client, _db
    if _db is None:
        mongo_uri = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/guessword')
        if 'mongodb.net' in mongo_uri or 'mongodb+srv' in mongo_uri:
            _client = MongoClient(
                mongo_uri,
                serverSelectionTimeoutMS=5000,
                tlsCAFile=certifi.where()
            )
        else:
            _client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)

        try:
            _db = _client.get_default_database()
        except Exception:
            _db = _client['guessword']
    return _db

def create_user(username, password_hash, role):
    db = get_db()
    user = {
        'username': username,
        'password': password_hash,
        'role': role
    }
    result = db.users.insert_one(user)
    return result.inserted_id

def find_user_by_username(username):
    db = get_db()
    return db.users.find_one({'username': {'$regex': f'^{username}$', '$options': 'i'}})

def get_all_users():
    db = get_db()
    return list(db.users.find())

def get_random_word():
    db = get_db()
    cursor = db.words.aggregate([{ '$sample': { 'size': 1 } }])
    words = list(cursor)
    if words:
        return words[0]['word']
    
    # Auto-seed 20 words if words collection is empty
    default_words = [
        "APPLE", "BRAVE", "CLOUD", "DREAM", "EAGLE", "FLAME", "GRAPE", "HONEY", "IVORY", 
        "JUMBO", "KNIFE", "LEMON", "MANGO", "NIGHT", "OASIS", "PEARL", "QUICK", "RIVER", 
        "STARS", "TIGER"
    ]
    db.words.insert_many([{'word': w} for w in default_words])
    return "APPLE"

def create_session(user_id, username, target_word, date):
    db = get_db()
    session = {
        'user_id': user_id,
        'username': username,
        'date': date,
        'target_word': target_word,
        'guesses': [],
        'outcome': None,
        'created_at': datetime.utcnow(),
        'completed_at': None
    }
    result = db.sessions.insert_one(session)
    return result.inserted_id

def get_session(session_id):
    db = get_db()
    return db.sessions.find_one({'_id': ObjectId(session_id)})

def update_session(session_id, update):
    db = get_db()
    db.sessions.update_one({'_id': ObjectId(session_id)}, {'$set': update})

def get_sessions_for_user_on_date(username, date):
    db = get_db()
    return list(db.sessions.find({'username': username, 'date': date}))

def get_all_sessions():
    db = get_db()
    return list(db.sessions.find())

def seed_words(words_list):
    db = get_db()
    db.words.delete_many({})
    db.words.insert_many([{'word': w} for w in words_list])

def seed_default_users(users_list):
    db = get_db()
    for u in users_list:
        if not find_user_by_username(u['username']):
            db.users.insert_one(u)
