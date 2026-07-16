from flask import Flask
from config import Config
from app.models import db
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from app.models import User
import os

bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Ensure upload directory exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    from app.services.copilot_engine import CitizenCopilotEngine
    print("🤖 Pre-warming Citizen Copilot Engine and FAISS Index...")
    app.extensions['copilot_engine'] = CitizenCopilotEngine(
        gemini_api_key=app.config.get('GEMINI_API_KEY')
    )

    with app.app_context():
        # Import blueprints
        from app.main import main_bp
        from app.auth import auth_bp
        from app.dashboard import dashboard_bp
        from app.engine import engine_bp
        from app.network import network_bp
        from app.currency import currency_bp
        from app.police import police_bp
        from app.copilot import copilot_bp
        
        
        # Register blueprints
        app.register_blueprint(main_bp)
        app.register_blueprint(auth_bp)
        app.register_blueprint(dashboard_bp)
        app.register_blueprint(engine_bp)
        app.register_blueprint(network_bp)
        app.register_blueprint(currency_bp)
        app.register_blueprint(police_bp)
        app.register_blueprint(copilot_bp)
        
        db.create_all()
    return app
