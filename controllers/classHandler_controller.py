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
               students.id_student, parents.id_parent, parent_users.firstName AS parent_firstName, parent_users.lastName AS parent_lastName
        FROM students
        JOIN users ON students.id_user = users.id
        LEFT JOIN parents ON students.id_parent = parents.id_parent
        LEFT JOIN users AS parent_users ON parents.id_user = parent_users.id
        WHERE students.id_class = ?
        '''
        cursor.execute(query_students, (class_id,))
        students = cursor.fetchall()

        # Debugowanie - sprawdź, czy students zawiera id_student
        print(f"Students for class {class_name}: {students}")

        # Przekształć dane na słownik
        students_in_classes[class_name] = [
            {
                "firstName": student[0],
                "lastName": student[1],
                "email": student[2],
                "phoneNumber": student[3],
                "address": student[4],
                "id_student": student[5],  # Sprawdzamy, czy id_student jest poprawnie przypisane
                "parentName": f"{student[7]} {student[8]}" if student[6] else "Brak"
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

def get_student_by_id(student_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    query = '''
    SELECT students.id_student, users.firstName, users.lastName, users.email, users.phoneNumber, users.address
    FROM students
    JOIN users ON students.id_user = users.id
    WHERE students.id_student = ?
    '''
    cursor.execute(query, (student_id,))
    student_data = cursor.fetchone()
    conn.close()

    if not student_data:
        return None

    return {
        "id_student": student_data[0],
        "firstName": student_data[1],
        "lastName": student_data[2],
        "email": student_data[3],
        "phoneNumber": student_data[4],
        "address": student_data[5],
    }


def update_student_data(student_id, updated_data):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Pobierz `id_user` ucznia na podstawie `id_student`
    query_user = '''
    SELECT id_user 
    FROM students 
    WHERE id_student = ?
    '''
    cursor.execute(query_user, (student_id,))
    result = cursor.fetchone()

    if not result:
        conn.close()
        return False

    user_id = result[0]

    # Zaktualizuj dane ucznia w tabeli `users`
    query_update_user = '''
    UPDATE users
    SET firstName = ?, lastName = ?, email = ?, phoneNumber = ?, address = ?
    WHERE id = ?
    '''
    cursor.execute(query_update_user, (
        updated_data["firstName"],
        updated_data["lastName"],
        updated_data["email"],
        updated_data["phoneNumber"],
        updated_data["address"],
        user_id
    ))

    # Jeśli dane rodzica zostały podane, zaktualizuj tabelę `parents`
    if "parentName" in updated_data and updated_data["parentName"] != "Brak":
        parent_first_name, parent_last_name = updated_data["parentName"].split(" ", 1)
        query_update_parent = '''
        UPDATE users
        SET firstName = ?, lastName = ?
        WHERE id = (
            SELECT id_user FROM parents
            WHERE id_parent = (
                SELECT id_parent FROM students WHERE id_student = ?
            )
        )
        '''
        cursor.execute(query_update_parent, (
            parent_first_name,
            parent_last_name,
            student_id
        ))

    conn.commit()
    conn.close()
    return True
