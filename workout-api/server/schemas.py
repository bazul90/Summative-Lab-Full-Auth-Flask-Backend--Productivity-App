from server.extensions import ma
from marshmallow import Schema, fields, validate, validates, ValidationError, validates_schema
from server.models import Exercise, Workout, WorkoutExercise


class ExerciseBasicSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Exercise
        fields = ('id', 'name', 'category', 'equipment_needed')


class WorkoutBasicSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Workout
        fields = ('id', 'date', 'duration_minutes', 'notes')


class WorkoutExerciseSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = WorkoutExercise
        include_fk = True

    reps = fields.Int(allow_none=True, validate=validate.Range(min=0))
    sets = fields.Int(allow_none=True, validate=validate.Range(min=0))
    duration_seconds = fields.Int(allow_none=True, validate=validate.Range(min=0))
    exercise = fields.Nested(ExerciseBasicSchema)
    workout = fields.Nested(WorkoutBasicSchema)

    @validates('reps')
    def validate_reps(self, value, **kwargs):
        if value is not None and value < 0:
            raise ValidationError('reps must be non-negative')

    @validates('sets')
    def validate_sets(self, value, **kwargs):
        if value is not None and value < 0:
            raise ValidationError('sets must be non-negative')

    @validates('duration_seconds')
    def validate_duration(self, value, **kwargs):
        if value is not None and value < 0:
            raise ValidationError('duration_seconds must be non-negative')

    @validates('workout_id')
    def validate_workout_id(self, value, **kwargs):
        if value is None:
            raise ValidationError('workout_id is required')
        return value

    @validates('exercise_id')
    def validate_exercise_id(self, value, **kwargs):
        if value is None:
            raise ValidationError('exercise_id is required')
        return value

    @validates_schema
    def validate_metrics(self, data, **kwargs):
        if not any(data.get(k) is not None for k in ['reps', 'sets', 'duration_seconds']):
            raise ValidationError('At least one of reps, sets, or duration_seconds must be provided')


class WorkoutSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Workout
        include_fk = True

    date = fields.Date(required=True)
    duration_minutes = fields.Int(required=True, validate=[
        validate.Range(min=1, error='Duration must be greater than 0')
    ])
    notes = fields.Str(allow_none=True)
    workout_exercises = fields.Nested(WorkoutExerciseSchema, many=True, dump_only=True)


class ExerciseSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Exercise

    name = fields.Str(required=True, validate=[
        validate.Length(min=3, error='Name must be at least 3 characters')
    ])
    category = fields.Str(required=True, validate=[
        validate.OneOf(['strength', 'cardio', 'flexibility'], error='Category must be strength, cardio, or flexibility')
    ])
    equipment_needed = fields.Bool(load_default=False)
    workout_exercises = fields.Nested(WorkoutExerciseSchema, many=True, dump_only=True)