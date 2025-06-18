import polars as pl


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
