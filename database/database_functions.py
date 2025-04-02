from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.database_models import Base, Ingredient  # Assuming db_models.py is in a 'database' directory

DATABASE_URL = "sqlite:///./nutrient_guide.db"  # You can change this to a different database

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def add_ingredient(db, name, nutrient_name, nutrient_value, nutrient_unit):
    """Adds a new ingredient to the database."""
    db_ingredient = Ingredient(
        name=name,
        nutrient_name=nutrient_name,
        nutrient_value=nutrient_value,
        nutrient_unit=nutrient_unit
    )
    db.add(db_ingredient)
    db.commit()
    db.refresh(db_ingredient)
    return db_ingredient

def get_ingredient_by_name(db, name):
    """Retrieves an ingredient from the database by name."""
    return db.query(Ingredient).filter(Ingredient.name == name).first()

def get_all_ingredients(db):
    """Retrieves all ingredients from the database."""
    return db.query(Ingredient).all()

def delete_ingredient(db, name):
    """Deletes an ingredient from the database by name."""
    db_ingredient = db.query(Ingredient).filter(Ingredient.name == name).first()
    if db_ingredient:
        db.delete(db_ingredient)
        db.commit()
        return True
    return False
