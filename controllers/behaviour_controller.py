import sqlite3
from flask import Blueprint, render_template, jsonify, request

def get_students_from_db(class_id):
    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        # Include student.id in the query
        query = """
        SELECT s.id_student, u.firstName || ' ' || u.lastName AS fullName
        FROM students s
        INNER JOIN users u ON s.id_user = u.id
        WHERE s.id_class = ?
        """
        cursor.execute(query, (class_id,))
        students = [{"id_student": row[0], "fullName": row[1]} for row in cursor.fetchall()]

        return students

    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return []

    finally:
        if conn:
            conn.close()


def get_classes_from_db():
    try:
        # Connect to the database
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        # Query to fetch all classes
        query = "SELECT id_class, class_name FROM classes"
        cursor.execute(query)
        classes = cursor.fetchall()

        # Close the database connection
        conn.close()

        # Format the classes into a list of dictionaries
        return [{"class_id": cls[0], "class_name": cls[1]} for cls in classes]

    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return []