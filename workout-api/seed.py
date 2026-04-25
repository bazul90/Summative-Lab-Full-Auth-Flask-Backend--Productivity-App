#!/usr/bin/env python
"""Seed file to create example data for all models."""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from models import db, Workout, Exercise

def seed():
    app = create_app()
    with app.app_context():
        # Drop all tables and recreate
        db.drop_all()
        db.create_all()
        print("Database tables created.")

        # Create Exercises
        exercises = [
            Exercise(
                name='Push Ups',
                description='Basic bodyweight chest exercise',
                muscle_group='chest',
                exercise_type='strength',
                difficulty='beginner'
            ),
            Exercise(
                name='Bench Press',
                description='Barbell chest press',
                muscle_group='chest',
                exercise_type='strength',
                difficulty='intermediate'
            ),
            Exercise(
                name='Squats',
                description='Bodyweight or barbell squats',
                muscle_group='legs',
                exercise_type='strength',
                difficulty='beginner'
            ),
            Exercise(
                name='Deadlift',
                description='Barbell deadlift',
                muscle_group='back',
                exercise_type='strength',
                difficulty='advanced'
            ),
            Exercise(
                name='Pull Ups',
                description='Bodyweight back exercise',
                muscle_group='back',
                exercise_type='strength',
                difficulty='intermediate'
            ),
            Exercise(
                name='Running',
                description='Cardio running',
                muscle_group='cardio',
                exercise_type='cardio',
                difficulty='beginner'
            ),
            Exercise(
                name='Bicep Curls',
                description='Dumbbell bicep curls',
                muscle_group='arms',
                exercise_type='strength',
                difficulty='beginner'
            ),
            Exercise(
                name='Plank',
                description='Core stability exercise',
                muscle_group='core',
                exercise_type='strength',
                difficulty='beginner'
            ),
        ]

        for ex in exercises:
            db.session.add(ex)
        db.session.commit()
        print(f"Created {len(exercises)} exercises.")

        # Create Workouts
        workout1 = Workout(
            name='Upper Body Strength',
            description='Full upper body workout focusing on chest, back, and arms',
            duration=60
        )
        workout1.exercises = [exercises[0], exercises[1], exercises[4], exercises[6]]
        db.session.add(workout1)

        workout2 = Workout(
            name='Lower Body Power',
            description='Leg-focused strength training',
            duration=75
        )
        workout2.exercises = [exercises[2], exercises[3]]
        db.session.add(workout2)

        workout3 = Workout(
            name='Full Body Circuit',
            description='Mixed strength and cardio circuit',
            duration=45
        )
        workout3.exercises = [exercises[0], exercises[2], exercises[5], exercises[7]]
        db.session.add(workout3)

        db.session.commit()
        print(f"Created 3 workouts.")

        # Manually create the association records with sets/reps data
        # Push Ups in Upper Body Strength
        db.session.execute(
            'INSERT INTO workout_exercise (workout_id, exercise_id, sets, reps, created_at) '
            'VALUES (1, 1, 3, 15, datetime("now"))'
        )
        # Bench Press in Upper Body Strength
        db.session.execute(
            'INSERT INTO workout_exercise (workout_id, exercise_id, sets, reps, created_at) '
            'VALUES (1, 2, 4, 10, datetime("now"))'
        )
        # Pull Ups in Upper Body Strength
        db.session.execute(
            'INSERT INTO workout_exercise (workout_id, exercise_id, sets, reps, created_at) '
            'VALUES (1, 5, 3, 8, datetime("now"))'
        )
        # Bicep Curls in Upper Body Strength
        db.session.execute(
            'INSERT INTO workout_exercise (workout_id, exercise_id, sets, reps, created_at) '
            'VALUES (1, 7, 3, 12, datetime("now"))'
        )
        # Squats in Lower Body Power
        db.session.execute(
            'INSERT INTO workout_exercise (workout_id, exercise_id, sets, reps, created_at) '
            'VALUES (2, 3, 4, 12, datetime("now"))'
        )
        # Deadlift in Lower Body Power
        db.session.execute(
            'INSERT INTO workout_exercise (workout_id, exercise_id, sets, reps, created_at) '
            'VALUES (2, 4, 3, 8, datetime("now"))'
        )
        # Push Ups in Full Body Circuit
        db.session.execute(
            'INSERT INTO workout_exercise (workout_id, exercise_id, sets, reps, created_at) '
            'VALUES (3, 1, 3, 12, datetime("now"))'
        )
        # Squats in Full Body Circuit
        db.session.execute(
            'INSERT INTO workout_exercise (workout_id, exercise_id, sets, reps, created_at) '
            'VALUES (3, 3, 3, 15, datetime("now"))'
        )
        # Running in Full Body Circuit
        db.session.execute(
            'INSERT INTO workout_exercise (workout_id, exercise_id, sets, duration, created_at) '
            'VALUES (3, 6, 1, 300, datetime("now"))'
        )
        # Plank in Full Body Circuit
        db.session.execute(
            'INSERT INTO workout_exercise (workout_id, exercise_id, sets, duration, created_at) '
            'VALUES (3, 8, 3, 60, datetime("now"))'
        )
        db.session.commit()

        print("Association records created with sets/reps/duration.")
        print("\nDatabase seeding complete!")
        print("\nWorkouts:")
        for w in [workout1, workout2, workout3]:
            print(f"  - {w.name} (ID: {w.id})")
        print("\nExercises:")
        for e in exercises:
            print(f"  - {e.name} (ID: {e.id})")


if __name__ == '__main__':
    seed()
