from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    # You can add other user-related fields here, like email, password, etc.

    ingredients = relationship("Ingredient", back_populates="user")

    def __repr__(self):
        return f"<User(username='{self.username}')>"

class Ingredient(Base):
    __tablename__ = 'ingredients'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    nutrient_name = Column(String)
    nutrient_value = Column(Float)
    nutrient_unit = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship("User", back_populates="ingredients")

    def __repr__(self):
        return f"<Ingredient(name='{self.name}')>"
