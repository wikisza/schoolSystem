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
    
def add_behaviour(id_student, behavior_type, behavior_note, current_user):
    try:
        # Connect to the database
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        # Query to insert behavior into the database
        query = """
        INSERT INTO student_behaviours (id_student, behaviour_type, created_at, created_by, details)
        VALUES (?, ?, datetime('now'), ?, ?)
        """
        cursor.execute(query, (id_student, behavior_type, current_user, behavior_note))
        conn.commit()
        conn.close()

        # Return response data as a dictionary (no jsonify here)
        return {"message": "Behavior added successfully"}, 200
    except sqlite3.Error as e:
        return {"error": f"Database error: {e}"}, 500

def get_student_id(user_id):
    try:
        # Connect to the database
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        # Execute the query to get the student ID based on the user ID
        cursor.execute("SELECT id_student FROM students WHERE id_user = ?", (user_id,))
        result = cursor.fetchone()

        # Close the database connection
        conn.close()

        # Check if a result was found
        if result:
            return {"student_id": result[0]}, 200
        else:
            return {"error": "Student ID not found"}, 404
    except sqlite3.Error as e:
        return {"error": f"Database error: {e}"}, 500
    
def get_behaviours_from_db(id_student):
    try:
        # Connect to the database
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        # Execute the query to get behaviors based on the student ID and join with the users table
        cursor.execute("""
            SELECT sb.id_behaviour, sb.id_student, sb.behaviour_type, sb.created_at, sb.created_by, sb.details, u.firstName, u.lastName
            FROM student_behaviours sb
            JOIN users u ON sb.created_by = u.id
            WHERE sb.id_student = ?
        """, (id_student,))
        behaviours = cursor.fetchall()

        # Close the database connection
        conn.close()

        # Check if any behaviors were found
        if behaviours:
            # Convert the result to a list of dictionaries
            behaviours_list = [
                {
                    "id_behaviour": row[0],
                    "id_student": row[1],
                    "behaviour_type": row[2],
                    "created_at": row[3],
                    "created_by": row[4],
                    "details": row[5],
                    "creator_first_name": row[6],
                    "creator_last_name": row[7]
                }
                for row in behaviours
            ]
            return behaviours_list, 200
        else:
            return [], 200
    except sqlite3.Error as e:
        return {"error": f"Database error: {e}"}, 500
    
def get_child_by_parent_id(parent_id):
    try:
        # Connect to the database
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        # Execute the query to get the child (student) information based on the parent ID
        cursor.execute("""
            SELECT s.id_student, u.firstName, u.lastName
            FROM students s
            JOIN users u ON s.id_user = u.id
            WHERE s.id_parent = ?
        """, (parent_id,))
        children = cursor.fetchall()

        # Close the database connection
        conn.close()

        # Check if any children were found
        if children:
            # Convert the result to a list of dictionaries
            children_list = [
                {
                    "id_student": row[0],
                    "first_name": row[1],
                    "last_name": row[2]
                }
                for row in children
            ]
            return children_list, 200
        else:
            return {"message": "No children found for this parent"}, 404
    except sqlite3.Error as e:
        return {"error": f"Database error: {e}"}, 500
    
def get_parent_id(user_id):
    try:
        # Connect to the database
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        # Execute the query to get the parent ID based on the user ID
        cursor.execute("SELECT id_parent FROM parents WHERE id_user = ?", (user_id,))
        result = cursor.fetchone()

        # Close the database connection
        conn.close()

        # Check if a result was found
        if result:
            return {"parent_id": result[0]}, 200
        else:
            return {"error": "Parent ID not found"}, 404
    except sqlite3.Error as e:
        return {"error": f"Database error: {e}"}, 500