from flask import Blueprint, render_template, jsonify, request
from flask_login import login_required, current_user
from controllers.attendance_controller import get_classes, get_subjects, get_attendance_data, get_lessons, save_attendance_changes

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

    lessons, students = get_lessons(class_id, subject_id)
    return jsonify({'lessons': lessons, 'students': students})


@attendance_blueprint.route('/save-attendance', methods=['POST'])
@login_required
def save_attendance():
    data = request.json.get('attendance')
    if not data:
        return jsonify({'error': 'No attendance data provided'}), 400

    # Zapisz dane do bazy
    result = save_attendance_changes(data)
    return jsonify(result)
