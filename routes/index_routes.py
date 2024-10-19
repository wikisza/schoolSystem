from flask import Blueprint, render_template, jsonify
from flask_login import login_required, current_user
from controllers.index_controller import get_reservations, get_old_reservations
from datetime import datetime, timedelta


index_blueprint = Blueprint('index', __name__)

@index_blueprint.route('/')
@login_required
def index():
    return render_template('index.html', username=current_user.username)

'''
@index_blueprint.route('/get_reservations')
def get_reservations_route():
    rezerwacje = get_reservations()

    events = []
    for rezerwacja in rezerwacje:

        start_date = datetime.strptime(rezerwacja[1], '%Y-%m-%d')
        end_date = datetime.strptime(rezerwacja[2], '%Y-%m-%d')

        title = str(rezerwacja[0]) + ' - Pokój: ' + str(rezerwacja[3])
        
        end_date += timedelta(days=1)
        events.append({
            'title': title,
            'start': start_date.strftime('%Y-%m-%d'),  
            'end': end_date.strftime('%Y-%m-%d'),
            'allDay': True  
        })

    return jsonify(events)

@index_blueprint.route('/get_old_reservations')
def get_old_reservation_route():
    stare = get_old_reservations()

    wydarzenia = []
    for stara in stare:

        start_date = datetime.strptime(stara[1], '%Y-%m-%d')
        end_date = datetime.strptime(stara[2], '%Y-%m-%d')

        title = str(stara[0]) + ' - Pokój: ' + str(stara[3])
        end_date += timedelta(days=1)
        wydarzenia.append({
            'title': title,
            'start': start_date.strftime('%Y-%m-%d'), 
            'end': end_date.strftime('%Y-%m-%d'),
            'allDay': True 
        })

    return jsonify(wydarzenia)

    '''