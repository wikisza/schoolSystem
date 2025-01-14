from flask import Blueprint, render_template, jsonify, request, flash, redirect
from flask_login import login_required, current_user
from controllers.classSchedule_controller import *
from datetime import datetime, timedelta
from controllers.classSchedule_controller import addClass, addGroup, search_items,getClassData, getStudentsInClass, editThisClass, get_teachers, assign_students_to_class, get_lessons, getAllClasses, getSubjectsList, addNewSubjectToPlan, get_teacher_lessons, get_id_teacher, get_student_class, SubjectTeacherConnection

classSchedule_blueprint = Blueprint('classSchedule', __name__)

@classSchedule_blueprint.route('/classSchedule')
@login_required
def classSchedule():
    return render_template('classSchedule.html', firstName=current_user.firstName, lastName=current_user.lastName, profession=current_user.profession)

@classSchedule_blueprint.route('/scheduleTeacher')
@login_required
def scheduleTeacher_route():
    return render_template('teacher/scheduleTeacher.html', firstName=current_user.firstName, lastName=current_user.lastName, id_user=current_user.id, profession=current_user.profession)

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

@classSchedule_blueprint.route('/getTeachersList', methods=['GET'])
def get_teachers_list_route():
    teachers = get_teachers()
    return jsonify(teachers)



@classSchedule_blueprint.route('/editThisClass', methods=['POST'])
def editThisClass_route():
    id_class = request.form.get('id_class');  # Pobranie ID klasy z parametru URL
    class_name = request.form.get('class_name')
    id_teacher = request.form.get('id_teacher')

    result = editThisClass(id_class, id_teacher, class_name)
    return render_template('administration/classManagement.html', result=result, firstName=current_user.firstName, lastName=current_user.lastName, profession=current_user.profession)



@classSchedule_blueprint.route('/search_items', methods=['GET'])
def search_items_route():
    search_query = request.args.get('query')  
    result = search_items(search_query)

    return result


@classSchedule_blueprint.route('/getTeachersList', methods=['GET'])
def getTeachersList_route():
    return getTeachersList()




##### POBIERANIE LEKCJI Z BAZY DANYCH


@classSchedule_blueprint.route('/get_lessons', methods=['POST'])
def get_lessons_route():
    data = request.json  
    class_id = data.get('id_class')

    classes = get_lessons(class_id)  

    return classes  

@classSchedule_blueprint.route('/getThisStudentLessons', methods=['GET'])
def getThisStudenLessons_route():
    id_user = current_user.id 

    id_class = get_student_class(id_user)

    classes = get_lessons(id_class)  

    return classes

@classSchedule_blueprint.route('/getAllClasses', methods=['GET'])
def getAllClasses_route():
    result = getAllClasses()
    return result


@classSchedule_blueprint.route('/addingSubjectToPlan')
def addingSubjectToPlan_route():
    return render_template('administration/addingSubjectToPlan.html', firstName=current_user.firstName, lastName=current_user.lastName, profession=current_user.profession)

@classSchedule_blueprint.route('/getSubjectsList', methods=['GET'])
def getSubjectsList_route():
    return getSubjectsList()


@classSchedule_blueprint.route('/addNewSubjectToPlan', methods=['POST'])
def addNewSubjectToPlan_route():

    data = request.json

    if not data:
        return jsonify({"error": "Brak danych w żądaniu."}), 400

    id_class = data.get('id_class')
    id_teacher = data.get('id_teacher')
    id_subject = data.get('id_subject')
    day_of_week = data.get('day_of_week')
    start_time = data.get('start_time')
    room_number = data.get('room_number')
    exact_date = data.get('exact_date')
    semester_start = data.get('semester_start')
    semester_end = data.get('semester_end')


    start_dt = datetime.strptime(start_time, '%H:%M')
    end_dt = start_dt + timedelta(minutes=45)
    stime = start_dt.strftime('%H:%M:%S')
    end_time = end_dt.strftime('%H:%M:%S')

    try:
            
        # Konwersja day_of_week na int (jeśli podano)
        if day_of_week is not None:
            try:
                day_of_week = int(day_of_week)  # Konwersja na int
                if not (0 <= day_of_week <= 5):  # Walidacja zakresu
                    raise ValueError("day_of_week must be an integer between 0 (Monday) and 6 (Sunday).")
            except ValueError:
                raise ValueError("day_of_week must be an integer.")


        # Wywołanie funkcji dodawania zajęć
        result = addNewSubjectToPlan(
            id_class, id_teacher, id_subject,room_number, stime, end_time, day_of_week,
            exact_date, semester_start, semester_end
        )

        return jsonify(result)

    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400

    except Exception as e:
        return jsonify({"error": "An unexpected error occurred: " + str(e)}), 500


@classSchedule_blueprint.route('/getTeacherLessons', methods=['GET'])
def get_teacher_lessons_route():

    user_id = current_user.id 

    teacher_id = get_id_teacher(user_id)

    lessons = get_teacher_lessons(teacher_id)  

    return lessons


@classSchedule_blueprint.route('/updateSubjectTeacherConnection', methods=['POST'])
def updateSubjectTeacherConnection_route():
    data = request.json

    if not data:
        return jsonify({"error": "Brak danych w żądaniu."}), 400

    id_teacher = data.get('id_teacher')
    id_subject = data.get('id_subject')

    
    try:
        result = SubjectTeacherConnection(id_subject, id_teacher)

        return result

    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400

    except Exception as e:
        return jsonify({"error": "An unexpected error occurred: " + str(e)}), 500

