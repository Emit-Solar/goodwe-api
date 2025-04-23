from goodwe_client import GoodWeClient
from config import Config
from logger import Logger
from database import PostgreSQLClient


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

    db_client = PostgreSQLClient(
        Config.POSTGRES_IP,
        Config.POSTGRES_USERNAME,
        Config.POSTGRES_PASSWORD,
        Config.POSTGRES_DB,
        Config.POSTGRES_SCHEMA,
        log,
        port=Config.POSTGRES_PORT,
    )

    plant_num, plant_list = api_client.get_plant_list()

    for i in range(plant_num):
        capacity_str = plant_list[i]["capacity"]
        plant_list[i]["capacity"] = float(
            "".join(c for c in capacity_str if c.isdigit() or c == ".")
        )
        db_client.insert_plant(plant_list[i])


if __name__ == "__main__":
    main()
