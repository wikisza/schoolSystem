import sqlite3

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
        lessons.time, 
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
        SELECT lessons.id_lesson, lessons.date, lessons.time
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



def save_attendance_changes(attendance_data):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    for entry in attendance_data:
        lesson_id = entry['lessonId']
        student_id = entry['studentId']
        status = entry['status']

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
    conn.close()
    return {'message': 'Attendance saved successfully'}