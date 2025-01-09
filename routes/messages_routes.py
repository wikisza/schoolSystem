from flask import Blueprint, render_template, jsonify, request, session, redirect
from flask_login import login_required, current_user
from controllers.messages_controller import *
from datetime import datetime, timedelta
from flask_socketio import join_room, leave_room, send, emit, SocketIO
import logging

messages_blueprint = Blueprint('messages', __name__)

socketio = SocketIO()

@messages_blueprint.route('/messages')
@login_required
def messages():
    return render_template('messages.html',firstName=current_user.firstName, lastName = current_user.lastName, username=current_user.username, profession=current_user.profession)

@messages_blueprint.route('/messagesTeacher')
@login_required
def messagesTeacher():
    rooms = get_rooms(current_user.id)
    return render_template('teacher/messagesTeacher.html',firstName=current_user.firstName, lastName = current_user.lastName, username=current_user.username, profession=current_user.profession, rooms=rooms)

@messages_blueprint.route('/messagesStudent')
@login_required
def messagesStudent():
    rooms = get_rooms(current_user.id)
    return render_template('student/messagesStudent.html',firstName=current_user.firstName, lastName = current_user.lastName, username=current_user.username, profession=current_user.profession, rooms=rooms)

@messages_blueprint.route('/messagesParent')
@login_required
def messagesParent():
    rooms = get_rooms(current_user.id)
    return render_template('parent/messagesParent.html', firstName=current_user.firstName, lastName = current_user.lastName,username=current_user.username, profession=current_user.profession, rooms=rooms)




@socketio.on('send_message')
@login_required
def handle_message(data):
    room_id = data['room']
    message = data['message']
    user_id = current_user.id
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    save_message(room_id, user_id, message, timestamp)

    send({
        'message':message,
        'sender_id':user_id,
        'timestamp':timestamp,
        'room':room_id

    },room=room_id)

@socketio.on('join')
@login_required
def on_join(data):
    room_id = data['room']
    join_room(room_id)

    messages = get_messages(room_id)

    for message in messages:
        send({
            'message': message['content'],
            'sender_name': message['sender_name'],
            'timestamp': message['timestamp'],
            'room': room_id,
            'user_id': message['sender_id'],  # Send sender ID to differentiate
        }, room=room_id)  # Send to all clients in the room
    

@socketio.on('create_room')
@login_required
def handle_create_room(data):
    room_name = data['room_name']
    creator_id = current_user.id
    user_ids = data.get('user_ids', [])

    # Save room in the database
    room_id = create_room(room_name, creator_id)
    if user_ids:
        add_users_to_room(room_id, user_ids)

    # Send a response back to the client (including the new room details)
    emit('room_created', {
        'room_id': room_id,
        'room_name': room_name
    }, room=room_id)



@socketio.on('leave')
@login_required
def handle_leave(data):
    room_id = data['room']
    leave_room(room_id)


@messages_blueprint.route('/search-users', methods=['GET'])
@login_required
def search_users_route():
    query = request.args.get('q', '').strip()
    print(query)
    return search_users(query)