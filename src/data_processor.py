import polars as pl
from datetime import datetime
from .model import GoodweModels
from decimal import Decimal


class GoodweDataProcessor:
    def __init__(self, log):
        self.log = log

    def process_plant_list(self, plant_num, plant_list):
        self.log.info("Processing plant list")

        raw_lf = pl.LazyFrame(plant_list)

        transformed_lf = raw_lf.select(
            pl.col("plantId").alias("station_id").cast(pl.Utf8),
            pl.col("plantName").alias("station_name").cast(pl.Utf8),
            pl.col("hasInverters").alias("has_inverters").cast(pl.Boolean),
            pl.col("capacity")
            .str.replace_all(" kW", "")
            .alias("capacity")
            .cast(pl.Decimal(10, 2)),
            pl.col("createDate")
            .str.to_datetime(format="%m/%d/%Y")
            .alias("create_date")
            .cast(pl.Datetime),
            pl.col("latitude").cast(pl.Decimal(10, 7)),
            pl.col("longitude").cast(pl.Decimal(10, 7)),
        )

        result = transformed_lf.collect()
        self.log.info(f"Processed {plant_num} plants")
        return result

    def process_plant_power_chart(self, station_id, date, plant_power_chart):
        self.log.info(f"Processing power chart for station {station_id} on {date}")
        all_entries = []
        if len(plant_power_chart) != 0:
            for i in range(len(plant_power_chart)):
                entry = plant_power_chart[i]
                ts_str = f"{date} {entry["x"]}:00"
                ts_obj = datetime.strptime(ts_str, "%Y-%m-%d %H:%M:%S")
                all_entries.append(
                    {
                        "collect_time": ts_obj,
                        "station_id": station_id,
                        "power": Decimal(entry["y"]),
                    }
                )

            power_lf = pl.LazyFrame(
                all_entries, schema=GoodweModels.station_realtime_power
            )
            result = power_lf.collect()
            self.log.info(f"Processed power chart for station {station_id} on {date}")
            return result
        return None
