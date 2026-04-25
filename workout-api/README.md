# Workout Tracker API

A Flask REST API for tracking workouts and exercises with a many-to-many relationship through a join table that stores additional metrics.

## Features

- **Exercise Management**: Create, view, and delete exercises with categories and equipment flags
- **Workout Management**: Create, view, and delete workout sessions with duration and notes
- **Workout-Exercise Linking**: Add exercises to workouts with reps, sets, or duration tracking
- **Cascade Deletes**: Deleting a workout or exercise removes all associated workout-exercise links
- **Nested Serialization**: Full relationship data included in responses
- **Input Validation**: Comprehensive schema and model-level validation

## Tech Stack

- Flask 2.x
- Flask-SQLAlchemy (ORM)
- Flask-Migrate (database migrations)
- Flask-Marshmallow (serialization/deserialization)
- SQLAlchemy (database abstraction)

## Project Structure

```
workout-api/
├── server/
│   ├── __init__.py
│   ├── app.py              # Application factory
│   ├── config.py           # Configuration
│   ├── extensions.py       # Flask extensions
│   ├── models.py           # Database models
│   ├── schemas.py          # Marshmallow schemas
│   ├── seed.py             # Database seeder
│   └── routes/
│       ├── exercise_routes.py
│       ├── workout_routes.py
│       └── workout_exercise_routes.py
├── Pipfile
├── README.md
└── .gitignore
```

## Database Schema

### Exercise
- `id` (PK)
- `name` (string, unique, required)
- `category` (enum: strength, cardio, flexibility)
- `equipment_needed` (boolean, default False)

### Workout
- `id` (PK)
- `date` (date, required)
- `duration_minutes` (integer, positive)
- `notes` (text, optional)

### WorkoutExercise (Join Table)
- `id` (PK)
- `workout_id` (FK to Workout, required)
- `exercise_id` (FK to Exercise, required)
- `reps` (integer, optional, ≥0)
- `sets` (integer, optional, ≥0)
- `duration_seconds` (integer, optional, ≥0)

Constraints:
- Exercise name must be ≥3 characters and unique
- Workout duration must be > 0
- WorkoutExercise requires at least one metric (reps, sets, or duration_seconds)
- All numeric fields are non-negative

## Installation

```bash
# Install dependencies with pipenv
pipenv install

# Activate virtual environment
pipenv shell
```

## Setup

```bash
# Initialize database migrations
flask db init

# Create initial migration
flask db migrate -m "initial"

# Apply migration
flask db upgrade

# Seed database with sample data
python server/seed.py
```

## Running the API

```bash
flask run
```

The API will be available at `http://localhost:5000`

## API Endpoints

### Workouts

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/workouts` | List all workouts |
| GET | `/workouts/<id>` | Get workout details with exercises |
| POST | `/workouts` | Create a new workout |
| DELETE | `/workouts/<id>` | Delete workout (cascade) |

### Exercises

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/exercises` | List all exercises |
| GET | `/exercises/<id>` | Get exercise details with workouts |
| POST | `/exercises` | Create a new exercise |
| DELETE | `/exercises/<id>` | Delete exercise (cascade) |

### Workout-Exercises

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/workouts/<workout_id>/exercises/<exercise_id>/workout_exercises` | Add exercise to workout with metrics |

## Example Requests

### Create a Workout

```bash
curl -X POST http://localhost:5000/workouts \
  -H "Content-Type: application/json" \
  -d '{"date": "2025-04-25", "duration_minutes": 60, "notes": "Strength training"}'
```

### Create an Exercise

```bash
curl -X POST http://localhost:5000/exercises \
  -H "Content-Type: application/json" \
  -d '{"name": "Squats", "category": "strength", "equipment_needed": false}'
```

### Add Exercise to Workout

```bash
curl -X POST http://localhost:5000/workouts/1/exercises/1/workout_exercises \
  -H "Content-Type: application/json" \
  -d '{"sets": 4, "reps": 12}'
```

### Get Workout with Exercises

```bash
curl http://localhost:5000/workouts/1
```

Response includes nested `workout_exercises` data with exercise details.

### Get Exercise with Workouts

```bash
curl http://localhost:5000/exercises/1
```

## Validation

The API enforces the following validation rules:

**Schema Level (Marshmallow):**
- Name minimum 3 characters
- Category must be one of: strength, cardio, flexibility
- Duration must be greater than 0
- At least one metric required for workout-exercise links

**Model Level (@validates):**
- Name cannot be empty
- Category from predefined list
- All numeric values are positive
- Foreign keys are required

**Database Constraints:**
- CHECK constraints on duration and numeric fields
- UNIQUE constraint on exercise name
- NOT NULL on required fields

## Error Handling

All validation errors return 400 with error message:

```json
{
  "error": "Description of the validation error"
}
```

Not found resources return 404.

## Seeding

The `seed.py` script creates:
- 6 exercises (2 strength, 2 cardio, 2 flexibility)
- 3 workouts with varying dates
- 6 workout-exercise associations demonstrating all metric types

Run the seeder anytime to reset the database:

```bash
python server/seed.py
```

## Development

To add new routes, create a file in `server/routes/` and register the blueprint in `app.py`.

Models should be defined in `models.py` with constraints and validators.

Schemas in `schemas.py` handle serialization and request validation.