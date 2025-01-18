from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from setup_database import Exercise, Muscles, ExerciseMuscleMapping

# Step 1: Connect to the database
def connect_to_database():
    engine = create_engine('sqlite:///Database/fitness.db')
    Session = sessionmaker(bind=engine)
    return Session()

# Step 2: Map exercises to muscles with activation percentages
def map_exercises_to_muscles(session):
    # Define mappings for each exercise
    mappings = [
        {"exercise": "Bench Press", "muscles": [("Chest", 70.0), ("Triceps", 20.0), ("Shoulders", 10.0)]},
        {"exercise": "Triceps Pulldown", "muscles": [("Triceps", 100.0)]},
        {"exercise": "Shoulder Press", "muscles": [("Shoulders", 80.0), ("Triceps", 20.0)]},
        {"exercise": "Biceps Curl", "muscles": [("Biceps", 100.0)]},
        {"exercise": "Leg Press", "muscles": [("Quadriceps", 90.0), ("Glutes", 10.0)]},
        {"exercise": "Ab Machine", "muscles": [("Abs", 100.0)]},
        {"exercise": "Pull Up", "muscles": [("Back", 70.0), ("Biceps", 30.0)]},
        {"exercise": "Stiff", "muscles": [("Hamstrings", 80.0), ("Glutes", 20.0)]},
        {"exercise": "Hip Thrust", "muscles": [("Glutes", 100.0)]},
    ]

    for mapping in mappings:
        # Step 2.1: Retrieve the exercise by name
        exercise = session.query(Exercise).filter_by(name=mapping["exercise"]).first()

        if not exercise:
            print(f"Exercise '{mapping['exercise']}' not found in the database. Skipping.")
            continue

        # Step 2.2: Map muscles to the exercise
        for muscle_name, percentage in mapping["muscles"]:
            muscle = session.query(Muscles).filter_by(name=muscle_name).first()

            if not muscle:
                print(f"Muscle '{muscle_name}' not found in the database. Skipping.")
                continue

            # Step 2.3: Check if the mapping already exists
            existing_mapping = session.query(ExerciseMuscleMapping).filter_by(
                exercise_id=exercise.id, muscle_id=muscle.id
            ).first()

            if existing_mapping:
                print(f"Mapping for '{exercise.name}' and '{muscle.name}' already exists. Skipping.")
                continue

            # Step 2.4: Add a new mapping
            new_mapping = ExerciseMuscleMapping(
                exercise_id=exercise.id,
                muscle_id=muscle.id,
                percentage=percentage
            )
            session.add(new_mapping)
            print(f"Added mapping: {exercise.name} -> {muscle.name} ({percentage}%)")

    # Commit all changes to the database
    session.commit()
    print("All mappings processed.")

# Step 3: Main execution
if __name__ == "__main__":
    session = connect_to_database()
    map_exercises_to_muscles(session)
