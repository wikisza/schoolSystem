import sqlite3
from datetime import datetime

import logging

import sqlite3
from datetime import datetime

def get_student_grades(student_id):
    """
    Pobiera oceny ucznia z bazy danych na podstawie jego ID.
    """
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    query = '''
    SELECT subjects.subject_name, grades.value, grades.date, grades.comment
    FROM grades
    JOIN subjects ON grades.id_subject = subjects.id_subject
    WHERE grades.id_student = ?
    '''
    cursor.execute(query, (student_id,))
    grades = cursor.fetchall()

    conn.close()

    # Zwróć oceny ucznia w formie listy słowników
    return [
        {
            "subject": grade[0],
            "grade": grade[1],
            "date": grade[2],
            "comment": grade[3]
        }
        for grade in grades
    ]



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
