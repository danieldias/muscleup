from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from setup_database import Muscles, Exercise, ExerciseMuscleMapping

def connect_to_database():
    engine = create_engine('sqlite:///fitness.db')
    Session = sessionmaker(bind=engine)
    return Session()

def insert_muscles(session):
    muscles = [
        "Chest", "Triceps", "Shoulders", "Biceps",
        "Quadriceps", "Abs", "Back", "Hamstrings", "Glutes"
    ]
    existing_muscles = session.query(Muscles).filter(Muscles.name.in_(muscles)).all()
    existing_names = {muscle.name for muscle in existing_muscles}

    new_muscles = [Muscles(name=name) for name in muscles if name not in existing_names]
    if new_muscles:
        session.add_all(new_muscles)
        session.commit()
        print(f"Added muscles: {[m.name for m in new_muscles]}")
    else:
        print("No new muscles to add.")

if __name__ == "__main__":
    session = connect_to_database()
    insert_muscles(session)
