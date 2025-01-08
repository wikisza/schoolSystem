import sqlite3

def get_students_for_class_leader(teacher_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Pobierz wszystkie klasy, w których nauczyciel jest wychowawcą
    query = '''
    SELECT classes.id_class, classes.class_name
    FROM classes
    WHERE classes.id_teacher = (
        SELECT id_teacher FROM teachers WHERE id_user = ?
    )
    '''
    cursor.execute(query, (teacher_id,))
    classes = cursor.fetchall()

    students_in_classes = {}

    for class_id, class_name in classes:
        # Pobierz uczniów przypisanych do tej klasy, a także ich rodziców
        query_students = '''
        SELECT users.firstName, users.lastName, users.email, users.phoneNumber, users.address, 
               parents.id_parent, parent_users.firstName AS parent_firstName, parent_users.lastName AS parent_lastName
        FROM students
        JOIN users ON students.id_user = users.id
        LEFT JOIN parents ON students.id_parent = parents.id_parent
        LEFT JOIN users AS parent_users ON parents.id_user = parent_users.id
        WHERE students.id_class = ?
        '''
        cursor.execute(query_students, (class_id,))
        students = cursor.fetchall()

        # Przekształć dane na słownik
        students_in_classes[class_name] = [
            {
                "firstName": student[0],
                "lastName": student[1],
                "email": student[2],
                "phoneNumber": student[3],
                "address": student[4],
                "parentName": f"{student[6]} {student[7]}" if student[5] else "Brak"
            }
            for student in students
        ]

    conn.close()
    return students_in_classes



def is_class_leader(user_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Pobierz id_teacher na podstawie id_user
    query_teacher = '''
    SELECT id_teacher
    FROM teachers
    WHERE id_user = ?
    '''
    cursor.execute(query_teacher, (user_id,))
    result_teacher = cursor.fetchone()

    if not result_teacher:
        # Jeśli użytkownik nie jest przypisany do nauczyciela, nie jest wychowawcą
        conn.close()
        return False

    id_teacher = result_teacher[0]

    # Sprawdź, czy nauczyciel (id_teacher) jest przypisany do jakiejkolwiek klasy
    query_class = '''
    SELECT COUNT(*)
    FROM classes
    WHERE id_teacher = ?
    '''
    cursor.execute(query_class, (id_teacher,))
    result_class = cursor.fetchone()

    conn.close()

    # Jeśli COUNT(*) > 0, użytkownik jest wychowawcą
    return result_class[0] > 0

