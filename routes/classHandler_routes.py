from flask import Blueprint, render_template, jsonify
from flask_login import login_required, current_user
from controllers.grades_controller import *
from models.user import User
from datetime import datetime, timedelta
from controllers.classHandler_controller import get_students_for_class_leader
from controllers.classHandler_controller import is_class_leader
from flask import request, redirect, url_for
from controllers.classHandler_controller import get_student_by_id, update_student_data
from controllers.classHandler_controller import get_all_parents

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

    # Debugowanie: Sprawdzenie zawartości students_for_classes
    print(f"students_for_classes: {students_for_classes}")

    return render_template(
        'teacher/classHandler.html',
        firstName=current_user.firstName,
        lastName=current_user.lastName,
        profession=current_user.profession,
        is_leader=is_leader,  # Nowa zmienna
        students_for_classes=students_for_classes
    )


@classHandler_blueprint.route('/edit_student', methods=['GET'])
@login_required
def edit_student():
    student_id = request.args.get('student_id')

    if not student_id:
        return "Student ID is required", 400

    student = get_student_by_id(student_id)
    if not student:
        return "Student not found", 404

    parents = get_all_parents()  # Pobranie listy rodziców
    return render_template('teacher/edit_student.html', student=student, parents=parents)



@classHandler_blueprint.route('/update_student', methods=['POST'])
@login_required
def update_student():
    student_id = request.form.get('student_id')
    if not student_id:
        return "Student ID is required", 400

    parent_id = request.form.get('parent_id')  # Pobierz ID rodzica z formularza
    if not parent_id:
        parent_id = None  # Jeśli brak wyboru, ustaw jako None

    updated_data = {
        "firstName": request.form.get('firstName'),
        "lastName": request.form.get('lastName'),
        "email": request.form.get('email'),
        "phoneNumber": request.form.get('phoneNumber'),
        "address": request.form.get('address'),
        "parent_id": parent_id,  # Dodanie ID rodzica
    }

    success = update_student_data(student_id, updated_data)
    if not success:
        return "Failed to update student data", 500

    return redirect(url_for('classHandler.classHandler'))
