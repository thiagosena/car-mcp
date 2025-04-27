"""
This module defines the `Car` class, which represents a car entity in a database using SQLAlchemy.

The `Car` class includes attributes such as brand, model, year, motorization, fuel type, color,
mileage, number of doors, transmission type, price, and additional features like air conditioning
and electric steering. It also provides methods to create an instance from a dictionary and
convert an instance to a dictionary.
"""

from sqlalchemy import Boolean, Column, Float, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Car(Base):
    """
    Represents a car entity in the database.

    Attributes:
        id (int): The unique identifier for the car.
        brand (str): The brand of the car.
        model (str): The model of the car.
        year (int): The manufacturing year of the car.
        motorization (float): The motorization of the car (e.g., engine capacity).
        fuel (str): The type of fuel used by the car.
        color (str): The color of the car.
        mileage (float): The mileage of the car. Defaults to 0.
        doors (int): The number of doors on the car. Defaults to 4.
        transmission (str): The type of transmission (e.g., manual, automatic).
        price (float): The price of the car.
        air_conditioning (bool): Indicates if the car has air conditioning. Defaults to False.
        electric_steering (bool): Indicates if the car has electric steering. Defaults to False.
        status (str): The status of the car (e.g., available, sold).

    Methods:
        from_dict(data: dict) -> Car:
            Creates a `Car` instance from a dictionary.

        to_dict() -> dict:
            Converts the `Car` instance to a dictionary.
    """
    __tablename__ = "car"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    brand = Column("brand", String(50), nullable=False)
    model = Column("model", String(100), nullable=False)
    year = Column("year", Integer, nullable=False)
    motorization = Column("motorization", Float, nullable=False)
    fuel = Column("fuel", String(20), nullable=False)
    color = Column("color", String(30), nullable=False)
    mileage = Column("mileage", Float, default=0)
    doors = Column("doors", Integer, default=4)
    transmission = Column("transmission", String(20), nullable=False)
    price = Column("price", Float, nullable=False)
    air_conditioning = Column("air_conditioning", Boolean, default=False)
    electric_steering = Column("electric_steering", Boolean, default=False)
    status = Column("status", String)

    @classmethod
    def from_dict(cls, data):
        """Creates a `Car` instance from a dictionary."""
        return cls(**data)

    def to_dict(self):
        """Converts the `Car` instance to a dictionary."""
        return {
            "id": self.id,
            "brand": self.brand,
            "model": self.model,
            "year": self.year,
            "motorization": self.motorization,
            "fuel": self.fuel,
            "color": self.color,
            "mileage": self.mileage,
            "doors": self.doors,
            "transmission": self.transmission,
            "price": self.price,
            "air_conditioning": self.air_conditioning,
            "electric_steering": self.electric_steering,
            "status": self.status,
        }
