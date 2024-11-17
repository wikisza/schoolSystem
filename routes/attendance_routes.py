from flask import Blueprint, render_template, jsonify
from flask_login import login_required, current_user
from controllers.attendance_controller import *
from datetime import datetime, timedelta


attendance_blueprint = Blueprint('attendance', __name__)

@attendance_blueprint.route('/attendance')
@login_required
def attendance():
    return render_template('attendance.html', username=current_user.username, profession=current_user.profession)

@attendance_blueprint.route('/attendanceTeacher')
@login_required
def attendanceTeacher():
    return render_template('teacher/attendanceTeacher.html', username=current_user.username, profession=current_user.profession)

@attendance_blueprint.route('/attendanceStudent')
@login_required
def attendanceStudent():
    return render_template('student/attendanceStudent.html', username=current_user.username, profession=current_user.profession)

@attendance_blueprint.route('/attendanceParent')
@login_required
def attendanceParent():
    return render_template('parent/attendanceParent.html', username=current_user.username, profession=current_user.profession)
