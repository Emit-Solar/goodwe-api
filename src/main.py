from goodwe_client import GoodWeClient
from config import Config
from logger import Logger
from database import PostgreSQLClient
import re


# Sample usage
def main():
    log = Logger("logs/api.log", clear=True)
    api_client = GoodWeClient(
        Config.GOODWE_USERNAME,
        Config.GOODWE_PASSWORD,
        Config.GOODWE_API_URL,
        Config.DEFAULT_HEADERS,
        log,
    )
    print(api_client.token)

    db_client = PostgreSQLClient(
        Config.POSTGRES_IP,
        Config.POSTGRES_USERNAME,
        Config.POSTGRES_PASSWORD,
        Config.POSTGRES_DB,
        Config.POSTGRES_SCHEMA,
        log,
        port=Config.POSTGRES_PORT,
    )

    # Init PostGreSQL database with correct columns and tables
    plant_num, plant_list = api_client.get_plant_list()
    sample_plant = plant_list[0]
    sample_monitor_detail = api_client.get_monitor_detail_by_powerstation_id(
        sample_plant["plantId"]
    )
    db_client.create_table("plant_list", sample_plant)
    db_client.create_table("monitor_detail", sample_monitor_detail)

    # Add all plant data to database
    for i in range(plant_num):
        # Insert to plant_list table
        capacity_str = plant_list[i]["capacity"]
        plant_list[i]["capacity"] = float(
            "".join(c for c in capacity_str if c.isdigit() or c == ".")
        )
        db_client.insert_data("plant_list", plant_list[i])


if __name__ == "__main__":
    main()
