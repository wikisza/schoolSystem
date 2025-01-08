from flask import Blueprint, render_template, jsonify
from flask_login import login_required, current_user
from controllers.grades_controller import *
from models.user import User
from datetime import datetime, timedelta
from controllers.classHandler_controller import get_students_for_class_leader
from controllers.classHandler_controller import is_class_leader

classHandler_blueprint = Blueprint('classHandler', __name__)

# Test dla uzytkownikow
# users = [
#     User(1, "jdoe", "password", "teacher", "jdoe@example.com", "John", "Doe", "123456789", "123 Main St"),
#     User(2, "asmith", "password", "student", "asmith@example.com", "Anna", "Smith", "987654321", "456 Elm St"),
#     User(3, "bwilliams", "password", "admin", "bwilliams@example.com", "Brian", "Williams", "456123789", "789 Oak St"),
# ]

@classHandler_blueprint.route('/classHandler')
@login_required
def classHandler():
    is_leader = is_class_leader(current_user.id)  # Czy użytkownik jest wychowawcą
    students_for_classes = (
        get_students_for_class_leader(current_user.id) if is_leader else {}
    )
    return render_template(
        'teacher/classHandler.html',
        firstName=current_user.firstName,
        lastName=current_user.lastName,
        profession=current_user.profession,
        is_leader=is_leader,  # Nowa zmienna
        students_for_classes=students_for_classes
    )
