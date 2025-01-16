import sqlite3
from datetime import datetime

import logging

import sqlite3
from datetime import datetime

def get_student_grades(student_id):
    """
    Pobiera oceny ucznia z bazy danych, pogrupowane według przedmiotu i kategorii.
    """
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    query = '''
    SELECT
        subjects.subject_name,
        grades_category.nazwa AS category_name,
        grades_category.waga AS category_weight,
        grades.value,
        grades.date,
        grades.comment
    FROM grades
    JOIN subjects ON grades.id_subject = subjects.id_subject
    JOIN grades_category ON grades.id_category = grades_category.id_category
    WHERE grades.id_student = ?
    ORDER BY subjects.subject_name, grades_category.id_category;
    '''
    cursor.execute(query, (student_id,))
    grades = cursor.fetchall()

    conn.close()

    # Zgrupowanie ocen według przedmiotów i kategorii
    grouped_grades = {}
    for grade in grades:
        subject = grade[0]
        category = grade[1]
        weight = grade[2]
        value = grade[3]
        date = grade[4]
        comment = grade[5]
        
        if subject not in grouped_grades:
            grouped_grades[subject] = {
                "sprawdzian": [],
                "prace klasowe": [],
                "zadania domowe": [],
                "aktywność": []  # Nowa kategoria
            }

        grade_data = {"value": value, "category": category, "weight": weight, "date": date, "comment": comment}
        if category == "sprawdzian":
            grouped_grades[subject]["sprawdzian"].append(grade_data)
        elif category == "praca klasowa":
            grouped_grades[subject]["prace klasowe"].append(grade_data)
        elif category == "zadanie domowe":
            grouped_grades[subject]["zadania domowe"].append(grade_data)
        elif category == "aktywność":  # Obsługa aktywności
            grouped_grades[subject]["aktywność"].append(grade_data)

    return grouped_grades



def get_teacher_grades(id_teacher):
    """
    Pobiera oceny ucznia z bazy danych, pogrupowane według przedmiotu i kategorii.
    """
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    query = '''
    SELECT
        subjects.subject_name,
        grades_category.nazwa AS category_name,
        grades_category.waga AS category_weight,
        grades.value,
        grades.date,
        grades.comment
    FROM grades
    JOIN subjects ON grades.id_subject = subjects.id_subject
    JOIN grades_category ON grades.id_category = grades_category.id_category
    WHERE grades.id_teacher = ?
    ORDER BY subjects.subject_name, grades_category.id_category;
    '''
    cursor.execute(query, (student_id,))
    grades = cursor.fetchall()

    conn.close()

    # Zgrupowanie ocen według przedmiotów i kategorii
    grouped_grades = {}
    for grade in grades:
        subject = grade[0]
        category = grade[1]
        weight = grade[2]
        value = grade[3]
        date = grade[4]
        comment = grade[5]
        
        if subject not in grouped_grades:
            grouped_grades[subject] = {
                "sprawdzian": [],
                "prace klasowe": [],
                "zadania domowe": [],
                "aktywność": []  # Nowa kategoria
            }

        grade_data = {"value": value, "category": category, "weight": weight, "date": date, "comment": comment}
        if category == "sprawdzian":
            grouped_grades[subject]["sprawdzian"].append(grade_data)
        elif category == "praca klasowa":
            grouped_grades[subject]["prace klasowe"].append(grade_data)
        elif category == "zadanie domowe":
            grouped_grades[subject]["zadania domowe"].append(grade_data)
        elif category == "aktywność":  # Obsługa aktywności
            grouped_grades[subject]["aktywność"].append(grade_data)

    return grouped_grades



def get_all_parents():
    """
    Pobiera wszystkich rodziców z bazy danych.
    """
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    query = '''
    SELECT parents.id_parent, users.firstName, users.lastName
    FROM parents
    JOIN users ON parents.id_user = users.id
    '''
    cursor.execute(query)
    parents = cursor.fetchall()

    conn.close()

    # Zwróć listę rodziców jako słownik
    return [{"id_parent": parent[0], "name": f"{parent[1]} {parent[2]}"} for parent in parents]

def get_student_id(user_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    query = '''
    SELECT id_student
    FROM students
    WHERE id_user = ?
    '''
    cursor.execute(query, (user_id,))
    student_id = cursor.fetchone()

    conn.close()

    return student_id[0] if student_id else None


import sqlite3

def get_parent_children(parent_id):
    """
    Pobiera dzieci dla danego rodzica.
    """
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    query = '''
    SELECT students.id_student, users.firstName, users.lastName
    FROM students
    JOIN users ON students.id_user = users.id
    WHERE students.id_parent = ?
    '''
    cursor.execute(query, (parent_id,))
    children = cursor.fetchall()

    conn.close()

    # Zwróć listę dzieci jako słownik
    return [{"id_student": child[0], "name": f"{child[1]} {child[2]}"} for child in children]

def get_children_grades(parent_id):
    """
    Pobiera oceny wszystkich dzieci danego rodzica.
    """
    children = get_parent_children(parent_id)

    if not children:
        return {}

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    grades_by_child = {}

    for child in children:
        child_id = child['id_student']
        child_name = child['name']

        query = '''
        SELECT
            subjects.subject_name,
            grades_category.nazwa AS category_name,
            grades_category.waga AS category_weight,
            grades.value,
            grades.date,
            grades.comment
        FROM grades
        JOIN subjects ON grades.id_subject = subjects.id_subject
        JOIN grades_category ON grades.id_category = grades_category.id_category
        WHERE grades.id_student = ?
        ORDER BY subjects.subject_name, grades_category.id_category
        '''
        cursor.execute(query, (child_id,))
        grades = cursor.fetchall()

        # Zgrupowanie ocen według przedmiotów i kategorii
        grouped_grades = {}
        for grade in grades:
            subject = grade[0]
            category = grade[1]
            weight = grade[2]
            value = grade[3]
            date = grade[4]
            comment = grade[5]

            if subject not in grouped_grades:
                grouped_grades[subject] = {
                    "sprawdzian": [],
                    "prace klasowe": [],
                    "zadania domowe": [],
                    "aktywność": []  # Nowa kategoria
                }

            grade_data = {"value": value, "category": category, "weight": weight, "date": date, "comment": comment}
            if category == "sprawdzian":
                grouped_grades[subject]["sprawdzian"].append(grade_data)
            elif category == "praca klasowa":
                grouped_grades[subject]["prace klasowe"].append(grade_data)
            elif category == "zadanie domowe":
                grouped_grades[subject]["zadania domowe"].append(grade_data)
            elif category == "aktywność":  # Obsługa aktywności
                grouped_grades[subject]["aktywność"].append(grade_data)

        grades_by_child[child_name] = grouped_grades

    conn.close()
    return grades_by_child

def get_parent_id(user_id):
    """
    Pobiera id rodzica na podstawie id użytkownika.
    """
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
