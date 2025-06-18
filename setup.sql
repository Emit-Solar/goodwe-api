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

CREATE TABLE IF NOT EXISTS __SCHEMA__.inverter_list(
    inverter_sn TEXT PRIMARY KEY,
    model TEXT,
    check_code TEXT,
    capacity DECIMAL(10, 2),
    firmware_version TEXT
);

CREATE TABLE IF NOT EXISTS __SCHEMA__.station_realtime_info(
    collect_time TIMESTAMPTZ,
    station_id TEXT,
    status INT NOT NULL,
    month_generation DECIMAL(10, 2),
    pac DECIMAL(10, 2),
    day_power DECIMAL(10, 2),
    total_power DECIMAL(10, 2),
    day_income DECIMAL(10, 2),
    total_income DECIMAL(10, 2),
    yield_rate DECIMAL(10, 2),
    co2 DECIMAL(10, 2),
    tree DECIMAL(10, 2),
    coal DECIMAL(10, 2),
    powercontrol_status INT
);

SELECT create_hypertable(
    '__SCHEMA__.station_realtime_info',
    by_range ('collect_time'),
    if_not_exists => true
);

CREATE TABLE IF NOT EXISTS __SCHEMA__.inverter_realtime_info (
    collect_time TIMESTAMPTZ,
    inverter_sn TEXT,
    in_pac DECIMAL(10, 2),
    out_pac DECIMAL(10, 2),
    eday DECIMAL(10, 2),
    emonth DECIMAL(10, 2),
    etotal DECIMAL(10, 2),
    status INT NOT NULL,
    temperature DECIMAL(10, 2),
    pv_input_1 TEXT,
    pv_input_2 TEXT,
    output_voltage DECIMAL(10, 2),
    output_current DECIMAL(10, 2),
    output_power DECIMAL(10, 2),
    total_generation DECIMAL(10, 2),
    daily_generation DECIMAL(10, 2),
    warning_code TEXT,
    dc_input1 TEXT,
    dc_input2 TEXT,
    vpv1 DECIMAL(10, 2),
    vpv2 DECIMAL(10, 2),
    ipv1 DECIMAL(10, 2),
    ipv2 DECIMAL(10, 2),
    vac1 DECIMAL(10, 2),
    vac2 DECIMAL(10, 2),
    vac3 DECIMAL(10, 2),
    iac1 DECIMAL(10, 2),
    iac2 DECIMAL(10, 2),
    iac3 DECIMAL(10, 2),
    fac1 DECIMAL(10, 2),
    fac2 DECIMAL(10, 2),
    grid_voltage DECIMAL(10, 2),
    h_total DECIMAL(10, 2)
);

SELECT create_hypertable(
  '__SCHEMA__.inverter_realtime_info',
  by_range ('collect_time'),
  if_not_exists => true
);


CREATE TABLE IF NOT EXISTS __SCHEMA__.station_realtime_power (
  collect_time TIMESTAMPTZ,
  station_id TEXT,
  power DECIMAL(10, 2)
);

SELECT create_hypertable(
  '__SCHEMA__.station_realtime_power',
  by_range ('collect_time'),
  if_not_exists => true
);
