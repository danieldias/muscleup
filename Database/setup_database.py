from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship, declarative_base, sessionmaker

Base = declarative_base()

class Exercise(Base):
    __tablename__ = 'exercises' #Name of the table in the dataset
    id = Column(Integer, primary_key=True) #Primary key column
    name = Column(String, nullable=False, unique=True) #Name of the exercise 

    #Relationship with the junction table
    muscles_activated = relationship("ExerciseMuscleMapping", back_populates="exercises_that_activate")

class ExerciseMuscleMapping(Base):
    __tablename__ = 'exercise_muscle_mapping' #Name of the junction table
    id = Column(Integer, primary_key=True) #Primary key column
    exercise_id = Column(Integer, ForeignKey('exercises.id'), nullable=False) #Foreign key column
    muscle_id = Column(Integer, ForeignKey('muscles.id'), nullable=False) #Foreign key column
    percentage = Column(Float, nullable=False) #Percentage of muscle activation

    #Relationship with the exercises table
    exercises_that_activate = relationship("Exercise", back_populates="muscles_activated")

    #Relationship with the muscles table
    muscles_activated = relationship("Muscles", back_populates="exercises_that_activate")

class Muscles(Base):
    __tablename__ = 'muscles' #Name of the table in the dataset
    id = Column(Integer, primary_key=True) #Primary key column
    name = Column(String, nullable=False, unique=True) #Name of the muscle

    #Relationship with the junction table
    exercises_that_activate = relationship("ExerciseMuscleMapping", back_populates="muscles_activated")

#Create the SQLite database and establish a connection
def setup_database():
    engine = create_engine('sqlite:///fitness.db') #databsed named exercises.db
    Base.metadata.create_all(engine) #Create the tables in the schema
    print("Database setup complete.")
    return engine

if __name__ == "__main__":
    engine = setup_database()  # Call the setup function to create the database