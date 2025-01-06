from flask import Blueprint, render_template, jsonify
from flask_login import login_required, current_user
from controllers.settings_controller import *
from datetime import datetime, timedelta


settings_blueprint = Blueprint('settings', __name__)

@settings_blueprint.route('/settings')
@login_required
def settings():
    return render_template('settings.html', firstName=current_user.firstName, lastName=current_user.lastName, profession=current_user.profession)
