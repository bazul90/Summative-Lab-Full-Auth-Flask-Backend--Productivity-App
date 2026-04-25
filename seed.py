from app import create_app
from models import db, User, Note

app = create_app()

with app.app_context():
    db.create_all()

    # Create test users
    user1 = User(username='alice')
    user1.set_password('password123')

    user2 = User(username='bob')
    user2.set_password('password123')

    db.session.add_all([user1, user2])
    db.session.commit()

    # Create notes for user1
    notes_user1 = [
        Note(title='Groceries', content='Buy milk, eggs, bread', user_id=user1.id),
        Note(title='Meeting notes', content='Discuss project timeline', user_id=user1.id),
        Note(title='Book list', content='Read Clean Architecture', user_id=user1.id),
        Note(title='Workout', content='Morning run 5km', user_id=user1.id),
        Note(title='Ideas', content='Build a Flask API', user_id=user1.id),
    ]

    # Create notes for user2
    notes_user2 = [
        Note(title='Shopping', content='Buy laptop stand', user_id=user2.id),
        Note(title='Project', content='Complete backend API', user_id=user2.id),
        Note(title='Habits', content='Drink more water', user_id=user2.id),
    ]

    db.session.add_all(notes_user1 + notes_user2)
    db.session.commit()

    print('✅ Database seeded successfully!')
    print(f'Created users: {user1.username}, {user2.username}')
    print(f'Total notes: {Note.query.count()}')
