from flask import Blueprint, render_template, jsonify
from flask_login import login_required, current_user
from controllers.grades_controller import *
from datetime import datetime, timedelta


grades_blueprint = Blueprint('grades', __name__)

@grades_blueprint.route('/grades')
@login_required
def grades():
    return render_template('grades.html', username=current_user.username, profession=current_user.profession)
