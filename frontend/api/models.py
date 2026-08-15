import os
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime

try:
    import certifi
    HAS_CERTIFI = True
except ImportError:
    HAS_CERTIFI = False

_client = None
_db = None

def get_db():
    global _client, _db
    if _db is None:
        mongo_uri = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/guessword')
        if 'mongodb.net' in mongo_uri or 'mongodb+srv' in mongo_uri:
            kwargs = {
                'serverSelectionTimeoutMS': 7000,
                'tls': True,
                'tlsAllowInvalidCertificates': True
            }
            if HAS_CERTIFI:
                kwargs['tlsCAFile'] = certifi.where()
            _client = MongoClient(mongo_uri, **kwargs)
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

EASY_WORDS = [
    "APPLE", "BEACH", "BRAVE", "CLOUD", "DREAM", "FLAME", "GRAPE", "HONEY", "HOUSE", "LEMON",
    "MANGO", "PEARL", "PLANT", "RIVER", "STARS", "TIGER", "WATER", "WOMAN", "WORLD", "MUSIC",
    "CHAIR", "SWEET", "HEART", "LIGHT", "SMILE", "TRAIN", "GREEN", "PAPER", "BREAD", "NIGHT"
]

MEDIUM_WORDS = [
    "ABYSS", "BRISK", "CHASM", "FROST", "GLYPH", "IVORY", "LURID", "PRISM", "QUIRK", "VALOR",
    "VORTEX", "ZEPHYR", "AMBER", "BRINE", "CIRCA", "DRUID", "EMBER", "GUILD", "ORBIT", "PIXEL",
    "QUOTA", "RADAR", "SOLAR", "TEXAS", "VOCAL", "YACHT", "VAGUE", "SHREW", "SQUID", "TWIST"
]

HARD_WORDS = [
    "ABACK", "ACRID", "BOSON", "CYNIC", "EPOCH", "FJORD", "GAUNT", "HYDRA", "KAPUT", "NYMPH",
    "QUAFF", "TRYST", "ZESTY", "AEGIS", "COYLY", "GAFFE", "HAZEL", "IONIC", "JAZZY", "KAZOO",
    "MYTHS", "ONYX", "PUPAL", "QUART", "RERUN", "SYNOD", "UMBRA", "VIXEN", "WALTZ", "ZINCS"
]

def get_random_word(mode='easy'):
    db = get_db()
    cursor = db.words.aggregate([
        { '$match': { 'mode': mode } },
        { '$sample': { 'size': 1 } }
    ])
    words = list(cursor)
    if words:
        return words[0]['word']
        
    import random
    if mode == 'medium':
        return random.choice(MEDIUM_WORDS)
    elif mode == 'hard':
        return random.choice(HARD_WORDS)
    else:
        return random.choice(EASY_WORDS)

def create_session(user_id, username, target_word, date, mode='easy'):
    db = get_db()
    session = {
        'user_id': user_id,
        'username': username,
        'date': date,
        'target_word': target_word,
        'mode': mode,
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
