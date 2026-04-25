from flask import Blueprint, request, jsonify
from server.models import Exercise, WorkoutExercise, Workout
from server.schemas import ExerciseSchema
from server.extensions import db

exercise_bp = Blueprint('exercise_bp', __name__, url_prefix='/exercises')
exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)


@exercise_bp.route('', methods=['GET'])
def get_exercises():
    exercises = Exercise.query.all()
    return jsonify(exercises_schema.dump(exercises)), 200


@exercise_bp.route('/<int:exercise_id>', methods=['GET'])
def get_exercise(exercise_id):
    exercise = Exercise.query.get_or_404(exercise_id)
    return jsonify(exercise_schema.dump(exercise)), 200


@exercise_bp.route('', methods=['POST'])
def create_exercise():
    json_data = request.get_json()
    if not json_data:
        return jsonify({'error': 'No input data provided'}), 400

    try:
        data = exercise_schema.load(json_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

    exercise = Exercise(**data)
    db.session.add(exercise)
    db.session.commit()

    return jsonify(exercise_schema.dump(exercise)), 201


@exercise_bp.route('/<int:exercise_id>', methods=['DELETE'])
def delete_exercise(exercise_id):
    exercise = Exercise.query.get_or_404(exercise_id)
    db.session.delete(exercise)
    db.session.commit()
    return '', 204