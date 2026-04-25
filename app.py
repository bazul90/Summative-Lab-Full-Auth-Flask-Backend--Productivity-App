from flask import Flask, jsonify
from flask_cors import CORS
from config import Config
from models import db, bcrypt
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    jwt = JWTManager(app)
    migrate = Migrate(app, db)

    # Enable CORS for all routes
    CORS(app)

    # Register blueprints
    from routes.auth_routes import auth_bp
    from routes.resource_routes import resource_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(resource_bp, url_prefix='/api')

    @app.route('/health', methods=['GET'])
    def health_check():
        return jsonify({'status': 'healthy'}), 200

    return app

# Create app instance for running directly
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
