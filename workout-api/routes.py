from flask import Blueprint, request, jsonify, abort
from models import db, Workout, Exercise, workout_exercise
from schemas import WorkoutSchema, ExerciseSchema, WorkoutExerciseSchema
from datetime import datetime

bp = Blueprint('api', __name__)

workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)
exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)
workout_exercise_schema = WorkoutExerciseSchema()


# ---- Workout Endpoints ----

@bp.route('/workouts', methods=['GET'])
def get_workouts():
    """Get all workouts."""
    expand = request.args.get('expand', 'false').lower() == 'true'
    workouts = Workout.query.order_by(Workout.date.desc()).all()
    if expand:
        return jsonify(workouts_schema.dump(workouts))
    # Return minimal representation
    result = [{
        'id': w.id,
        'name': w.name,
        'description': w.description,
        'date': w.date.isoformat() if w.date else None,
        'duration': w.duration,
        'exercise_count': len(w.exercises)
    } for w in workouts]
    return jsonify(result)


@bp.route('/workouts/<int:workout_id>', methods=['GET'])
def get_workout(workout_id):
    """Get a single workout by ID."""
    expand = request.args.get('expand', 'false').lower() == 'true'
    workout = Workout.query.get_or_404(workout_id)
    if expand:
        return jsonify(workout_schema.dump(workout))
    result = {
        'id': workout.id,
        'name': workout.name,
        'description': workout.description,
        'date': workout.date.isoformat() if workout.date else None,
        'duration': workout.duration,
        'exercises': exercises_schema.dump(workout.exercises)
    }
    return jsonify(result)


@bp.route('/workouts', methods=['POST'])
def create_workout():
    """Create a new workout."""
    data = request.get_json()
    if not data:
        abort(400, description="Request body must be JSON")

    # Validate using schema
    errors = workout_schema.validate(data)
    if errors:
        abort(400, description=errors)

    # Check for unique name constraint
    existing = Workout.query.filter_by(name=data['name'].strip()).first()
    if existing:
        abort(400, description=f"Workout with name '{data['name']}' already exists")

    workout, exercise_ids = workout_schema.load(data)
    workout.validate()

    # Associate exercises if provided
    if exercise_ids:
        for eid in exercise_ids:
            exercise = Exercise.query.get(eid)
            if not exercise:
                abort(400, description=f"Exercise with id {eid} does not exist")
            if exercise not in workout.exercises:
                workout.exercises.append(exercise)

    db.session.add(workout)
    db.session.commit()
    return jsonify(workout_schema.dump(workout)), 201


@bp.route('/workouts/<int:workout_id>', methods=['DELETE'])
def delete_workout(workout_id):
    """Delete a workout."""
    workout = Workout.query.get_or_404(workout_id)
    db.session.delete(workout)
    db.session.commit()
    return jsonify({'message': f'Workout "{workout.name}" deleted successfully'}), 200


# ---- Exercise Endpoints ----

@bp.route('/exercises', methods=['GET'])
def get_exercises():
    """Get all exercises."""
    exercises = Exercise.query.order_by(Exercise.name).all()
    return jsonify(exercises_schema.dump(exercises))


@bp.route('/exercises/<int:exercise_id>', methods=['GET'])
def get_exercise(exercise_id):
    """Get a single exercise by ID."""
    exercise = Exercise.query.get_or_404(exercise_id)
    result = exercise_schema.dump(exercise)
    result['workout_ids'] = [w.id for w in exercise.workouts.all()]
    return jsonify(result)


@bp.route('/exercises', methods=['POST'])
def create_exercise():
    """Create a new exercise."""
    data = request.get_json()
    if not data:
        abort(400, description="Request body must be JSON")

    errors = exercise_schema.validate(data)
    if errors:
        abort(400, description=errors)

    existing = Exercise.query.filter_by(name=data['name'].strip()).first()
    if existing:
        abort(400, description=f"Exercise with name '{data['name']}' already exists")

    exercise = exercise_schema.load(data)
    exercise.validate()

    db.session.add(exercise)
    db.session.commit()
    return jsonify(exercise_schema.dump(exercise)), 201


@bp.route('/exercises/<int:exercise_id>', methods=['DELETE'])
def delete_exercise(exercise_id):
    """Delete an exercise."""
    exercise = Exercise.query.get_or_404(exercise_id)
    db.session.delete(exercise)
    db.session.commit()
    return jsonify({'message': f'Exercise "{exercise.name}" deleted successfully'}), 200


# ---- Workout-Exercise Association Endpoints ----

@bp.route('/workouts/<int:workout_id>/exercises', methods=['POST'])
def add_exercise_to_workout(workout_id):
    """Add an exercise to a workout with sets/reps or duration."""
    workout = Workout.query.get_or_404(workout_id)
    data = request.get_json()
    if not data:
        abort(400, description="Request body must be JSON")

    # Validate the association data
    assoc_data = workout_exercise_schema.load(data)
    exercise_id = assoc_data['exercise_id']
    sets = assoc_data.get('sets', 3)
    reps = assoc_data.get('reps')
    duration = assoc_data.get('duration')

    exercise = Exercise.query.get(exercise_id)
    if not exercise:
        abort(400, description=f"Exercise with id {exercise_id} does not exist")

    # Check if already associated
    existing_assoc = db.session.query(workout_exercise).filter_by(
        workout_id=workout_id, exercise_id=exercise_id
    ).first()
    if existing_assoc:
        abort(400, description=f"Exercise '{exercise.name}' is already in workout '{workout.name}'")

    # Add the exercise to the workout
    workout.exercises.append(exercise)
    db.session.flush()  # To get the association recorded

    # Update the association with sets/reps/duration
    db.session.execute(
        workout_exercise.update().
        where((workout_exercise.c.workout_id == workout_id) & (workout_exercise.c.exercise_id == exercise_id)).
        values(sets=sets, reps=reps, duration=duration)
    )

    db.session.commit()
    result = {
        'message': f"Exercise '{exercise.name}' added to workout '{workout.name}'",
        'workout_id': workout_id,
        'exercise_id': exercise_id,
        'sets': sets,
        'reps': reps,
        'duration': duration
    }
    return jsonify(result), 201


@bp.route('/workouts/<int:workout_id>/exercises', methods=['GET'])
def get_workout_exercises(workout_id):
    """Get all exercises for a workout with their association details."""
    workout = Workout.query.get_or_404(workout_id)
    result = []
    for exercise in workout.exercises:
        assoc = db.session.query(workout_exercise).filter_by(
            workout_id=workout_id, exercise_id=exercise.id
        ).first()
        result.append({
            'id': exercise.id,
            'name': exercise.name,
            'description': exercise.description,
            'muscle_group': exercise.muscle_group,
            'exercise_type': exercise.exercise_type,
            'difficulty': exercise.difficulty,
            'sets': assoc.sets if assoc else None,
            'reps': assoc.reps if assoc else None,
            'duration': assoc.duration if assoc else None
        })
    return jsonify(result)


# Error handlers
@bp.errorhandler(400)
def bad_request(e):
    return jsonify(error=str(e.description)), 400

@bp.errorhandler(404)
def not_found(e):
    return jsonify(error=str(e.description)), 404

@bp.errorhandler(500)
def internal_error(e):
    return jsonify(error='Internal server error'), 500
