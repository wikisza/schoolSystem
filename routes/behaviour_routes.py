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

    # Fetch all classes from the database
    classes = get_classes_from_db()
    print(classes)
    # Pass classes to the template
    return render_template(
        'teacher/behaviourTeacher.html', 
        firstName=current_user.firstName, 
        lastName=current_user.lastName, 
        profession=current_user.profession, 
        classes=classes
    )

@behaviour_blueprint.route('/behaviourStudent')
@login_required
def behaviourStudent():
    return render_template('student/behaviourStudent.html', firstName=current_user.firstName, lastName=current_user.lastName, profession=current_user.profession)

@behaviour_blueprint.route('/behaviourParent')
@login_required
def behaviourParent():
    return render_template('parent/behaviourParent.html', firstName=current_user.firstName, lastName=current_user.lastName, profession=current_user.profession)

@behaviour_blueprint.route('/addBehaviour/<id_student>')
@login_required
def addBehaviour(id_student):
    # Fetch details about the student using student_id if needed
    
    return render_template(
        'teacher/addBehaviour.html', 
        firstName=current_user.firstName, 
        lastName=current_user.lastName, 
        profession=current_user.profession, 
    )
@behaviour_blueprint.route('/addBehavior/<int:id_student>', methods=['POST'])
@login_required
def add_behavior(id_student):
    """
    Route for adding a behavior for a specific student.
    """
    # Retrieve form data from the request
    behavior_type = request.form.get('behaviorType')
    behavior_note = request.form.get('behaviorNote')
    
    

    # Pass student_id, user_id, and other data to the controller
    response, status_code = add_behaviour(id_student, behavior_type, behavior_note, current_user.id)

    # Return a JSON response using jsonify and pass the status code
    return jsonify(response), status_code
@behaviour_blueprint.route('/getStudents/<class_id>', methods=['GET'])
@login_required
def getStudents(class_id):
    students = get_students_from_db(class_id)
    
    return jsonify(students)

