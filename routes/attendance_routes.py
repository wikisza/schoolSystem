from flask import Blueprint, render_template, jsonify
from flask_login import login_required, current_user
from controllers.attendance_controller import *
from datetime import datetime, timedelta


attendance_blueprint = Blueprint('attendance', __name__)

@attendance_blueprint.route('/attendance')
@login_required
def attendance():
    return render_template('attendance.html', username=current_user.username, profession=current_user.profession)
