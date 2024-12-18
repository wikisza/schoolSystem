from flask import Blueprint, render_template, jsonify, request, flash, redirect
from flask_login import login_required, current_user
from controllers.classSchedule_controller import *
from datetime import datetime, timedelta
from controllers.classSchedule_controller import addClass, addGroup, search_items,getClassData, getStudentsInClass, editThisClass, assign_students_to_class

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
    if request.method == 'POST':
        # Obsługa zapisu zmian
        id_class = request.form.get('id_class')
        class_name = request.form.get('class_name')
        id_teacher = request.form.get('id_teacher')
        edit_success = editThisClass(id_class, id_teacher, class_name)

        if edit_success:
            flash("Zmiany zostały zapisane!")
            return redirect('/classManagement')
        else:
            flash("Nie udało się zapisać zmian.")
            return redirect(f'/editThisClass?id={id_class}')

    # Obsługa ładowania danych klasy (GET)
    id_class = request.args.get('id')  # Pobranie ID klasy z parametru URL
    class_data = getClassData(id_class)  # Pobranie danych klasy z bazy danych
    students = getStudentsInClass(id_class)  # Pobranie uczniów w klasie

    return render_template(
        'administration/editClass.html',
        class_data=class_data, 
        students=students,
        firstName=current_user.firstName, 
        lastName=current_user.lastName
    )

@classSchedule_blueprint.route('/getUnassignedStudents', methods=['GET'])
def get_unassigned_students_route():
    unassigned_students = getUnassignedStudents()
    return jsonify(unassigned_students)

@classSchedule_blueprint.route('/assignStudentsToClass', methods=['POST'])
def assign_students_to_class_route():
    data = request.get_json()
    student_ids = data.get('student_ids')
    class_id = data.get('class_id')

    result = assign_students_to_class(data, student_ids, class_id)

    # Obsługa ładowania danych klasy (GET)
    id_class = request.args.get('id')  # Pobranie ID klasy z parametru URL
    class_data = getClassData(id_class)  # Pobranie danych klasy z bazy danych
    students = getStudentsInClass(id_class)

    return render_template(
        'administration/editClass.html',
        class_data=class_data, 
        students=students,
        result=result,
        firstName=current_user.firstName, 
        lastName=current_user.lastName
    )


@classSchedule_blueprint.route('/editThisClass', methods=['GET', 'POST'])
def editThisClass_route():
    id_class = request.form.get('id_class')
    class_name = request.form.get('class_name')
    id_teacher = request.form.get('id_teacher')
    result = editThisClass(id_class, id_teacher, class_name)

@classSchedule_blueprint.route('/search_items', methods=['GET'])
def search_items_route():
    search_query = request.args.get('query')  # Pobranie zapytania z wyszukiwarki
    result = search_items(search_query)

    return result


@classSchedule_blueprint.route('/getTeachersList', methods=['GET'])
def getTeachersList_route():
    return getTeachersList()


