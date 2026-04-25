import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from server.extensions import db
from server.models import Exercise, Workout, WorkoutExercise
from server.app import create_app
from datetime import date, timedelta


def seed_data():
    app = create_app('development')
    with app.app_context():
        db.drop_all()
        db.create_all()

        ex1 = Exercise(name='Bench Press', category='strength', equipment_needed=True)
        ex2 = Exercise(name='Running', category='cardio', equipment_needed=False)
        ex3 = Exercise(name='Yoga Stretch', category='flexibility', equipment_needed=False)
        ex4 = Exercise(name='Deadlift', category='strength', equipment_needed=True)
        ex5 = Exercise(name='Cycling', category='cardio', equipment_needed=True)
        ex6 = Exercise(name='Push-ups', category='strength', equipment_needed=False)

        db.session.add_all([ex1, ex2, ex3, ex4, ex5, ex6])
        db.session.commit()

        today = date.today()
        w1 = Workout(date=today - timedelta(days=6), duration_minutes=45, notes='Chest day')
        w2 = Workout(date=today - timedelta(days=5), duration_minutes=30, notes='Morning run')
        w3 = Workout(date=today - timedelta(days=4), duration_minutes=60, notes='Full body')

        db.session.add_all([w1, w2, w3])
        db.session.commit()

        we1 = WorkoutExercise(workout_id=w1.id, exercise_id=ex1.id, sets=4, reps=10)
        we2 = WorkoutExercise(workout_id=w1.id, exercise_id=ex4.id, sets=3, reps=8)
        we3 = WorkoutExercise(workout_id=w2.id, exercise_id=ex2.id, duration_seconds=1800)
        we4 = WorkoutExercise(workout_id=w2.id, exercise_id=ex5.id, sets=5, reps=10)
        we5 = WorkoutExercise(workout_id=w3.id, exercise_id=ex6.id, sets=3, reps=15)
        we6 = WorkoutExercise(workout_id=w3.id, exercise_id=ex3.id, duration_seconds=900)

        db.session.add_all([we1, we2, we3, we4, we5, we6])
        db.session.commit()

        print('Database seeded successfully!')


if __name__ == '__main__':
    seed_data()