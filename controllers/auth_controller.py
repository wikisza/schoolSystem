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
        return User(user[0], user[1], user[2], user[3], user[4], user[5], user[6], user[7], user[8])  # Tworzysz obiekt User z wartościami z bazy danych
    return None

def authenticate(username, password):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    conn.close()
    
    if user and check_password_hash(user[2], password):
        user_obj = User(user[0], user[1], user[2], user[3], user[4], user[5], user[6], user[7], user[8])
        login_user(user_obj)
        return True
    return False

def register_user( username, password, profession,email, firstName, lastName,  phoneNumber, address):
    hashed_password = generate_password_hash(password).decode('utf-8')
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO users (username, password, profession, email, firstName, lastName, phoneNumber, address) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', (username, hashed_password, profession, email, firstName, lastName, phoneNumber, address))
        
        user_id = cursor.lastrowid

        if profession == 'uczen':
            cursor.execute('INSERT INTO students (id_user, id_parent, PESEL, id_class) VALUES (?, ?, ?, ?)', (user_id, 0, '0', 0))

        elif profession == 'rodzic':
            cursor.execute('INSERT INTO parents (id_user) VALUES (?)', (user_id,))

        elif profession == 'nauczyciel':
            cursor.execute('INSERT INTO teachers (id_user) VALUES (?)', (user_id,))

        elif profession == 'administracja':
            cursor.execute('INSERT INTO admins (id_user) VALUES (?)', (user_id,))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()



#kontrolery do listy użytkowników

def getUsersData(selectId):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    query = '''
    SELECT users.firstName || ' ' || users.lastName AS fullName, 
           users.phoneNumber, users.address, users.email
    FROM users
    WHERE users.profession = ?
    '''
    cursor.execute(query, (selectId,))
    users_data = cursor.fetchall()  # Zmieniamy na fetchall(), aby zwrócić wiele rekordów
    conn.close()

    result = [
        {
            "fullName": row[0],
            "phoneNumber": row[1],
            "address": row[2],
            "email": row[3]
        }
        for row in users_data
    ]

    return result
