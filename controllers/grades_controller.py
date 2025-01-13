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
