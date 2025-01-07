from flask import Blueprint, render_template, jsonify, request, session, redirect
from flask_login import login_required, current_user
from controllers.messages_controller import *
from datetime import datetime, timedelta
from flask_socketio import join_room, leave_room, send, SocketIO

messages_blueprint = Blueprint('messages', __name__)

@messages_blueprint.route('/messages')
@login_required
def messages():
    return render_template('messages.html', firstName=current_user.firstName, lastName=current_user.lastName, profession=current_user.profession)

@messages_blueprint.route('/messagesTeacher')
@login_required
def messagesTeacher():
    return render_template('teacher/messagesTeacher.html', firstName=current_user.firstName, lastName=current_user.lastName, profession=current_user.profession)

@messages_blueprint.route('/messagesStudent')
@login_required
def messagesStudent():
    return render_template('student/messagesStudent.html', firstName=current_user.firstName, lastName=current_user.lastName, profession=current_user.profession)

@messages_blueprint.route('/messagesParent')
@login_required
def messagesParent():
    return render_template('parent/messagesParent.html', firstName=current_user.firstName, lastName=current_user.lastName, profession=current_user.profession)


