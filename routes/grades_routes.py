from flask import Blueprint, render_template, jsonify, request
from flask_login import login_required, current_user
from controllers.grades_controller import *
from datetime import datetime, timedelta

grades_blueprint = Blueprint('grades', __name__)

# Strona główna z ocenami dla zalogowanego użytkownika
@grades_blueprint.route('/grades')
@login_required
def grades():
    return render_template('grades.html', firstName=current_user.firstName, lastName=current_user.lastName, profession=current_user.profession)

# Widok ocen nauczyciela
@grades_blueprint.route('/gradesTeacher', methods=['GET'])
@login_required
def gradesTeacher():
    class_id = request.args.get('id_class')
    grades = get_class_grades(class_id)  # Pobierz oceny
    return render_template('teacher/gradesTeacher.html', grades=grades, firstName=current_user.firstName, lastName=current_user.lastName, profession=current_user.profession)


@grades_blueprint.route('/addNewGrade', methods=['POST'])
def add_grade_route():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    data = request.get_json()

    id_student = data['id_student']
    id_subject = data['id_subject']
    value = data['value']
    comment = data['comment']
    date = data['date']
    id_category = data['id_category']
    id_teacher = data['id_teacher']

    result = add_grade(id_student, id_subject, value, comment, date, id_category, id_teacher)
    return result

@grades_blueprint.route('/getGradesForClass', methods=['GET'])
@login_required
def gradesTgetGradesForClass():
    class_id = request.args.get('id_class')  # Pobierz ID klasy z parametrów URL
    if not class_id:
        return jsonify({'error': 'ID klasy nie zostało podane'}), 400

    # Pobierz oceny dla danej klasy
    grades = get_class_grades(class_id)  # Funkcja, która zwraca dane ocen w formacie słownika
    return jsonify(grades)

@grades_blueprint.route('/gradesStudent')
@login_required
def gradesStudent():
    student_id = get_student_id(current_user.id)  # Pobierz id_student
    grades = get_student_grades(student_id)  # Pobierz oceny
    student_name = f"{current_user.firstName} {current_user.lastName}"  # Imię i nazwisko ucznia
    return render_template('student/gradesStudent.html', grades=grades, student_name=student_name,firstName=current_user.firstName, lastName=current_user.lastName, profession=current_user.profession)

# Widok ocen rodzica
@grades_blueprint.route('/gradesParent')
@login_required
def gradesParent():
    parent_id = get_parent_id(current_user.id)  # Pobierz id_parent
    children_grades = get_children_grades(parent_id)  # Pobierz oceny dzieci
    return render_template('parent/gradesParent.html', children_grades=children_grades, firstName=current_user.firstName, lastName=current_user.lastName, profession=current_user.profession)

# Strona do dodawania ocen
@grades_blueprint.route('/addGrades')
def addGrades_route():
    student_id = get_student_id(current_user.id)  # Pobierz id_student
    grades = get_student_grades(student_id)  # Pobierz oceny
    return render_template('teacher/addGrades.html',grades=grades, firstName=current_user.firstName, lastName=current_user.lastName, profession=current_user.profession)


