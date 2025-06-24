from src.main import initialization


def main():
    log, api_client, sql_client, dt_processor = initialization("station_list.log")

    plant_num, plant_list = api_client.get_plant_list()
    station_df = dt_processor.process_plant_list(plant_num, plant_list)

    sql_client.upsert_data(station_df, "station_list", ["station_id"])


if __name__ == "__main__":
    main()
