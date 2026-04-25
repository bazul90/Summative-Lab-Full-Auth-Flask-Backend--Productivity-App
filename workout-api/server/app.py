from flask import Flask, jsonify
from server.extensions import db, migrate, ma
from server.config import config
from server.models import Exercise, Workout, WorkoutExercise
from server.routes.workout_routes import workout_bp
from server.routes.exercise_routes import exercise_bp
from server.routes.workout_exercise_routes import workout_exercise_bp


def create_app(config_name='development'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)

    app.register_blueprint(workout_bp)
    app.register_blueprint(exercise_bp)
    app.register_blueprint(workout_exercise_bp)

    @app.route('/health')
    def health():
        return jsonify({'status': 'healthy'}), 200

    return app


app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=5000)