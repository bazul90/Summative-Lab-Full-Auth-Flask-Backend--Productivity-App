from server.extensions import db
from sqlalchemy.orm import validates
from sqlalchemy import CheckConstraint


class Exercise(db.Model):
    __tablename__ = 'exercises'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    category = db.Column(db.String(50), nullable=False)
    equipment_needed = db.Column(db.Boolean, default=False)

    workout_exercises = db.relationship('WorkoutExercise', back_populates='exercise', cascade='all, delete-orphan')
    workouts = db.relationship('Workout', secondary='workout_exercises', back_populates='exercises', viewonly=True)

    __table_args__ = (
        CheckConstraint('LENGTH(TRIM(name)) >= 3', name='name_min_length'),
        CheckConstraint("category IN ('strength', 'cardio', 'flexibility')", name='valid_category'),
    )

    @validates('name')
    def validate_name(self, key, name):
        if not name or name.strip() == '':
            raise ValueError('Exercise name cannot be empty')
        if len(name.strip()) < 3:
            raise ValueError('Exercise name must be at least 3 characters')
        return name.strip()

    @validates('category')
    def validate_category(self, key, category):
        valid_categories = ['strength', 'cardio', 'flexibility']
        if category not in valid_categories:
            raise ValueError(f'Category must be one of: {valid_categories}')
        return category


class Workout(db.Model):
    __tablename__ = 'workouts'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text)

    workout_exercises = db.relationship('WorkoutExercise', back_populates='workout', cascade='all, delete-orphan')
    exercises = db.relationship('Exercise', secondary='workout_exercises', back_populates='workouts', viewonly=True)

    __table_args__ = (
        CheckConstraint('duration_minutes > 0', name='duration_positive'),
    )

    @validates('duration_minutes')
    def validate_duration(self, key, duration):
        if duration <= 0:
            raise ValueError('Duration must be greater than 0')
        return duration


class WorkoutExercise(db.Model):
    __tablename__ = 'workout_exercises'

    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey('workouts.id'), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'), nullable=False)
    reps = db.Column(db.Integer)
    sets = db.Column(db.Integer)
    duration_seconds = db.Column(db.Integer)

    workout = db.relationship('Workout', back_populates='workout_exercises')
    exercise = db.relationship('Exercise', back_populates='workout_exercises')

    __table_args__ = (
        CheckConstraint('reps IS NULL OR reps >= 0', name='reps_non_negative'),
        CheckConstraint('sets IS NULL OR sets >= 0', name='sets_non_negative'),
        CheckConstraint('duration_seconds IS NULL OR duration_seconds >= 0', name='duration_seconds_non_negative'),
        CheckConstraint('reps IS NOT NULL OR sets IS NOT NULL OR duration_seconds IS NOT NULL',
                        name='at_least_one_metric'),
    )

    @validates('reps', 'sets', 'duration_seconds')
    def validate_non_negative(self, key, value):
        if value is not None and value < 0:
            raise ValueError(f'{key} must be non-negative')
        return value

    @validates('workout_id', 'exercise_id')
    def validate_foreign_keys(self, key, value):
        if value is None:
            raise ValueError(f'{key} cannot be null')
        return value