from flask import Blueprint, render_template, jsonify
from flask_login import login_required, current_user
from controllers.classSchedule_controller import *
from datetime import datetime, timedelta


classSchedule_blueprint = Blueprint('classSchedule', __name__)

@classSchedule_blueprint.route('/classSchedule')
@login_required
def classSchedule():
    return render_template('classSchedule.html', username=current_user.username, profession=current_user.profession)
