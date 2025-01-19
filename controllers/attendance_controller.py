
import sqlite3
from datetime import datetime


from flask import jsonify

def get_classes():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    query = '''
        SELECT id_class, class_name 
        FROM classes
    '''
    cursor.execute(query)
    classes = cursor.fetchall()
    conn.close()

    return classes

def get_subjects():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    query = '''
        SELECT id_subject, subject_name 
        FROM subjects
    '''
    cursor.execute(query)
    subjects = cursor.fetchall()
    conn.close()

    return subjects

def get_attendance_data(class_id, subject_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    query = '''
        SELECT 
        lessons.date, 
        lessons.start_time, 
        students.id_student, 
        users.firstName, 
        users.lastName
    FROM lessons
    JOIN students ON lessons.id_class = students.id_class
    JOIN users ON students.id_user = users.id
    WHERE lessons.id_class = ? AND lessons.id_subject = ?
    '''
    cursor.execute(query, (class_id, subject_id))
    attendance_data = cursor.fetchall()
    conn.close()
    return attendance_data

def get_lessons(class_id, subject_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    query = '''
        SELECT lessons.id_lesson, lessons.date, lessons.start_time
        FROM lessons
        WHERE lessons.id_class = ? AND lessons.id_subject = ?
    '''
    cursor.execute(query, (class_id, subject_id))
    lessons = cursor.fetchall()

    query_students = '''
        SELECT students.id_student, users.firstName || ' ' || users.lastName AS student_name
        FROM students
        JOIN users ON students.id_user = users.id
        WHERE students.id_class = ?
    '''
    cursor.execute(query_students, (class_id,))
    students = cursor.fetchall()

    conn.close()
    return lessons, students

def get_existing_attendance(class_id, subject_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    query = '''
        SELECT 
            presences.id_lesson, 
            presences.id_student, 
            presences.status
        FROM presences
        JOIN lessons ON presences.id_lesson = lessons.id_lesson
        WHERE lessons.id_class = ? AND lessons.id_subject = ?
    '''
    cursor.execute(query, (class_id, subject_id))
    existing_attendance = cursor.fetchall()
    conn.close()

    attendance_dict = {}
    for lesson_id, student_id, status in existing_attendance:
        if lesson_id not in attendance_dict:
            attendance_dict[lesson_id] = {}
        attendance_dict[lesson_id][student_id] = status

    return attendance_dict



import time

def save_attendance_changes(attendance_data):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Ustawienie PRAGMA busy_timeout
    cursor.execute('PRAGMA busy_timeout = 3000')  # Czas oczekiwania na odblokowanie (w milisekundach)

    for entry in attendance_data:
        lesson_id = entry['lessonId']
        student_id = entry['studentId']
        status = entry['status']

        attempt = 0
        max_attempts = 5
        while attempt < max_attempts:
            try:
                # Sprawdzenie czy wpis już istnieje
                cursor.execute('''
                    SELECT id_presence FROM presences WHERE id_lesson = ? AND id_student = ?
                ''', (lesson_id, student_id))
                existing_entry = cursor.fetchone()

                if existing_entry:
                    # Jeśli wpis istnieje, zaktualizuj go
                    cursor.execute('''
                        UPDATE presences SET status = ? WHERE id_lesson = ? AND id_student = ?
                    ''', (status, lesson_id, student_id))
                else:
                    # Jeśli wpis nie istnieje, wstaw nowy rekord
                    cursor.execute('''
                        INSERT INTO presences (id_student, id_lesson, status) 
                        VALUES (?, ?, ?)
                    ''', (student_id, lesson_id, status))

                conn.commit()
                break
            except sqlite3.OperationalError as e:
                if "database is locked" in str(e):
                    attempt += 1
                    time.sleep(1)  # Czekaj 1 sekundę przed ponowną próbą
                else:
                    raise e
    conn.close()
    return {'message': 'Attendance saved successfully'}



def get_student_id(id_user):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    query = '''
    SELECT id_student
    FROM students
    WHERE id_user = ?
    '''
    
    cursor.execute(query, (id_user,))
    result = cursor.fetchone()
    conn.close()

    id_student = result[0] if result else None
    
    return id_student


def get_presence_status(id_lesson, id_student):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    query = '''
    SELECT status
    FROM presences
    WHERE id_lesson = ? AND id_student = ?
    '''
    
    cursor.execute(query, (id_lesson, id_student))
    result = cursor.fetchone()
    conn.close()

    status = result[0] if result else 'Nie wprowadzono obecności'
    
    return status


def get_lessons_with_presence(class_id, id_student):
    if not class_id:
        return jsonify([])  # Jeśli brak id klasy

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    query = '''
    SELECT 
        lessons.id_lesson,
        subjects.subject_name,
        lessons.start_time,
        lessons.end_time,
        lessons.room_number,
        users.firstName || ' ' || users.lastName AS teacher_name,
        lessons.date  
    FROM lessons
    JOIN teachers ON lessons.id_teacher = teachers.id_teacher
    JOIN users ON teachers.id_user = users.id
    JOIN subjects ON lessons.id_subject = subjects.id_subject
    WHERE lessons.id_class = ?
    '''
    cursor.execute(query, (class_id,))
    lessons = cursor.fetchall()
    conn.close()

    result = []

    for lesson in lessons:
        lesson_id = lesson[0]  # ID lekcji
        lesson_date = lesson[6]  # Data lekcji (w formacie YYYY-MM-DD)

        # Łączymy datę z czasem rozpoczęcia i zakończenia lekcji
        start_time = lesson[2]
        end_time = lesson[3]
        subject_name = lesson[1]
        room_number = lesson[4]
        teacher_name = lesson[5]

        start_datetime = datetime.combine(datetime.strptime(lesson_date, "%Y-%m-%d").date(), datetime.strptime(start_time, "%H:%M:%S").time())
        end_datetime = datetime.combine(datetime.strptime(lesson_date, "%Y-%m-%d").date(), datetime.strptime(end_time, "%H:%M:%S").time())

        # Pobranie statusu obecności
        presence_status = get_presence_status(lesson_id, id_student)

        # Dodajemy lekcję do wyników
        lesson_for_day = {
            'id': lesson_id,  # ID lekcji jako 'id'
            'title': subject_name,
            'start': start_datetime.isoformat(),  # Format ISO 8601
            'end': end_datetime.isoformat(),
            'room': room_number,
            'teacher': teacher_name,
            'status': presence_status,
            'description': f'Lekcja w sali {room_number}',
            'extendedProps': {
                'lessonId': lesson_id,
                'studentId': id_student,
                'status': presence_status,
                'room': room_number
            }
        }

        result.append(lesson_for_day)

    # Jeśli nie znaleziono żadnej lekcji, zwróć informację o braku zajęć
    if not result:
        result.append({
            'title': 'Brak lekcji',
            'start': datetime.now().isoformat(),
            'end': datetime.now().isoformat(),
            'description': 'Brak danych lekcji'
        })

    return jsonify(result)


#widok rodzica

def get_parent_id(user_id):
    """
    Pobiera id rodzica na podstawie id użytkownika.
    """
    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        query = '''
        SELECT id_parent
        FROM parents
        WHERE id_user = ?
        '''
        cursor.execute(query, (user_id,))
        parent_id = cursor.fetchone()

        conn.close()

        return parent_id[0] if parent_id else None
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None

def get_children_by_parent_id(parent_id):
    """
    Pobiera listę dzieci na podstawie id rodzica.
    """
    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        
        query = '''
        SELECT s.id_student, u.firstName, u.lastName
        FROM students s
        JOIN users u ON s.id_user = u.id
        WHERE s.id_parent = ?
        '''
        cursor.execute(query, (parent_id,))
        children = cursor.fetchall()
        
        conn.close()
        
        children_list = [
            {"id_student": child[0], "first_name": child[1], "last_name": child[2]}
            for child in children
        ]
        
        return children_list
        
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return []


#dziala dalej nw

def get_student_class_by_id(id_student):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    query = ''' SELECT id_class FROM students WHERE id_student = ? '''
    cursor.execute(query, (id_student,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None
