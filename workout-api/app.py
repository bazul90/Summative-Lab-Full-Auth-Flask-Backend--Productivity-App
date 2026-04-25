import os
from flask import Flask
from config import Config
from models import db
from routes import bp
from flask_migrate import Migrate

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate = Migrate(app, db)

    app.register_blueprint(bp, url_prefix='/api')

    @app.shell_context_processor
    def make_shell_context():
        return {'db': db, 'Workout': Workout, 'Exercise': Exercise}

    from models import Workout, Exercise
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
