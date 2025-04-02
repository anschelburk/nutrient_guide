from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Ingredient(Base):
    __tablename__ = 'ingredients'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    nutrient_name = Column(String)
    nutrient_value = Column(Float)
    nutrient_unit = Column(String)

    def __repr__(self):
        return f"<Ingredient(name='{self.name}')>"
