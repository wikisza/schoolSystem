import sqlite3

def get_students_for_class_leader(teacher_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # Pobierz wszystkie klasy, w których nauczyciel jest wychowawcą
    query = '''
    SELECT classes.id_class, classes.class_name
    FROM classes
    JOIN teachers ON teachers.id_teacher = classes.id_teacher
    WHERE teachers.id_teacher = ?
    '''
    cursor.execute(query, (teacher_id,))
    classes = cursor.fetchall()
    
    students_in_classes = {}
    
    # Dla każdej klasy nauczyciela pobieramy listę uczniów
    for class_data in classes:
        class_id = class_data[0]
        
        # Pobierz uczniów przypisanych do tej klasy
        query_students = '''
        SELECT users.firstName || ' ' || users.lastName 
        FROM students 
        JOIN users ON students.id_user = users.id
        WHERE students.id_class = ?
        '''
        cursor.execute(query_students, (class_id,))
        students = cursor.fetchall()
        
        students_in_classes[class_data[1]] = [student[0] for student in students]
    
    conn.close()
    
    return students_in_classes
