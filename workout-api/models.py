from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint, UniqueConstraint
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

# Association table for many-to-many relationship between Workout and Exercise
workout_exercise = db.Table('workout_exercise',
    db.Column('workout_id', db.Integer, db.ForeignKey('workout.id'), primary_key=True),
    db.Column('exercise_id', db.Integer, db.ForeignKey('exercise.id'), primary_key=True),
    db.Column('sets', db.Integer, nullable=False, default=3),
    db.Column('reps', db.Integer, nullable=True),
    db.Column('duration', db.Integer, nullable=True),  # in seconds, for time-based exercises
    db.Column('created_at', db.DateTime, default=datetime.utcnow),
    UniqueConstraint('workout_id', 'exercise_id', name='uq_workout_exercise'),
    CheckConstraint('sets > 0', name='check_sets_positive'),
    CheckConstraint('reps > 0 OR duration > 0', name='check_reps_or_duration_positive')
)


class Workout(db.Model):
    __tablename__ = 'workout'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    duration = db.Column(db.Integer, nullable=True)  # total duration in minutes
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    exercises = db.relationship('Exercise', secondary=workout_exercise, lazy='joined',
        backref=db.backref('workouts', lazy='dynamic'))

    # Table-level constraints
    __table_args__ = (
        CheckConstraint('duration > 0', name='check_workout_duration_positive'),
    )

    # Model-level validations
    def validate_name(self):
        """Validate that workout name is not empty and has reasonable length."""
        if not self.name or not self.name.strip():
            raise ValueError("Workout name cannot be empty")
        if len(self.name.strip()) < 2:
            raise ValueError("Workout name must be at least 2 characters long")
        if len(self.name.strip()) > 120:
            raise ValueError("Workout name cannot exceed 120 characters")

    def validate_duration(self):
        """Validate that duration is positive if provided."""
        if self.duration is not None and self.duration <= 0:
            raise ValueError("Duration must be a positive number")

    def validate(self):
        """Run all validations."""
        self.validate_name()
        self.validate_duration()

    def __repr__(self):
        return f'<Workout {self.name}>'


class Exercise(db.Model):
    __tablename__ = 'exercise'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=True)
    muscle_group = db.Column(db.String(60), nullable=True)
    exercise_type = db.Column(db.String(60), nullable=False, default='strength')  # strength, cardio, flexibility
    difficulty = db.Column(db.String(20), nullable=True)  # beginner, intermediate, advanced
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Table-level constraints
    __table_args__ = (
        CheckConstraint("exercise_type IN ('strength', 'cardio', 'flexibility', 'balance', 'endurance')",
            name='check_exercise_type_valid'),
        CheckConstraint("difficulty IN ('beginner', 'intermediate', 'advanced') OR difficulty IS NULL",
            name='check_difficulty_valid'),
    )

    # Model-level validations
    def validate_name(self):
        """Validate that exercise name is not empty and has reasonable length."""
        if not self.name or not self.name.strip():
            raise ValueError("Exercise name cannot be empty")
        if len(self.name.strip()) < 2:
            raise ValueError("Exercise name must be at least 2 characters long")
        if len(self.name.strip()) > 120:
            raise ValueError("Exercise name cannot exceed 120 characters")

    def validate_muscle_group(self):
        """Validate muscle group if provided."""
        valid_groups = ['chest', 'back', 'legs', 'shoulders', 'arms', 'core', 'full body',
                       'glutes', 'calves', 'forearms', 'neck', 'cardio']
        if self.muscle_group and self.muscle_group.lower() not in valid_groups:
            # Allow custom muscle groups but warn via convention
            pass

    def validate_type(self):
        """Validate exercise type."""
        valid_types = ['strength', 'cardio', 'flexibility', 'balance', 'endurance']
        if self.exercise_type not in valid_types:
            raise ValueError(f"Exercise type must be one of: {', '.join(valid_types)}")

    def validate_difficulty(self):
        """Validate difficulty level if provided."""
        if self.difficulty:
            valid_levels = ['beginner', 'intermediate', 'advanced']
            if self.difficulty not in valid_levels:
                raise ValueError(f"Difficulty must be one of: {', '.join(valid_levels)}")

    def validate(self):
        """Run all validations."""
        self.validate_name()
        self.validate_muscle_group()
        self.validate_type()
        self.validate_difficulty()

    def __repr__(self):
        return f'<Exercise {self.name}>'
