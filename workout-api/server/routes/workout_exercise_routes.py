from flask import Blueprint, request, jsonify
from server.models import Workout, Exercise, WorkoutExercise
from server.schemas import WorkoutExerciseSchema
from server.extensions import db

workout_exercise_bp = Blueprint('workout_exercise_bp', __name__)
workout_exercise_schema = WorkoutExerciseSchema()


@workout_exercise_bp.route('/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises', methods=['POST'])
def add_exercise_to_workout(workout_id, exercise_id):
    workout = Workout.query.get_or_404(workout_id)
    exercise = Exercise.query.get_or_404(exercise_id)

    json_data = request.get_json() or {}
    json_data['workout_id'] = workout_id
    json_data['exercise_id'] = exercise_id

    try:
        data = workout_exercise_schema.load(json_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

    workout_exercise = WorkoutExercise(**data)
    db.session.add(workout_exercise)
    db.session.commit()

    return jsonify(workout_exercise_schema.dump(workout_exercise)), 201