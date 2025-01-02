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
        cursor.execute('INSERT INTO classes (id_teacher,class_name) VALUES (?,?)', (0,className,))
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
    query = '''
    SELECT classes.class_name,
           classes.id_teacher,
           CASE
               WHEN users.firstName IS NOT NULL THEN users.firstName || ' ' || users.lastName
               ELSE 'Brak przypisanego wychowawcy'
           END AS teacher_name,
           classes.id_class
    FROM classes
    LEFT JOIN teachers ON classes.id_teacher = teachers.id_teacher
    LEFT JOIN users ON teachers.id_user = users.id
    WHERE classes.id_class = ?
    '''
    cursor.execute(query, (id_class,))
    class_data = cursor.fetchone()
    conn.close()
    return class_data



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

def get_teachers():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    query = '''
    SELECT teachers.id_teacher, users.firstName || ' ' || users.lastName AS name
    FROM teachers
    JOIN users ON teachers.id_user = users.id
    WHERE teachers.id_teacher != 0
    '''
    cursor.execute(query)
    teachers = cursor.fetchall()
    conn.close()

    return [{'id': teacher[0], 'name': teacher[1]} for teacher in teachers]


def editThisClass(id_class, id_teacher, class_name):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    try:
        cursor.execute('UPDATE classes SET id_teacher = ?, class_name = ? WHERE id_class = ? ', (id_teacher,class_name, id_class,))
        conn.commit()
        return jsonify({"success": True}), 200
    except Exception as e:
        print(f"Błąd podczas przypisywania uczniów: {e}")
        return jsonify({"success": False}), 500
    finally:
        conn.close()

def getTeachersList():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # Pobieranie nauczycieli z filtrem `id_teacher != 0`
    query = '''
    SELECT teachers.id_teacher, users.firstName || ' ' || users.lastName AS name
    FROM teachers
    JOIN users ON teachers.id_user = users.id
    WHERE teachers.id_teacher != 0
    '''
    cursor.execute(query)
    teachers = cursor.fetchall()
    conn.close()
    
    # Konwersja wyników do listy słowników dla lepszej obsługi w JSON
    teachers_list = [{'id': t[0], 'name': t[1]} for t in teachers]
    return jsonify(teachers_list)



#### POBIERANIE LEKCJI Z BAZY DANYCH

def get_lessons(class_id):
    if not class_id:
        return jsonify([])  # Brak danych, jeśli `classId` nie jest przesłane

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    query = '''
    SELECT 
        lessons.subject,
        lessons.start_time,
        lessons.end_time,
        lessons.room,
        teachers.first_name || ' ' || teachers.last_name AS teacher_name
    FROM lessons
    JOIN teachers ON lessons.teacher_id = teachers.id
    WHERE lessons.class_id = ?
    '''
    cursor.execute(query, (class_id,))
    lessons = cursor.fetchall()
    conn.close()

    # Przekształcenie wyników w listę obiektów JSON
    result = [
        {
            'title': lesson[0],
            'start': lesson[1],
            'end': lesson[2],
            'room': lesson[3],
            'teacher': lesson[4],
            'description': f'Lekcja w sali {lesson[3]}'
        }
        for lesson in lessons
    ]
    return jsonify(result)


#wszystkie klasy

def getAllClasses():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    query = '''SELECT id_class, class_name FROM classes ORDER BY class_name'''
    cursor.execute(query)
    classes = cursor.fetchall()
    conn.close()

    result = [
        {
            "id_class": row[0],
            "class_name": row[1]
        }
        for row in classes
    ]

    return jsonify(result)

