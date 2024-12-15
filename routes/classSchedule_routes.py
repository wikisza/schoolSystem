from flask import Blueprint, render_template, jsonify, request
from flask_login import login_required, current_user
from controllers.classSchedule_controller import *
from datetime import datetime, timedelta
from controllers.classSchedule_controller import addClass, addGroup, search_items

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

@classSchedule_blueprint.route('/createSchedule')
@login_required
def createSchedule_route():
    return render_template('administration/createSchedule.html', firstName=current_user.firstName, lastName=current_user.lastName, profession=current_user.profession)

@classSchedule_blueprint.route('/classManagement')
@login_required
def classManagement_route():
    return render_template('administration/classManagement.html', firstName=current_user.firstName, lastName=current_user.lastName, profession=current_user.profession)

@classSchedule_blueprint.route('/addNewGroup')
def addNewGroup_route():
    return render_template('administration/addNewGroup.html', firstName=current_user.firstName, lastName=current_user.lastName, profession=current_user.profession)

@classSchedule_blueprint.route('/addGroup', methods=['POST'])
def addGroup_route():
    className = request.form['className']
    result = addGroup(className)

    return render_template('administration/classManagement.html', result=result, firstName=current_user.firstName, lastName=current_user.lastName, profession=current_user.profession)

@classSchedule_blueprint.route('/editClass')
@login_required
def editClass_route():
    return render_template('administration/editClass.html', firstName=current_user.firstName, lastName=current_user.lastName, profession=current_user.profession)

@classSchedule_blueprint.route('/search_items', methods=['GET'])
def search_items_route():
    result = search_items()

    return render_template('administration/editClass.html',result=result, firstName=current_user.firstName, lastName=current_user.lastName, profession=current_user.profession)




