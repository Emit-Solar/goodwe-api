from src.main import initialization
from datetime import timedelta, date
import time

API_TOKEN_INTERVAL = 120


def main():
    log, api_client, sql_client, dt_processor = initialization("realtime_power.log")
    last_login = time.time()

    # get installation date from db first, otherwise get it from api

    # use first station as example
    query = f"SELECT station_id, create_date FROM {sql_client.schema}.station_list"
    station_id, create_date = None, None

    try:
        raw = sql_client.execute_query(query)
        log.info("Retrieved station list from database")

        if raw:
            station_id, create_date = raw[0]
            log.info(f"Using station {station_id} with installation date {create_date}")
        else:
            log.info("No stations found in the database, retrieving from API")
            plant_num, plant_list = api_client.get_plant_list()
            station_df = dt_processor.process_plant_list(plant_num, plant_list)
            station_id, create_date = (
                station_df[0, "station_id"],
                station_df[0, "create_date"],
            )

    except Exception as e:
        log.exception("Failed to retrieve station list from database or API", e)

    start_date = None

    if station_id and create_date:
        # get latest power data
        query = f"SELECT collect_time FROM {sql_client.schema}.station_realtime_power WHERE station_id = '{station_id}' ORDER BY collect_time DESC LIMIT 1"
        try:
            raw = sql_client.execute_query(query)
            if not raw:
                start_date = create_date.date()
            else:
                start_date = raw[0][0].date() + timedelta(days=1)

        except Exception as e:
            log.exception("Failed to retrieve latest power data from database", e)

    if start_date:
        # Fetch power data from start_date to now
        today = date.today()
        while start_date <= today:
            # Refresh API token every 2 minutes
            if time.time() - last_login > API_TOKEN_INTERVAL:
                log.info("Refreshing API token")
                try:
                    api_client.login()
                    last_login = time.time()
                    log.info("API token refreshed successfully")
                except Exception as e:
                    log.exception("Failed to refresh API token", e)
                    break

            date_str = start_date.strftime("%Y-%m-%d")
            log.info(f"Fetching power data on {date_str} for {station_id}")

            try:
                plant_power = api_client.get_plant_power_chart(station_id, date_str)
                power_df = dt_processor.process_plant_power_chart(
                    station_id, date_str, plant_power
                )
                if power_df is not None:
                    sql_client.upsert_data(
                        power_df,
                        "station_realtime_power",
                        primary_keys=["collect_time", "station_id"],
                    )
                    log.info(
                        f"Successfully processed power data for {station_id} on {date_str}"
                    )
                else:
                    log.warning(
                        f"No power data found for {station_id} on {date_str}, skipping"
                    )

            except Exception as e:
                log.exception(
                    f"Failed to fetch or process power data for {station_id} on {date_str}",
                    e,
                )

            start_date += timedelta(days=1)

        log.info("All power data fetched successfully")
        sql_client.close()


if __name__ == "__main__":
    main()
