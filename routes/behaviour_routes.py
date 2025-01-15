from flask import Blueprint, render_template, jsonify
from flask_login import login_required, current_user
from controllers.behaviour_controller import *
from datetime import datetime, timedelta

behaviour_blueprint = Blueprint('behaviour', __name__)

@behaviour_blueprint.route('/behaviour')
@login_required
def behaviour():
    return render_template('behaviour.html', firstName=current_user.firstName, lastName=current_user.lastName, profession=current_user.profession)

@behaviour_blueprint.route('/behaviourTeacher')
@login_required
def behaviourTeacher():
    print("Rendering behaviourTeacher.html") 
    return render_template('teacher/behaviourTeacher.html', firstName=current_user.firstName, lastName=current_user.lastName, profession=current_user.profession)

@behaviour_blueprint.route('/behaviourStudent')
@login_required
def behaviourStudent():
    return render_template('student/behaviourStudent.html', firstName=current_user.firstName, lastName=current_user.lastName, profession=current_user.profession)

@behaviour_blueprint.route('/behaviourParent')
@login_required
def behaviourParent():
    return render_template('parent/behaviourParent.html', firstName=current_user.firstName, lastName=current_user.lastName, profession=current_user.profession)

@behaviour_blueprint.route('/addBehaviour')
def addGrades_route():
    return render_template('teacher/addGrades.html', firstName=current_user.firstName, lastName=current_user.lastName, profession=current_user.profession)

