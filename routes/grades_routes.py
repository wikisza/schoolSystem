from flask import Blueprint, render_template, jsonify
from flask_login import login_required, current_user
from controllers.grades_controller import *
from datetime import datetime, timedelta

grades_blueprint = Blueprint('grades', __name__)

# Strona główna z ocenami dla zalogowanego użytkownika
@grades_blueprint.route('/grades')
@login_required
def grades():
    return render_template('grades.html', username=current_user.username, profession=current_user.profession)

# Widok ocen nauczyciela
@grades_blueprint.route('/gradesTeacher')
@login_required
def gradesTeacher():
    return render_template('teacher/gradesTeacher.html', username=current_user.username, profession=current_user.profession)

@grades_blueprint.route('/gradesStudent')
@login_required
def gradesStudent():
    student_id = get_student_id(current_user.id)  # Pobierz id_student
    grades = get_student_grades(student_id)  # Pobierz oceny
    student_name = f"{current_user.firstName} {current_user.lastName}"  # Imię i nazwisko ucznia
    return render_template('student/gradesStudent.html', grades=grades, student_name=student_name)

# Widok ocen rodzica
@grades_blueprint.route('/gradesParent')
@login_required
def gradesParent():
    return render_template('parent/gradesParent.html', username=current_user.username, profession=current_user.profession)

# Strona do dodawania ocen
@grades_blueprint.route('/addGrades')
def addGrades_route():
    return render_template('teacher/addGrades.html', username=current_user.username, profession=current_user.profession)
