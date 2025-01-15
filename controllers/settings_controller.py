import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

def update_user_data(user_id, firstName, lastName, email, phoneNumber, address, password, confirmPassword):
    """
    Funkcja do aktualizacji danych użytkownika w bazie danych.
    """
    if password and password != confirmPassword:
        return False  # Hasła się nie zgadzają

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Sprawdzenie, czy zmienia się hasło
    if password:
        hashed_password = generate_password_hash(password)
        query = '''
        UPDATE users
        SET firstName = ?, lastName = ?, email = ?, phoneNumber = ?, address = ?, password = ?
        WHERE id = ?
        '''
        cursor.execute(query, (firstName, lastName, email, phoneNumber, address, hashed_password, user_id))
    else:
        query = '''
        UPDATE users
        SET firstName = ?, lastName = ?, email = ?, phoneNumber = ?, address = ?
        WHERE id = ?
        '''
        cursor.execute(query, (firstName, lastName, email, phoneNumber, address, user_id))

    conn.commit()
    conn.close()

    # Jeśli wszystko się udało, zwróć True
    return True
