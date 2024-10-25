from flask import Blueprint, render_template, request, redirect, flash, url_for
from controllers.auth_controller import authenticate, register_user
from flask_login import login_required, logout_user

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
        if register_user(username, password, profession):
            return redirect(url_for('auth.login'))
        else:
            flash('Login już zajęty.')
            return redirect(url_for('auth.register'))
    return render_template('register.html')

@auth_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))