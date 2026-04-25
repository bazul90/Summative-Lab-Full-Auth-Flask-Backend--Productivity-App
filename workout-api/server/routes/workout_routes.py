from flask import Blueprint, request, jsonify
from server.models import Workout
from server.schemas import WorkoutSchema
from server.extensions import db

workout_bp = Blueprint('workout_bp', __name__, url_prefix='/workouts')

workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)


@workout_bp.route('', methods=['GET'])
def get_workouts():
    workouts = Workout.query.all()
    return jsonify(workouts_schema.dump(workouts)), 200


@workout_bp.route('/<int:workout_id>', methods=['GET'])
def get_workout(workout_id):
    workout = Workout.query.get_or_404(workout_id)
    return jsonify(workout_schema.dump(workout)), 200


@workout_bp.route('', methods=['POST'])
def create_workout():
    json_data = request.get_json()
    if not json_data:
        return jsonify({'error': 'No input data provided'}), 400

    try:
        data = workout_schema.load(json_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

    workout = Workout(**data)
    db.session.add(workout)
    db.session.commit()

    return jsonify(workout_schema.dump(workout)), 201


@workout_bp.route('/<int:workout_id>', methods=['DELETE'])
def delete_workout(workout_id):
    workout = Workout.query.get_or_404(workout_id)
    db.session.delete(workout)
    db.session.commit()
    return '', 204