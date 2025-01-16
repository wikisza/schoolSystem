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

#nauczyciele bez wychowawstwa
def get_teachers_without_class():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    query = '''
    SELECT teachers.id_teacher, users.firstName || ' ' || users.lastName AS name
    FROM teachers
    JOIN users ON teachers.id_user = users.id
    WHERE teachers.id_teacher NOT IN (
        SELECT id_teacher FROM classes
    )
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

from datetime import datetime, timedelta

#lekcje danej klasy
def get_lessons(class_id):
    if not class_id:
        return jsonify([])  # Jeśli brak id klasy

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    query = '''
    SELECT 
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
        lesson_date = lesson[5]  # Data lekcji (w formacie YYYY-MM-DD)

        # Łączymy datę z czasem rozpoczęcia i zakończenia lekcji
        start_time = lesson[1]
        end_time = lesson[2]
        subject_name = lesson[0]
        room_number = lesson[3]
        teacher_name = lesson[4]

        start_datetime = datetime.combine(datetime.strptime(lesson_date, "%Y-%m-%d").date(), datetime.strptime(start_time, "%H:%M:%S").time())
        end_datetime = datetime.combine(datetime.strptime(lesson_date, "%Y-%m-%d").date(), datetime.strptime(end_time, "%H:%M:%S").time())

        # Dodajemy lekcję do wyników
        lesson_for_day = {
            'title': subject_name,
            'start': start_datetime.isoformat(),  # Format ISO 8601
            'end': end_datetime.isoformat(),
            'room': room_number,
            'teacher': teacher_name,
            'description': f'Lekcja w sali {room_number}'
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

def get_student_class(id_user):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    query = '''
    SELECT id_class
    FROM students
    WHERE id_user = ?
    '''
    
    cursor.execute(query, (id_user,))
    result = cursor.fetchone()
    conn.close()

    id_class = result[0] if result else None
    
    return id_class


#wszystkie przedmioty

def getSubjectsList():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    query = '''
    SELECT id_subject, subject_name
    FROM subjects
    '''
    cursor.execute(query)
    subjects = cursor.fetchall()
    conn.close()
    
    # Konwersja wyników do listy słowników dla lepszej obsługi w JSON
    subjects_list = [{'id': t[0], 'name': t[1]} for t in subjects]
    return jsonify(subjects_list)


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

#dodawanie lekcji do planu lekcji jakiejś klasy


def addNewSubjectToPlan(
    id_class, id_teacher, id_subject,room_number, stime, end_time, day_of_week,
    exact_date=None, semester_start=None, semester_end=None):
    
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    query = '''
    INSERT INTO lessons (id_class, id_teacher, id_subject, date, start_time, end_time, room_number) 
    VALUES (?, ?, ?, ?, ?, ?, ?)
    '''

    try:
        if exact_date:
            try:
                lesson_date = datetime.strptime(exact_date, "%Y-%m-%d").date()
                cursor.execute(query, (id_class, id_teacher, id_subject, lesson_date, stime, end_time, room_number))
                conn.commit()
            except ValueError:
                return jsonify({"error": "Invalid exact_date format. Use YYYY-MM-DD."}), 400
        else:
            # Jeśli `exact_date` jest None, sprawdzamy, czy podano `day_of_week`
            if day_of_week is not None:
                if not semester_start or not semester_end:
                    return jsonify({"error": "Semester start and end dates are required when adding lessons for a day of the week."}), 400

                # Określ zakres semestru
                semester_start = datetime.strptime(semester_start, "%Y-%m-%d").date()
                semester_end = datetime.strptime(semester_end, "%Y-%m-%d").date()

                # Znajdź pierwszy dzień tygodnia w semestrze
                current_date = semester_start

                print(f"Adding lesson: date={day_of_week or 'pusto' }")

                while current_date.weekday() != int(day_of_week):
                    current_date += timedelta(days=1)

                # Generuj zajęcia w podane dni tygodnia
                while current_date <= semester_end:
                    cursor.execute(query, (id_class, id_teacher, id_subject, current_date, stime, end_time, room_number))
                    current_date += timedelta(days=7)
                    conn.commit()
            else:
                return jsonify({"error": "Either exact_date or day_of_week must be provided."}), 400


    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    except Exception as e:
        return jsonify({"error": "An error occurred: " + str(e)}), 500

    finally:
        conn.close()



#pobieranie lekcji danego nauczyciela
def get_teacher_lessons(id_teacher):
    if not id_teacher:
        return jsonify([])  # Jeśli brak id nauczyciela

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    query = '''
    SELECT 
        subjects.subject_name,
        lessons.start_time,
        lessons.end_time,
        lessons.room_number,
        classes.class_name,
        lessons.date  
    FROM lessons
    JOIN teachers ON lessons.id_teacher = teachers.id_teacher
    JOIN users ON teachers.id_user = users.id
    JOIN subjects ON lessons.id_subject = subjects.id_subject
    JOIN classes ON lessons.id_class = classes.id_class
    WHERE lessons.id_teacher = ?
    '''
    cursor.execute(query, (id_teacher,))
    lessons = cursor.fetchall()
    conn.close()

    result = []

    for lesson in lessons:
        lesson_date = lesson[5]  # Data lekcji (w formacie YYYY-MM-DD)

        # Łączymy datę z czasem rozpoczęcia i zakończenia lekcji
        start_time = lesson[1]
        end_time = lesson[2]
        subject_name = lesson[0]
        room_number = lesson[3]
        class_name = lesson[4]

        start_datetime = datetime.combine(datetime.strptime(lesson_date, "%Y-%m-%d").date(), datetime.strptime(start_time, "%H:%M:%S").time())
        end_datetime = datetime.combine(datetime.strptime(lesson_date, "%Y-%m-%d").date(), datetime.strptime(end_time, "%H:%M:%S").time())

        print("godzina rozpoczecia", room_number)
        # Dodajemy lekcję do wyników
        lesson_for_day = {
            'title': subject_name,
            'start': start_datetime.isoformat(),  # Format ISO 8601
            'end': end_datetime.isoformat(),
            'room': room_number,
            'class_name': class_name,
            'description': f'Lekcja w sali {room_number}'
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

def get_id_teacher(id_user):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    query = '''
    SELECT id_teacher
    FROM teachers
    WHERE id_user = ?
    '''
    
    cursor.execute(query, (id_user,))
    result = cursor.fetchone()
    conn.close()

    teacher_id = result[0] if result else None
    
    return teacher_id


def SubjectTeacherConnection(id_subject, id_teacher):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO subjectsTeachers (id_subject, id_teacher) VALUES (?,?)', (id_subject,id_teacher,))
        conn.commit()
        return jsonify({"success": True}), 200
    except Exception as e:
        print(f"Błąd podczas przypisywania uczniów: {e}")
        return jsonify({"success": False}), 500
    finally:
        conn.close()