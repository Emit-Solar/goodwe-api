import polars as pl


class GoodweModels:
    station_realtime_power = {
        "collect_time": pl.Datetime,
        "station_id": pl.Utf8,
        "power": pl.Decimal(10, 2),
    }
