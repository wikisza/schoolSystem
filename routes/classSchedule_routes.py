from flask import Blueprint, render_template, jsonify, request
from flask_login import login_required, current_user
from controllers.classSchedule_controller import *
from datetime import datetime, timedelta
from controllers.classSchedule_controller import addClass

classSchedule_blueprint = Blueprint('classSchedule', __name__)

@classSchedule_blueprint.route('/classSchedule')
@login_required
def classSchedule():
    return render_template('classSchedule.html', firstName=current_user.firstName, lastName=current_user.lastName, profession=current_user.profession)

@classSchedule_blueprint.route('/scheduleTeacher')
@login_required
def scheduleTeacher_route():
    return render_template('teacher/scheduleTeacher.html', firstName=current_user.firstName, lastName=current_user.lastName, profession=current_user.profession)

@classSchedule_blueprint.route('/scheduleStudent')
@login_required
def scheduleStudent_route():
    return render_template('student/scheduleStudent.html', firstName=current_user.firstName, lastName=current_user.lastName, profession=current_user.profession)

@classSchedule_blueprint.route('/scheduleParent')
@login_required
def scheduleParent_route():
    return render_template('parent/scheduleParent.html', firstName=current_user.firstName, lastName=current_user.lastName, profession=current_user.profession)

@classSchedule_blueprint.route('/scheduleAdmin')
@login_required
def scheduleAdmin_route():
    return render_template('administration/scheduleAdmin.html', firstName=current_user.firstName, lastName=current_user.lastName, profession=current_user.profession)

@classSchedule_blueprint.route('/addNewClass')
@login_required
def addNewClass_route():
    return render_template('administration/addNewClass.html', firstName=current_user.firstName, lastName=current_user.lastName, profession=current_user.profession)

@classSchedule_blueprint.route('/addClass', methods=['POST'])
def addClass_route():
    className = request.form['className']
    result = addClass(className)

    return render_template('/administration/addNewClass.html', result=result, firstName=current_user.firstName, lastName=current_user.lastName, profession=current_user.profession)