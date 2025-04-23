import psycopg2
from psycopg2 import sql


class PostgreSQLClient:
    def __init__(self, host, username, password, database, schema, log, port=5432):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.database = database
        self.schema = schema

        self.log = log

        self.connect()
        self.create_schema()
        self.create_tables()

    def connect(self):
        self.log.info("Connecting to PostgreSQL database...")
        try:
            self.connection = psycopg2.connect(
                host=self.host,
                port=self.port,
                user=self.username,
                password=self.password,
                database=self.database,
            )
            self.cursor = self.connection.cursor()
            self.log.info("PostgreSQL connection established")
        except Exception as e:
            self.log.exception("Failed to connect to PostgreSQL", e)
            raise e

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
            self.log.info("PostgreSQL connection closed")

    def create_schema(self):
        self.cursor.execute(
            sql.SQL("CREATE SCHEMA IF NOT EXISTS {}").format(
                sql.Identifier(self.schema)
            )
        )
        self.connection.commit()
        self.log.info(f"Schema {self.schema} created or already exists")

    def create_tables(self):
        self.cursor.execute(
            sql.SQL("""
                CREATE TABLE IF NOT EXISTS {}.plant_list (
                    plant_id TEXT PRIMARY KEY,
                    plant_name TEXT,
                    classification TEXT,
                    plant_types TEXT,
                    capacity NUMERIC,
                    create_date DATE,
                    latitude NUMERIC,
                    longitude NUMERIC
                )
            """).format(sql.Identifier(self.schema))
        )

        self.connection.commit()
        self.log.info(f"Table {self.schema}.plant_list created or already exists")

    def insert_plant(self, plant_data):
        try:
            query = sql.SQL("""
                INSERT INTO {}.plant_list (
                    plant_id, plant_name, classification, plant_types,
                    capacity, create_date, latitude, longitude
                ) VALUES (
                    %(plantId)s, %(plantName)s, %(classification)s, %(plantTypes)s,
                    %(capacity)s, %(createDate)s, %(latitude)s, %(longitude)s
                )
                ON CONFLICT (plant_id) DO UPDATE SET
                    plant_name = EXCLUDED.plant_name,
                    classification = EXCLUDED.classification,
                    plant_types = EXCLUDED.plant_types,
                    capacity = EXCLUDED.capacity,
                    create_date = EXCLUDED.create_date,
                    latitude = EXCLUDED.latitude,
                    longitude = EXCLUDED.longitude;
            """).format(sql.Identifier(self.schema))

            self.cursor.execute(query, plant_data)
            self.connection.commit()
            self.log.info(f"Inserted/Updated plant data: {plant_data['plantId']}")

        except Exception as e:
            self.connection.rollback()
            self.log.exception("Failed to insert plant data", e)
            raise e
