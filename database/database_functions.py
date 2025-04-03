from database.database_models import Base, Ingredient, User
from decouple import config
from sqlalchemy import create_engine, exc
from sqlalchemy.orm import sessionmaker

DATABASE_URL = config('DATABASE_URL')

try:
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
except exc.SQLAlchemyError as error:
    print(f"Error connecting to the database: {error}")
    # Handle the error appropriately, e.g., exit the application or log the error


def get_db():
    db = SessionLocal()
    try:
        yield db
    
    except exc.SQLAlchemyError as error:
        print(f"Database error: {error}")
        db.rollback()
        # Handle the error

    finally:
        db.close()

def add_ingredient(db, name, nutrient_name, nutrient_value, nutrient_unit, user_id):
    """Adds a new ingredient to the database for a specific user."""
    db_ingredient = Ingredient(
        name=name,
        nutrient_name=nutrient_name,
        nutrient_value=nutrient_value,
        nutrient_unit=nutrient_unit,
        user_id=user_id
    )
    db.add(db_ingredient)
    db.commit()
    db.refresh(db_ingredient)
    return db_ingredient

def get_ingredient_by_name(db, name, user_id):
    """Retrieves an ingredient from the database by name for a specific user."""
    return db.query(Ingredient).filter(Ingredient.name == name, Ingredient.user_id == user_id).first()

def get_all_ingredients(db, user_id):
    """Retrieves all ingredients from the database for a specific user."""
    return db.query(Ingredient).filter(Ingredient.user_id == user_id).all()

def delete_ingredient(db, name, user_id):
    """Deletes an ingredient from the database by name for a specific user."""
    db_ingredient = db.query(Ingredient).filter(Ingredient.name == name, Ingredient.user_id == user_id).first()
    if db_ingredient:
        db.delete(db_ingredient)
        db.commit()
        return True
    return False

def get_or_create_user(db, username):
    """Gets or creates a user by username."""
    user = db.query(User).filter(User.username == username).first()
    if not user:
        user = User(username=username)
        db.add(user)
        db.commit()
        db.refresh(user)
    return user