"""
Database management module for the car inventory system.

This module provides database operations for storing and retrieving car information
using SQLAlchemy ORM. It supports SQLite database operations with logging capabilities.

Dependencies:
    - logging: For SQL query logging
    - sqlalchemy: For database operations
    - car: For Car model and Base classes
"""

import logging

from sqlalchemy import and_, create_engine
from sqlalchemy.orm import sessionmaker

from car_mcp.models.car import Base, Car

logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.DEBUG)


class DatabaseManager:
    """
    Manages database operations for the car inventory system.

    This class handles all database interactions including initialization,
    data insertion, searching, and retrieval operations.
    """

    def __init__(self, db_url="sqlite:///data/cars.db"):
        self._engine = create_engine(db_url, echo=True)
        Base.metadata.create_all(bind=self._engine)
        self._session = sessionmaker(bind=self._engine)

    def insert(self, df):
        """
        Insert car data from a DataFrame into the database.

        Args:
            df (pandas.DataFrame): DataFrame containing car information to be inserted.
        """
        df.to_sql("car", self._engine, if_exists="append", index=False)

    def search(self, filters):
        """
        Search for cars based on specified filters.

        Args:
            filters (dict): Dictionary containing search criteria with the following possible keys:
                - brand: Car brand (str)
                - model: Car model (str)
                - fuel: Fuel type (str)
                - color: Car color (str)
                - transmission: Transmission type (str)
                - year_min: Minimum year (int)
                - year_max: Maximum year (int)
                - price_min: Minimum price (float)
                - price_max: Maximum price (float)

        Returns:
            list: List of Car objects matching the search criteria.
        """
        query = self._session().query(Car)

        conditions = []
        for campo in ["brand", "model", "fuel", "color", "transmission"]:
            if campo in filters and filters[campo] is not None:
                valor = filters[campo]
                if isinstance(valor, list):
                    if len(valor) > 0:
                        or_conditions = []
                        for item in valor:
                            or_conditions.append(getattr(Car, campo).ilike(f"%{item}%"))
                        if or_conditions:
                            from sqlalchemy import or_
                            conditions.append(or_(*or_conditions))
                else:
                    conditions.append(getattr(Car, campo).ilike(f"%{valor}%"))

        if filters["year_min"] is not None and "year_min" in filters:
            conditions.append(Car.year >= filters["year_min"])

        if filters["year_max"] is not None and "year_max" in filters:
            conditions.append(Car.year <= filters["year_max"])

        if filters["price_min"] is not None and "price_min" in filters:
            conditions.append(Car.price >= filters["price_min"])

        if filters["price_max"] is not None and "price_max" in filters:
            conditions.append(Car.price <= filters["price_max"])

        if conditions:
            query = query.filter(and_(*conditions))

        resultados = query.all()
        self._session().close()

        return resultados

    def get_all_cars(self):
        """
        Retrieve all cars from the database.

        Returns:
            list: List of all Car objects in the database.
        """
        cars = self._session().query(Car).all()
        self._session().close()
        return cars
