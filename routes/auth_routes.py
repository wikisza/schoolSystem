from flask import Blueprint, render_template, request, redirect, flash, url_for
from controllers.auth_controller import authenticate, register_user
from flask_login import login_required, logout_user
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