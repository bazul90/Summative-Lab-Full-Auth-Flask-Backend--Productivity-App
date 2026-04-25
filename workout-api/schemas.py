from marshmallow import Schema, fields, post_load, pre_load, validates, validates_schema, ValidationError
from models import Workout, Exercise
import re


class ExerciseSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True)
    description = fields.String(allow_none=True)
    muscle_group = fields.String(allow_none=True)
    exercise_type = fields.String(required=False, default='strength')
    difficulty = fields.String(allow_none=True)
    created_at = fields.DateTime(dump_only=True)
    # Nested workout IDs for relationship management
    workout_ids = fields.List(fields.Integer(), dump_only=True)

    # Schema-level validations
    @validates('name')
    def validate_name(self, value):
        """Validate exercise name."""
        if not value or not value.strip():
            raise ValidationError("Exercise name cannot be empty")
        if len(value.strip()) < 2:
            raise ValidationError("Exercise name must be at least 2 characters long")
        if len(value.strip()) > 120:
            raise ValidationError("Exercise name cannot exceed 120 characters")
        # Prevent excessive whitespace
        if re.search(r'\s{2,}', value):
            raise ValidationError("Exercise name cannot contain multiple consecutive spaces")

    @validates('exercise_type')
    def validate_exercise_type(self, value):
        """Validate exercise type."""
        valid_types = ['strength', 'cardio', 'flexibility', 'balance', 'endurance']
        if value not in valid_types:
            raise ValidationError(f"Exercise type must be one of: {', '.join(valid_types)}")

    @validates('difficulty')
    def validate_difficulty(self, value):
        """Validate difficulty level if provided."""
        if value:
            valid_levels = ['beginner', 'intermediate', 'advanced']
            if value not in valid_levels:
                raise ValidationError(f"Difficulty must be one of: {', '.join(valid_levels)}")

    @validates('muscle_group')
    def validate_muscle_group(self, value):
        """Validate muscle group if provided."""
        if value and len(value) > 60:
            raise ValidationError("Muscle group cannot exceed 60 characters")

    @pre_load
    def strip_strings(self, data, **kwargs):
        """Strip whitespace from string fields."""
        result = {}
        for key, val in data.items():
            if isinstance(val, str):
                result[key] = val.strip()
            else:
                result[key] = val
        return result

    @post_load
    def make_exercise(self, data, **kwargs):
        """Create Exercise instance from dict."""
        return Exercise(**data)


class WorkoutSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True)
    description = fields.String(allow_none=True)
    date = fields.DateTime(allow_none=True)
    duration = fields.Integer(allow_none=True)
    created_at = fields.DateTime(dump_only=True)
    # Nested exercise data when expanding
    exercises = fields.Nested(ExerciseSchema, many=True, dump_only=True)
    exercise_ids = fields.List(fields.Integer(), load_only=True, allow_none=True,
                               metadata={'description': 'List of exercise IDs to associate with this workout'})

    # Schema-level validations
    @validates('name')
    def validate_name(self, value):
        """Validate workout name."""
        if not value or not value.strip():
            raise ValidationError("Workout name cannot be empty")
        if len(value.strip()) < 2:
            raise ValidationError("Workout name must be at least 2 characters long")
        if len(value.strip()) > 120:
            raise ValidationError("Workout name cannot exceed 120 characters")
        if re.search(r'\s{2,}', value):
            raise ValidationError("Workout name cannot contain multiple consecutive spaces")

    @validates('duration')
    def validate_duration(self, value):
        """Validate duration if provided."""
        if value is not None:
            if not isinstance(value, int) or value <= 0:
                raise ValidationError("Duration must be a positive integer")
            if value > 1440:  # More than 24 hours
                raise ValidationError("Duration cannot exceed 1440 minutes (24 hours)")

    @validates_schema
    def validate_associated_exercises(self, data, **kwargs):
        """Validate that exercise_ids reference existing exercises when provided."""
        # This validation is checked at the route level since we need DB access
        pass

    @pre_load
    def strip_strings(self, data, **kwargs):
        """Strip whitespace from string fields."""
        result = {}
        for key, val in data.items():
            if isinstance(val, str):
                result[key] = val.strip()
            else:
                result[key] = val
        return result

    @post_load
    def make_workout(self, data, **kwargs):
        """Create Workout instance from dict."""
        # Don't pass exercise_ids to constructor
        exercise_ids = data.pop('exercise_ids', None)
        return Workout(**data), exercise_ids


class WorkoutExerciseSchema(Schema):
    """Schema for adding exercises to a workout with sets/reps/duration."""
    exercise_id = fields.Integer(required=True)
    sets = fields.Integer(required=False, default=3)
    reps = fields.Integer(allow_none=True)
    duration = fields.Integer(allow_none=True)  # in seconds

    @validates('sets')
    def validate_sets(self, value):
        if value <= 0:
            raise ValidationError("Sets must be a positive integer")

    @validates('reps')
    def validate_reps(self, value):
        if value is not None and value <= 0:
            raise ValidationError("Reps must be a positive integer")

    @validates('duration')
    def validate_duration(self, value):
        if value is not None and value <= 0:
            raise ValidationError("Duration must be a positive integer")

    @validates_schema
    def validate_reps_or_duration(self, data, **kwargs):
        """Validate that either reps or duration is provided."""
        reps = data.get('reps')
        duration = data.get('duration')
        if reps is None and duration is None:
            raise ValidationError("Either reps or duration must be provided")
