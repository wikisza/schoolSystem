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

def get_rooms(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Updated query to include 'creator_id' from the 'chat_rooms' table
    cursor.execute(
        'SELECT r.id_room, r.name, r.creator_id FROM room_users ru '
        'JOIN chat_rooms r ON ru.id_room = r.id_room '
        'WHERE ru.id_user = ?',
        (user_id,)
    )
    
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



def save_message(id_room, user_id, message, timestamp):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO messages (id_room, id_sender, message, timestamp) VALUES (?, ?, ?, ?)',
        (id_room, user_id, message, timestamp)
    )
    conn.commit()
    conn.close()

def get_messages(id_room):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Query to get messages along with sender info (join messages with users table)
    cursor.execute("""
        SELECT m.id, m.id_room, m.sender_id, m.content, m.timestamp, u.username
        FROM messages m
        JOIN users u ON m.sender_id = u.id
        WHERE m.id_room = ?
        ORDER BY m.timestamp ASC
    """, (id_room,))

    messages = cursor.fetchall()  # Fetch all messages for the room

    # Close the connection
    conn.close()

    # Return a list of messages with sender's name and message content
    return [{
        'id': message[0],
        'id_room': message[1],
        'sender_id': message[2],
        'content': message[3],
        'timestamp': message[4],
        'sender_name': message[5]  # Include sender's name from the users table
    } for message in messages]

from flask import jsonify, request

def search_users(query):
    if not query:
        return jsonify([])  # Return an empty list if the query is empty

    try:
        # Connect to the database
        connection = get_db_connection()
        cursor = connection.cursor()

        # SQL query to find matches in firstName or lastName
        cursor.execute("""
            SELECT id, firstName, lastName
            FROM users
            WHERE LOWER(firstName) LIKE ? OR LOWER(lastName) LIKE ?
            LIMIT 30
        """, (query.lower() + '%', query.lower() + '%'))

        results = cursor.fetchall()

        # Format the results as a list of dictionaries
        users = [{'id': row['id'], 'name': f"{row['firstName']} {row['lastName']}"} for row in results]

        return jsonify(users)  # Return a JSON response with both IDs and names

    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500  # Return error if any

    finally:
        if connection:
            connection.close()