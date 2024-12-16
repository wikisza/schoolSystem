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

def search_items(search_query):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    # Jeśli pole wyszukiwania nie jest puste, wykonaj zapytanie SQL
    if search_query:
        search_query = f"%{search_query}%"
        query = '''
        SELECT classes.class_name, 
               COALESCE(users.firstName || ' ' || users.lastName, 'brak przypisanego wychowawcy'), 
               classes.id_class
        FROM classes
        LEFT JOIN teachers ON classes.id_teacher = teachers.id_teacher
        LEFT JOIN users ON teachers.id_user = users.id
        WHERE classes.class_name LIKE ?
        '''
        cursor.execute(query, (search_query,))
    else:
        # Jeśli pole jest puste, zwróć wszystkie propozycje
        query = '''
        SELECT classes.class_name, 
               COALESCE(users.firstName || ' ' || users.lastName, 'brak przypisanego wychowawcy')
        FROM classes
        LEFT JOIN teachers ON classes.id_teacher = teachers.id_teacher
        LEFT JOIN users ON teachers.id_user = users.id
        '''
        cursor.execute(query)
    
    items = cursor.fetchall()
    conn.close()
    
    # Zwróć wyniki jako JSON
    return jsonify(items)

def getClassData(id_class):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    try:
        query = '''
        SELECT classes.class_name, 
               COALESCE(users.firstName || ' ' || users.lastName, 'brak przypisanego wychowawcy')
        FROM classes 
        JOIN teachers ON classes.id_teacher = teachers.id_teacher
        JOIN users ON teachers.id_user = users.id
        WHERE id_class = ?
        '''
        cursor.execute(query, (id_class,))
        class_data = cursor.fetchone()  # Pobranie danych (krotka)
        return class_data
    except Exception as e:
        print(f"Błąd podczas pobierania danych klasy: {e}")
        return None
    finally:
        conn.close()


def getStudentsInClass(id_class):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    try:
        query = '''
        SELECT users.firstName||' '||users.lastName 
        FROM students 
        JOIN users ON students.id_user = users.id
        WHERE id_class = ?
        '''
        cursor.execute(query, (id_class,))
        students = cursor.fetchall()  
        return [student[0] for student in students]
    except Exception as e:
        print(f"Błąd podczas pobierania uczniów: {e}")
        return []
    finally:
        conn.close()

def getUnassignedStudents():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    try:
        query = '''
        SELECT users.id, users.firstName || ' ' || users.lastName 
        FROM users
        JOIN students ON students.id_user = users.id
        WHERE students.id_class = 0
        '''
        cursor.execute(query)
        students = cursor.fetchall()  # Zwraca listę krotek (id, imię i nazwisko)
        return [{'id': student[0], 'name': student[1]} for student in students]  # Zwracamy listę słowników
    except Exception as e:
        print(f"Błąd podczas pobierania uczniów: {e}")
        return []
    finally:
        conn.close()

def assign_students_to_class(data, student_ids, class_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    try:
        for student_id in student_ids:
            cursor.execute('UPDATE students SET id_class = ? WHERE id_user = ?', (class_id, student_id))
        conn.commit()
        return jsonify({"success": True}), 200
    except Exception as e:
        print(f"Błąd podczas przypisywania uczniów: {e}")
        return jsonify({"success": False}), 500
    finally:
        conn.close()


def editThisClass(id_class, id_teacher, class_name):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    try:
        cursor.execute('UPDATE classes SET id_teacher = ?, class_name = ? WHERE id_class = ? ', (id_teacher,class_name, id_class,))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()