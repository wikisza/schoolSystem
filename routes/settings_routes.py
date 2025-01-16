from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from controllers.settings_controller import update_user_data

settings_blueprint = Blueprint('settings', __name__)

@settings_blueprint.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        email = request.form['email']
        phoneNumber = request.form['phoneNumber']
        address = request.form['address']
        password = request.form['password']
        confirmPassword = request.form['confirmPassword']

        # Wywołanie funkcji do zaktualizowania danych
        if update_user_data(current_user.id, firstName, lastName, email, phoneNumber, address, password, confirmPassword):
            flash("Dane zostały zaktualizowane", "success")
            return redirect(url_for('settings.settings'))
        else:
            flash("Wystąpił błąd. Spróbuj ponownie.", "danger")

    # Renderowanie widoku dla GET
    return render_template('settings.html', 
                           firstName=current_user.firstName,
                           lastName=current_user.lastName,
                           email=current_user.email,
                           phoneNumber=current_user.phoneNumber,
                           address=current_user.address)

# Dodaj tę trasę poniżej, żeby rozwiązać błąd
@settings_blueprint.route('/settings/update_settings', methods=['POST'])
@login_required
def update_settings():
    # Ta funkcja może być zbędna, ponieważ logika już jest w `settings`
    # Jeśli jednak chcesz, możesz dodać bardziej zaawansowaną logikę w tym miejscu
    return redirect(url_for('settings.settings'))
