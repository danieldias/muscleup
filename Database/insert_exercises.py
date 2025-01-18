from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from setup_database import Muscles, Exercise, ExerciseMuscleMapping

def connect_to_database():
    engine = create_engine('sqlite:///Database/fitness.db')
    Session = sessionmaker(bind=engine)
    return Session()

def insert_exercises(session):
    exercises = [
        "Bench Press", "Triceps Pulldown", "Shoulder Press", "Biceps Curl",
        "Leg Press", "Ab Machine", "Pull Up", "Stiff", "Hip Thrust"
    ]
    existing_exercises = session.query(Exercise).filter(Exercise.name.in_(exercises)).all()
    existing_names = {exercise.name for exercise in existing_exercises}

    new_exercises = [Exercise(name=name) for name in exercises if name not in existing_names]
    if new_exercises:
        session.add_all(new_exercises)
        session.commit()
        print(f"Added exercise: {[m.name for m in new_exercises]}")
    else:
        print("No new exercises to add.")

if __name__ == "__main__":
    session = connect_to_database()
    insert_exercises(session)
