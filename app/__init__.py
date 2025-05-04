from flask import Flask
from flask_login import LoginManager
from app.config import Config
from app.models.user import get_user_by_id
import os
from dotenv import load_dotenv

login_manager = LoginManager()

def create_app():
    # Load environment variables
    load_dotenv()
    
    app = Flask(__name__)
    app.config.from_object(Config)
    
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    
    @login_manager.user_loader
    def load_user(user_id):
        return get_user_by_id(user_id)
    
    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.main import main_bp
    from app.routes.doctors import doctors_bp
    from app.routes.users import users_bp
    from app.routes.patients import patients_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(doctors_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(patients_bp)
    
    return app 