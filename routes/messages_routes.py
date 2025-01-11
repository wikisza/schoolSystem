from flask import Blueprint, render_template, jsonify, request, session, redirect
from flask_login import login_required, current_user
from controllers.messages_controller import *
from datetime import datetime, timedelta
from flask_socketio import join_room, leave_room, send, emit, SocketIO

messages_blueprint = Blueprint('messages', __name__)

socketio = SocketIO()

@messages_blueprint.route('/messages')
@login_required
def messages():
    return render_template('messages.html',firstName=current_user.firstName, lastName = current_user.lastName, username=current_user.username, profession=current_user.profession)


@messages_blueprint.route('/messagesTeacher')
@login_required
def messagesTeacher():
    user_id = current_user.id
    rooms = get_rooms(current_user.id)
    return render_template('teacher/messagesTeacher.html',user =user_id , firstName=current_user.firstName, lastName = current_user.lastName, username=current_user.username, profession=current_user.profession, rooms=rooms)

@messages_blueprint.route('/messagesStudent')
@login_required
def messagesStudent():
    user_id = current_user.id
    rooms = get_rooms(current_user.id)
    return render_template('student/messagesStudent.html',user=user_id,firstName=current_user.firstName, lastName = current_user.lastName, username=current_user.username, profession=current_user.profession, rooms=rooms)

@messages_blueprint.route('/messagesParent')
@login_required
def messagesParent():
    user_id = current_user.id
    rooms = get_rooms(current_user.id)
    return render_template('parent/messagesParent.html', user= user_id,firstName=current_user.firstName, lastName = current_user.lastName,username=current_user.username, profession=current_user.profession, rooms=rooms)

@messages_blueprint.route('/messagesAdministration')
@login_required
def messagesAdministration():
    user_id = current_user.id
    rooms = get_rooms(current_user.id)
    return render_template('administration/messagesAdministration.html',user=user_id, firstName=current_user.firstName, lastName = current_user.lastName, username=current_user.username, profession=current_user.profession, rooms=rooms)


@messages_blueprint.route('/search-users', methods=['GET'])
@login_required
def search_users_route():
    query = request.args.get('q', '').strip()
    if current_user.profession == "uczen":
        return search_users_uczen(query, excluded_id = current_user.id)
    if current_user.profession == "rodzic":
        return search_users_parent(query, excluded_id = current_user.id)
    else:
        return search_users(query, excluded_id = current_user.id)
    

    



def register_message_socketio(socketio):
    @socketio.on('connect')
    def test_connect():
        print('Client connected')
        
    @socketio.on('create_room')
    @login_required
    def handle_create_room(data):
        room_name = data['room_name']
        creator_id = current_user.id
        user_ids = data.get('user_ids', [])
        existing_room = check_existing_room(user_ids)
        if existing_room:
            emit('error', {'message': 'A room with the same members already exists!', 'room_id': existing_room})
            return
        # Save room in the database
        room_id = create_room(room_name, creator_id)
        if user_ids:
            add_users_to_room(room_id, user_ids)
        
        # Broadcast the event to all clients
        emit('room_created', {
            'room_id': room_id,
            'room_name': room_name,
            'creator_id': creator_id,
            'user_ids': user_ids  # Include the list of invited user IDs
        }, broadcast=True)  # Broadcast to all connected clients

        print(f"Room created with ID {room_id} and broadcasted to users {user_ids}")

    @socketio.on('join')
    @login_required
    def on_join(data):
        room_id = data['room']
        join_room(room_id)

        messages = get_messages(room_id)

        if messages:
            # Emit all messages as a single array
            emit("messages", {
                'messages': [
                    {
                        'message': message['content'],
                        'sender_name': message['sender_name'],
                        'timestamp': message['timestamp'],
                        'room': room_id,
                        'user_id': message['sender_id']
                    } for message in messages
                ],
                'room': room_id
            }, room=room_id)
        else:
            print('No messages found')

        print(f"User {current_user.id} joined room {room_id}")

    @socketio.on('send_message')
    @login_required
    def handle_message(data):
        room_id = data['room']
        message = data['message']
        user_id = current_user.id
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        sender_name = current_user.firstName + " " + current_user.lastName
        print(f"Received message: {message} from user {user_id} in room {room_id}")
        save_message(room_id, user_id, message, timestamp)
        
        emit("message", {
            'message': message,
            'sender_id': user_id,
            'timestamp': timestamp,
            'sender_name': sender_name,
            'room': room_id
        }, room=room_id)

    @socketio.on('leave')
    @login_required
    def handle_leave(data):
        room_id = data['room']
        leave_room(room_id)
        print(f"User {current_user.id} left room {room_id}")