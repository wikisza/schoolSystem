from flask_bcrypt import check_password_hash, generate_password_hash
from flask_login import LoginManager, login_user, UserMixin
import sqlite3
from models.user import User


login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    conn.close()

    if user:
        return User(user[0], user[1], user[2], user[3])  # Tworzysz obiekt User z wartościami z bazy danych
    return None

def authenticate(username, password):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    conn.close()
    
    if user and check_password_hash(user[2], password):
        user_obj = User(user[0], user[1], user[2], user[3])
        login_user(user_obj)
        return True
    return False

def register_user(username, password, profession):
    hashed_password = generate_password_hash(password).decode('utf-8')
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO users (username, password, profession) VALUES (?, ?, ?)', (username, hashed_password, profession))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()
