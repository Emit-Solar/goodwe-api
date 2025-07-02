CREATE SCHEMA IF NOT EXISTS __SCHEMA__;

CREATE TABLE IF NOT EXISTS __SCHEMA__.station_list (
    station_id TEXT PRIMARY KEY,
    station_name TEXT,
    has_inverters BOOLEAN,
    capacity DECIMAL(10, 2),
    create_date TIMESTAMPTZ,
    latitude DECIMAL(10, 7),
    longitude DECIMAL(10, 7)
);

CREATE TABLE IF NOT EXISTS __SCHEMA__.station_realtime_power (
  collect_time TIMESTAMPTZ NOT NULL,
  station_id TEXT NOT NULL,
  power DECIMAL(10, 2),
  PRIMARY KEY (collect_time, station_id)
);

SELECT create_hypertable(
  '__SCHEMA__.station_realtime_power',
  by_range ('collect_time'),
  if_not_exists => true
);
