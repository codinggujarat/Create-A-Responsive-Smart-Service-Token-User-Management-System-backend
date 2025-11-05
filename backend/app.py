from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS
from flask_mail import Mail
from flask_jwt_extended import JWTManager
from backend.config import Config
from backend.models import db
from backend.routes.user_routes import user_bp
from backend.routes.admin_routes import admin_bp
from backend.services.scheduler_service import start_scheduler
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_app():
    app = Flask(__name__, static_folder='../frontend/dist', static_url_path='')
    app.config.from_object(Config)
    
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    db.init_app(app)
    mail = Mail(app)
    jwt = JWTManager(app)
    
    app.register_blueprint(user_bp)
    app.register_blueprint(admin_bp)
    
    with app.app_context():
        db.create_all()
        logger.info("Database tables created successfully")
    
    start_scheduler(app, mail)
    
    @app.route('/health')
    def health():
        return {'status': 'healthy'}, 200
    
    @app.route('/api/health')
    def api_health():
        return jsonify({'status': 'healthy'}), 200
    
    @app.route('/')
    def index():
        return send_from_directory(app.static_folder, 'index.html')
    
    @app.errorhandler(404)
    def not_found(e):
        path = str(e).split("'")[1] if "'" in str(e) else ""
        if path.startswith('/api/'):
            return {'error': 'API endpoint not found'}, 404
        if path and not path.startswith('/'):
            path = '/' + path
        file_path = path[1:] if path.startswith('/') else path
        if file_path and os.path.exists(os.path.join(app.static_folder, file_path)):
            return send_from_directory(app.static_folder, file_path)
        return send_from_directory(app.static_folder, 'index.html')
    
    return app

# Create an app instance for gunicorn
app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)