from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

db = SQLAlchemy()


class CarOwner(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    cars = relationship("Car", back_populates="owner")


class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    color = db.Column(
        db.Enum("yellow", "blue", "gray", name="color_types"), nullable=False
    )
    model = db.Column(
        db.Enum("hatch", "sedan", "convertible", name="model_types"), nullable=False
    )
    owner_id = db.Column(db.Integer, db.ForeignKey("car_owner.id"), nullable=False)
    owner = relationship("CarOwner", back_populates="cars")
