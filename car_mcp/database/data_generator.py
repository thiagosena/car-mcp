"""
Fictional car data generator module.

This module provides functionality to generate random car data using Faker library
with Brazilian Portuguese localization. It creates realistic-looking automobile data
including various attributes such as brand, model, year, and specifications.

Dependencies:
    - random: For random selections
    - pandas: For DataFrame creation
    - faker: For generating fake data
    - faker_vehicle: For vehicle-specific fake data
"""

import random

import pandas as pd
from faker import Faker
from faker_vehicle import VehicleProvider

fake = Faker("pt_BR")
fake.add_provider(VehicleProvider)


def generate_cars(total_cars=100):
    """
    Generate a DataFrame containing fictional car data.

    Args:
        total_cars (int, optional): Number of car records to generate. Defaults to 100.

    Returns:
        pandas.DataFrame: A DataFrame containing generated car records with the following columns:
            - brand: Car manufacturer
            - model: Car model name
            - year: Manufacturing year
            - motorization: Engine size (in liters)
            - fuel: Fuel type
            - color: Car color
            - mileage: Odometer reading
            - doors: Number of doors
            - transmission: Transmission type
            - price: Car price
            - air_conditioning: Boolean indicating AC presence
            - electric_steering: Boolean indicating electric steering presence
            - status: New or Used condition
    """
    print(f"Gerando {total_cars} automóveis fictícios...")

    cars = []

    for _ in range(total_cars):

        mileage = random.choice([0, 50000, 150000, 200000])
        colors = [
            "Preto",
            "Branco",
            "Prata",
            "Azul",
            "Vermelho",
            "Cinza",
            "Verde",
            "Amarelo",
            "Marrom",
            "Bege",
        ]
        transmissions = [
            "Manual",
            "Automática",
            "CVT",
            "Semi-automática",
            "Automatizada",
            "DCT",
        ]

        car = {
            "brand": fake.vehicle_make(),
            "model": fake.vehicle_make_model(),
            "year": int(fake.vehicle_year()),
            "motorization": random.choice(
                [1.0, 1.3, 1.4, 1.5, 1.6, 1.8, 2.0, 2.5, 3.0]
            ),
            "fuel": fake.random_element(
                elements=("Gasolina", "Etanol", "Flex", "Diesel", "Elétrico", "Híbrido")
            ),
            "color": random.choice(colors),
            "mileage": mileage,
            "doors": random.choice([2, 4]),
            "transmission": random.choice(transmissions),
            "price": f"{fake.random_int(min=5000, max=150000):.2f}",
            "air_conditioning": random.random() > 0.1,
            "electric_steering": random.random() > 0.2,
            "status": "Novo" if mileage == 0 else "Usado",
        }
        cars.append(car)

    data_frame = pd.DataFrame(cars)
    return data_frame
