import os
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime

client = None
db = None

def get_db():
    global client, db
    if db is None:
        mongo_uri = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/guessword')
        client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
        try:
            db = client.get_default_database()
        except Exception:
            db = client['guessword']
    return db

def create_user(username, password_hash, role):
    _db = get_db()
    user = {
        'username': username,
        'password': password_hash,
        'role': role
    }
    result = _db.users.insert_one(user)
    return result.inserted_id

def find_user_by_username(username):
    _db = get_db()
    return _db.users.find_one({'username': {'$regex': f'^{username}$', '$options': 'i'}})

def get_all_users():
    _db = get_db()
    return list(_db.users.find())

def get_random_word():
    _db = get_db()
    cursor = _db.words.aggregate([{ '$sample': { 'size': 1 } }])
    words = list(cursor)
    if words:
        return words[0]['word']
        
    default_words = [
        "APPLE", "BRAVE", "CLOUD", "DREAM", "EAGLE", "FLAME", "GRAPE", "HONEY", "IVORY", 
        "JUMBO", "KNIFE", "LEMON", "MANGO", "NIGHT", "OASIS", "PEARL", "QUICK", "RIVER", 
        "STARS", "TIGER"
    ]
    _db.words.insert_many([{'word': w} for w in default_words])
    return "APPLE"

def create_session(user_id, username, target_word, date):
    _db = get_db()
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
    result = _db.sessions.insert_one(session)
    return result.inserted_id

def get_session(session_id):
    _db = get_db()
    return _db.sessions.find_one({'_id': ObjectId(session_id)})

def update_session(session_id, update):
    _db = get_db()
    _db.sessions.update_one({'_id': ObjectId(session_id)}, {'$set': update})

def get_sessions_for_user_on_date(username, date):
    _db = get_db()
    return list(_db.sessions.find({'username': username, 'date': date}))

def get_all_sessions():
    _db = get_db()
    return list(_db.sessions.find())

def seed_words(words_list):
    _db = get_db()
    _db.words.delete_many({})
    _db.words.insert_many([{'word': w} for w in words_list])

def seed_default_users(users_list):
    _db = get_db()
    for u in users_list:
        if not find_user_by_username(u['username']):
            _db.users.insert_one(u)
