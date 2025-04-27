"""
Database initialization script for the car search system.

This script checks if the database is empty and, if so, generates fictional car data
to populate it. If the database already contains records, it skips the data generation
process.

Dependencies:
    - data_generator: Provides functions to generate fictional car data
    - db_manager: Handles database operations through DatabaseManager class
"""

from car_mcp.database.data_generator import generate_cars
from car_mcp.database.db_manager import DatabaseManager


def main():
    """
    Initialize the car search system database.
    
    This function checks if the database is empty. If empty, it generates 1000 fictional
    car records and inserts them into the database. If the database already contains
    records, it skips the data generation process.
    
    Returns:
        None
    """
    print("Inicializando sistema de busca de automóveis...")

    db_manager = DatabaseManager()

    if len(db_manager.get_all_cars()) == 0:
        print("Banco de dados vazio. Gerando dados fictícios...")
        pd_data_frame_cars = generate_cars(total_cars=1000)
        db_manager.insert(pd_data_frame_cars)
        print(f"Banco de dados populado com {len(pd_data_frame_cars)} automóveis.")
    else:
        print("Banco de dados já contém registros. Pulando geração de dados.")


if __name__ == "__main__":
    main()
