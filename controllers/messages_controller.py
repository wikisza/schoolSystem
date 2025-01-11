import sqlite3
from flask import Blueprint, render_template, jsonify, request


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn



def add_users_to_room(room_id, user_ids):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Add the users to the room_users table
    for user_id in user_ids:
        cursor.execute(
            'INSERT INTO room_users (id_room, id_user) VALUES (?, ?)', 
            (room_id, user_id)
        )
    conn.commit()
    conn.close()

def create_room(name, creator_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO chat_rooms  (name, creator_id) VALUES(?, ?)', 
        (name, creator_id)
    )
    conn.commit()
    room_id = cursor.lastrowid
    conn.close()
    return room_id
def get_user_by_id(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT firstName, lastName FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user

def get_rooms(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Corrected query to properly compare with 'Tak'
    cursor.execute("""
        SELECT r.id_room, r.name, r.creator_id 
        FROM room_users ru
        JOIN chat_rooms r ON ru.id_room = r.id_room
        WHERE ru.id_user = ? 
    """, (user_id,))

    rooms = cursor.fetchall()
    conn.close()

    if rooms:
        # Return rooms with the correct number of fields
        return [{
            'id': room[0],           # Room ID
            'name': room[1],         # Room name
            'creator_id': room[2]    # Creator ID
        } for room in rooms]
    else:
        return None
    
def check_existing_room(user_ids):
    conn = get_db_connection()
    cursor = conn.cursor()

    user_ids = sorted(user_ids)  # Sort the user IDs to ensure consistency
    
    cursor.execute("""
        SELECT ru.id_room, GROUP_CONCAT(ru.id_user ORDER BY ru.id_user) AS user_ids
        FROM room_users ru
        GROUP BY ru.id_room
    """)

    rooms = cursor.fetchall()

    # Iterate through the results to check for a match
    for room in rooms:
        room_user_ids = room['user_ids'].split(',')  # Split the user IDs
        room_user_ids = list(map(int, room_user_ids))  # Convert to integers
        if room_user_ids == user_ids:
            conn.close()
            return room['id_room']  # Return the existing room ID

    conn.close()
    return None  # No matching room found

def save_message(id_room, user_id, message, timestamp):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO messages (id_room, id_sender, content, timestamp) VALUES (?, ?, ?, ?)',
        (id_room, user_id, message, timestamp)
    )
    conn.commit()
    conn.close()

def get_messages(id_room):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Query to get messages along with sender info (join messages with users table)
    cursor.execute("""
        SELECT m.id_message, m.id_room, m.id_sender, m.content, m.timestamp, u.firstName, u.lastName
        FROM messages m
        JOIN users u ON m.id_sender = u.id
        WHERE m.id_room = ?
        ORDER BY m.timestamp ASC
    """, (id_room,))

    messages = cursor.fetchall()  # Fetch all messages for the room

    # Close the connection
    conn.close()

    # Return a list of messages with sender's full name and message content
    return [{
        'id': message[0],
        'id_room': message[1],
        'sender_id': message[2],
        'content': message[3],
        'timestamp': message[4],
        'sender_name': f"{message[5]} {message[6]}"  # Concatenate firstName and lastName
    } for message in messages]



def search_users(query, excluded_id):
    if not query:
        return jsonify([])  # Return an empty list if the query is empty

    try:
        # Connect to the database
        connection = get_db_connection()
        cursor = connection.cursor()

        # SQL query to find matches in firstName, lastName, or profesion
        cursor.execute("""
            SELECT id, firstName, lastName, profession
            FROM users
            WHERE (LOWER(firstName) LIKE ? OR LOWER(lastName) LIKE ? OR LOWER(profession) LIKE ?)
            AND id!=? AND profession!= 'admin'
            LIMIT 30
        """, (query.lower() + '%', query.lower() + '%', query.lower() + '%', excluded_id))

        results = cursor.fetchall()

        # Format the results as a list of dictionaries
        users = [{'id': row['id'], 'name': f"{row['firstName']} {row['lastName']}", 'profession': row['profession']} for row in results]

        return jsonify(users)  # Return a JSON response with IDs, names, and professions

    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500  # Return error if any

    finally:
        if connection:
            connection.close()
def search_users_parent(query, excluded_id):
    if not query:
        return jsonify([])  # Return an empty list if the query is empty

    try:
        # Connect to the database
        connection = get_db_connection()
        cursor = connection.cursor()

        # SQL query to find matches in firstName, lastName, or profesion
        cursor.execute("""
            SELECT id, firstName, lastName, profession
            FROM users
            WHERE (LOWER(firstName) LIKE ? OR LOWER(lastName) LIKE ? OR LOWER(profession) LIKE ?)
            AND id!=? AND profession!= 'uczen' AND profession!='rodzic' AND profession!='admin'
            LIMIT 30
        """, (query.lower() + '%', query.lower() + '%', query.lower() + '%', excluded_id))

        results = cursor.fetchall()

        # Format the results as a list of dictionaries
        users = [{'id': row['id'], 'name': f"{row['firstName']} {row['lastName']}", 'profession': row['profession']} for row in results]

        return jsonify(users)  # Return a JSON response with IDs, names, and professions

    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500  # Return error if any

    finally:
        if connection:
            connection.close()

def search_users_uczen(query, excluded_id):
    if not query:
        return jsonify([])  # Return an empty list if the query is empty

    try:
        # Connect to the database
        connection = get_db_connection()
        cursor = connection.cursor()

        # SQL query to find matches in firstName, lastName, or profesion
        cursor.execute("""
            SELECT id, firstName, lastName, profession
            FROM users
            WHERE (LOWER(firstName) LIKE ? OR LOWER(lastName) LIKE ? OR LOWER(profession) LIKE ?)
            AND id!=? AND profession!= 'rodzic'
            LIMIT 30
        """, (query.lower() + '%', query.lower() + '%', query.lower() + '%', excluded_id))

        results = cursor.fetchall()

        # Format the results as a list of dictionaries
        users = [{'id': row['id'], 'name': f"{row['firstName']} {row['lastName']}", 'profession': row['profession']} for row in results]

        return jsonify(users)  # Return a JSON response with IDs, names, and professions

    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500  # Return error if any

    finally:
        if connection:
            connection.close()



def is_user_member(user_id, room_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Query to check if the user is a member of the room
    cursor.execute("""
        SELECT 1 FROM room_users 
        WHERE id_user = ? AND id_room = ?
    """, (user_id, room_id))

    result = cursor.fetchone()  # Fetch one result

    conn.close()

    # If result is found, it means the user is a member of the room
    return result is not None