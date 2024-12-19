from flask import Blueprint, render_template, request, redirect, flash, url_for,jsonify
from controllers.auth_controller import authenticate, register_user, getUsersData
from flask_login import login_required, logout_user, current_user
from routes.index_routes import administrationView_route

auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if authenticate(username, password):
            return redirect(url_for('index.index'))
        else:
            flash('Nieprawidłowy login lub hasło.')
    return render_template('login.html')


@auth_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        profession = request.form['profession']
        email = request.form['email']
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        phoneNumber = request.form['phoneNumber']
        address = request.form['address']
        if register_user(username, password, profession, email, firstName, lastName, phoneNumber, address):
            return redirect(url_for('index.administrationView_route'))
        else:
            flash('Login już zajęty.')
            return redirect(url_for('auth.register'))
    return render_template('register.html')

@auth_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))



#ścieżki do listy pracowników i uczniów

@auth_blueprint.route('/listOfUsers')
@login_required
def listOfUsers():
    return render_template('administration/listOfUsers.html', firstName=current_user.firstName, lastName=current_user.lastName, profession=current_user.profession)

@auth_blueprint.route('/getUsersData', methods=['POST'])
def getUsersData_route():
    selectId = request.form.get('selectId')
    users_data = getUsersData(selectId)

    return jsonify(users_data)
