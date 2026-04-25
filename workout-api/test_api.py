import sys
import os
from datetime import date
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from server.app import create_app
from server.extensions import db
from server.models import Exercise, Workout, WorkoutExercise

app = create_app('testing')
app.config['TESTING'] = True

client = app.test_client()

def setup():
    with app.app_context():
        db.create_all()
        ex1 = Exercise(name='Bench Press', category='strength', equipment_needed=True)
        ex2 = Exercise(name='Running', category='cardio', equipment_needed=False)
        db.session.add_all([ex1, ex2])
        db.session.commit()
        w1 = Workout(date=date(2026, 4, 19), duration_minutes=45, notes='Chest day')
        w2 = Workout(date=date(2026, 4, 20), duration_minutes=30, notes='Morning run')
        db.session.add_all([w1, w2])
        db.session.commit()

def test_health():
    r = client.get('/health')
    assert r.status_code == 200 and r.get_json()['status'] == 'healthy'
    print("✓ Health endpoint")

def test_get_workouts():
    r = client.get('/workouts')
    assert r.status_code == 200 and len(r.get_json()) == 2
    print("✓ GET /workouts list")

def test_get_workout_detail():
    r = client.get('/workouts/1')
    assert r.status_code == 200
    data = r.get_json()
    assert 'workout_exercises' in data
    print("✓ GET /workouts/<id> detail with nested")

def test_create_workout():
    r = client.post('/workouts', json={'date': '2026-04-25', 'duration_minutes': 45})
    assert r.status_code == 201
    assert r.get_json()['duration_minutes'] == 45
    print("✓ POST /workouts")

def test_create_workout_invalid():
    r = client.post('/workouts', json={'date': '2026-04-25'})
    assert r.status_code == 400
    print("✓ POST /workouts invalid (missing duration)")

def test_get_exercises():
    r = client.get('/exercises')
    assert r.status_code == 200 and len(r.get_json()) == 2
    print("✓ GET /exercises list")

def test_get_exercise_detail():
    r = client.get('/exercises/1')
    assert r.status_code == 200
    data = r.get_json()
    assert 'workout_exercises' in data
    if data['workout_exercises']:
        assert 'workout' in data['workout_exercises'][0]
    print("✓ GET /exercises/<id> detail with nested")

def test_create_exercise():
    r = client.post('/exercises', json={'name': 'Squats', 'category': 'strength'})
    assert r.status_code == 201
    assert r.get_json()['name'] == 'Squats'
    print("✓ POST /exercises")

def test_create_exercise_invalid():
    r = client.post('/exercises', json={'name': 'AB', 'category': 'strength'})
    assert r.status_code == 400
    print("✓ POST /exercises invalid (short name)")

def test_add_exercise_to_workout():
    r = client.post('/workouts/1/exercises/1/workout_exercises', json={'sets': 5, 'reps': 10})
    assert r.status_code == 201 and r.get_json()['sets'] == 5
    print("✓ POST /workouts/<wid>/exercises/<eid>/workout_exercises")

def test_add_exercise_to_workout_invalid():
    r = client.post('/workouts/1/exercises/1/workout_exercises', json={})
    assert r.status_code == 400
    print("✓ POST /workout_exercise invalid (missing metrics)")

def test_delete_workout():
    r = client.delete('/workouts/2')
    assert r.status_code == 204
    print("✓ DELETE /workouts/<id>")

def test_delete_exercise():
    r = client.delete('/exercises/2')
    assert r.status_code == 204
    print("✓ DELETE /exercises/<id>")

if __name__ == '__main__':
    with app.app_context():
        db.drop_all()
        db.create_all()
        setup()
    test_health()
    test_get_workouts()
    test_get_workout_detail()
    test_create_workout()
    test_create_workout_invalid()
    test_get_exercises()
    test_get_exercise_detail()
    test_create_exercise()
    test_create_exercise_invalid()
    test_add_exercise_to_workout()
    test_add_exercise_to_workout_invalid()
    test_delete_workout()
    test_delete_exercise()
    print("\n✅ All tests passed!")