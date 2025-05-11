import psycopg2
from psycopg2 import sql
import re


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

    def _flatten_dict(self, json_dict, parent_col="", columns=None):
        """
        Returns columns, types, and values from JSON dictionary.
        """

        data = {}
        if columns is None:
            columns = {}
        for k, v in json_dict.items():
            k_split = re.split(r"(?=[A-Z])", k)
            k_fmt = "_".join(k_split)
            col_name = (f"{parent_col}_{k_fmt}" if parent_col else k_fmt).lower()
            col_type = "TEXT"

            if isinstance(v, dict):
                self._flatten_dict(v, parent_col=col_name, columns=columns)
            elif isinstance(v, int):
                col_type = "INT"
            elif isinstance(v, float):
                col_type = "NUMERIC"

            columns[col_name] = col_type
            data[col_name] = v

        return columns, data

    def create_table(self, table_name, json_dict):
        columns, _ = self._flatten_dict(json_dict)

        columns_str = ",\n".join([f"{k} {v}" for k, v in columns.items()])

        create_query = sql.SQL(
            """
            CREATE TABLE IF NOT EXISTS {}.{} (
                id SERIAL PRIMARY KEY,
                {}
            )
            """
        ).format(
            sql.Identifier(self.schema),
            sql.Identifier(table_name),
            sql.SQL(columns_str),
        )

        self.cursor.execute(create_query)
        self.connection.commit()
        self.log.info(
            f"Table {table_name} created or already exists in schema {self.schema}"
        )

    def insert_data(self, table_name, json_data):
        _, data = self._flatten_dict(json_data)
        insert_query = sql.SQL(
            """
            INSERT INTO {}.{} ({})
            VALUES ({})
            ON CONFLICT DO NOTHING
            """
        ).format(
            sql.Identifier(self.schema),
            sql.Identifier(table_name),
            sql.SQL(", ").join(sql.Identifier(k) for k in data.keys()),
            sql.SQL(", ").join(sql.Placeholder() * len(data)),
        )

        try:
            self.cursor.execute(insert_query, tuple(data.values()))
            self.connection.commit()
            self.log.info(f"Data inserted into {table_name}")
        except Exception as e:
            self.connection.rollback()
            self.log.exception(f"Failed to insert data into {table_name}", e)
            raise e
