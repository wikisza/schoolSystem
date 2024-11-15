from flask import Blueprint, render_template, jsonify
from flask_login import login_required, current_user
from controllers.messages_controller import *
from datetime import datetime, timedelta


messages_blueprint = Blueprint('messages', __name__)

@messages_blueprint.route('/messages')
@login_required
def messages():
    return render_template('messages.html', username=current_user.username, profession=current_user.profession)
