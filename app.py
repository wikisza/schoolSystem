from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from config import Config
from routes.auth_routes import auth_blueprint
from routes.index_routes import index_blueprint
from routes.classSchedule_routes import classSchedule_blueprint
from routes.grades_routes import grades_blueprint
from routes.attendance_routes import attendance_blueprint
from routes.messages_routes import messages_blueprint,register_message_socketio
from routes.settings_routes import settings_blueprint
from routes.classHandler_routes import classHandler_blueprint
from routes.behaviour_routes import behaviour_blueprint
from controllers.auth_controller import load_user
from flask_socketio import SocketIO  

app = Flask(__name__)
app.config.from_object(Config)

app.register_blueprint(auth_blueprint)
app.register_blueprint(index_blueprint)
app.register_blueprint(classSchedule_blueprint)
app.register_blueprint(grades_blueprint)
app.register_blueprint(attendance_blueprint)
app.register_blueprint(messages_blueprint)
app.register_blueprint(behaviour_blueprint)
app.register_blueprint(settings_blueprint)
app.register_blueprint(classHandler_blueprint)

bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.user_loader(load_user)
login_manager.login_view = 'auth.login'

socketio = SocketIO(app)
register_message_socketio(socketio)  
if __name__ == '__main__':
    socketio.run(app, debug=True)