import os
import bcrypt
from dotenv import load_dotenv
from models import get_db, seed_words, seed_default_users

load_dotenv()

words = [
    "APPLE", "BRAVE", "CLOUD", "DREAM", "EAGLE", "FLAME", "GRAPE", "HONEY", "IVORY", 
    "JUMBO", "KNIFE", "LEMON", "MANGO", "NIGHT", "OASIS", "PEARL", "QUICK", "RIVER", 
    "STARS", "TIGER"
]

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

users = [
    {'username': 'Admin1', 'password': hash_password('Admin1$'), 'role': 'admin'},
    {'username': 'Player1', 'password': hash_password('Player1$'), 'role': 'player'}
]

if __name__ == '__main__':
    print("Connecting to database...")
    db = get_db()
    print("Seeding words...")
    seed_words(words)
    print(f"Seeded {len(words)} words.")
    print("Seeding users...")
    seed_default_users(users)
    print("Seeded default users.")
    print("Done!")
