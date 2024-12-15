import sqlite3
from flask import Blueprint, render_template, jsonify, request

def addClass(className):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO subjects (subject_name) VALUES (?)', (className,))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

        
def addGroup(className):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO classes (id_teacher, class_name) VALUES (?, ?)', (0, className,))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def search_items():
    search_query = request.args.get('query')  # Pobranie zapytania z wyszukiwarki
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    # Jeśli pole wyszukiwania nie jest puste, wykonaj zapytanie SQL
    if search_query:
        search_query = f"%{search_query}%"
        query = '''
        SELECT classes.class_name, users.firstName 
        FROM classes
        JOIN teachers ON classes.id_teacher = teachers.id_teacher
        JOIN users ON teachers.id_user = users.id
        WHERE classes.class_name LIKE ?
        '''
        cursor.execute(query, (search_query,))
    else:
        # Jeśli pole jest puste, zwróć wszystkie propozycje
        query = '''
        SELECT classes.class_name, users.firstName 
        FROM classes
        JOIN teachers ON classes.id_teacher = teachers.id_teacher
        JOIN users ON teachers.id_user = users.id
        '''
        cursor.execute(query)
    items = cursor.fetchall()
    conn.close()
    # Zwróć wyniki jako JSON
    return jsonify(items)