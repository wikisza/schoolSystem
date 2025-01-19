from flask import Blueprint, render_template, jsonify, request
from flask_login import login_required, current_user
from controllers.attendance_controller import *

from controllers.classSchedule_controller import get_student_class

attendance_blueprint = Blueprint('attendance', __name__)

@attendance_blueprint.route('/attendance')
@login_required
def attendance():
    return render_template('attendance.html', firstName=current_user.firstName, lastName=current_user.lastName, profession=current_user.profession)

@attendance_blueprint.route('/attendanceStudent')
@login_required
def attendanceStudent():
    return render_template('student/attendanceStudent.html', firstName=current_user.firstName, lastName=current_user.lastName, profession=current_user.profession)

@attendance_blueprint.route('/attendanceParent')
@login_required
def attendanceParent():
    return render_template('parent/attendanceParent.html', firstName=current_user.firstName, lastName=current_user.lastName, profession=current_user.profession)

@attendance_blueprint.route('/attendanceTeacher')
@login_required
def attendanceTeacher():
    classes = get_classes()
    subjects = get_subjects()

    class_id = request.args.get('class_id')
    subject_id = request.args.get('subject_id')

    attendance_data = []
    if class_id and subject_id:
        attendance_data = get_attendance_data(class_id, subject_id)

    return render_template('teacher/attendanceTeacher.html', attendance_data=attendance_data, classes=classes, subjects=subjects,firstName=current_user.firstName, lastName=current_user.lastName, profession=current_user.profession)

# Zmieniona nazwa widoku na fetch_lessons_view
@attendance_blueprint.route('/get-lessons', methods=['POST'])
def fetch_lessons_view():
    class_id = request.json.get('classId')
    subject_id = request.json.get('subjectId')

    if not class_id or not subject_id:
        return jsonify({'error': 'classId and subjectId are required'}), 400

    lessons, students = get_lessons(int(class_id), int(subject_id))
    existing_attendance = get_existing_attendance(int(class_id), int(subject_id))
    
    # Upewnijmy się, że klucze i wartości w existing_attendance są typu str
    existing_attendance_str_keys = {
        str(key): {
            str(inner_key): value
            for inner_key, value in inner_dict.items()
        } for key, inner_dict in existing_attendance.items()
    }

    return jsonify({
        'lessons': lessons,
        'students': students,
        'attendance': existing_attendance_str_keys
    })

@attendance_blueprint.route('/save-attendance', methods=['POST'])
@login_required
def save_attendance():
    data = request.json.get('attendance')
    if not data:
        return jsonify({'error': 'No attendance data provided'}), 400

    try:
        # Zapisz dane do bazy
        result = save_attendance_changes(data)
        return jsonify(result)
    except sqlite3.OperationalError as e:
        return jsonify({'error': 'Database is locked, please try again later.'}), 500

@attendance_blueprint.route('/getThisStudentLessonsAndPresences', methods=['GET'])
def getThisStudentLessonsAndPresences_routes():
    id_user = current_user.id
    id_class = get_student_class(id_user)
    id_student = get_student_id(id_user)  # Zakładamy, że jest funkcja get_student_id

    classes = get_lessons_with_presence(id_class, id_student)

    return classes



@attendance_blueprint.route('/get_logged_in_parent', methods=['GET'])
@login_required
def get_logged_in_parent():
    user_id = current_user.id
    parent_id = get_parent_id(user_id)
    if parent_id:
        return jsonify({"parent_id": parent_id})
    else:
        return jsonify({"message": "No parent found for this user"}), 404

@attendance_blueprint.route('/get_children', methods=['GET'])
@login_required
def get_children():
    parent_id = request.args.get('parent_id')
    if not parent_id:
        return jsonify({"message": "Parent ID is required"}), 400

    children = get_children_by_parent_id(parent_id)
    if children:
        return jsonify({"children": children})
    else:
        return jsonify({"message": "No children found for this parent"}), 404


############
@attendance_blueprint.route('/get_selected_child_lessons', methods=['GET'])
@login_required
def get_selected_child_lessons():
    child_id = request.args.get('child_id')
    if not child_id:
        return jsonify({"error": "Child ID is required"}), 400

    # Pobierz klasę dziecka na podstawie ID ucznia
    id_class = get_student_class_by_id(child_id)
    if not id_class:
        return jsonify({"error": "Class not found for this child"}), 404

    # Pobierz lekcje i obecności dla danego dziecka
    lessons_with_presence = get_lessons_with_presence(id_class, child_id)
    return lessons_with_presence


##

@attendance_blueprint.route('/update-attendance-status', methods=['POST'])
@login_required
def update_attendance_status():
    data = request.json
    lesson_id = data.get('lessonId')
    student_id = data.get('studentId')
    new_status = data.get('newStatus')  # Zawiera status z powodem

    if not (lesson_id and student_id and new_status):
        return jsonify({'success': False, 'message': 'Brak wymaganych danych.'}), 400

    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE presences
            SET status = ?
            WHERE id_lesson = ? AND id_student = ?
        ''', (new_status, lesson_id, student_id))
        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': 'Status zaktualizowany pomyślnie.'})
    except sqlite3.Error as e:
        print(f"Błąd bazy danych: {e}")
        return jsonify({'success': False, 'message': 'Wystąpił błąd bazy danych.'}), 500
