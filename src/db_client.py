import polars as pl
from sqlalchemy import create_engine, MetaData, Table, text
from sqlalchemy.dialects.postgresql import insert


class SQLClient:
    def __init__(self, database, user, password, host, port, schema, setup_file, log):
        self.database = database
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.schema = schema
        self.setup_file = setup_file
        self.log = log

        self.engine = self.connect()

        self._setup()

    def connect(self):
        self.log.info("Connecting to PostgreSQL database...")
        try:
            engine = create_engine(
                f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"
            )
            self.log.info("PostgreSQL connection established")
            return engine
        except Exception as e:
            self.log.exception("Failed to connect to PostgreSQL", e)
            raise e

    def _setup(self):
        self.log.info("Setting up database schema...")
        try:
            with open(self.setup_file, "r") as f:
                setup_sql = f.read()
            setup_sql = setup_sql.replace("__SCHEMA__", self.schema)

            stmts = [s.strip() for s in setup_sql.split(";") if s.strip()]
            with self.engine.connect() as conn:
                for stmt in stmts:
                    conn.execute(text(stmt))
                conn.commit()
            self.log.info("Database schema setup completed")
        except FileNotFoundError:
            self.log.error(f"Setup file {self.setup_file} not found")
            raise
        except Exception as e:
            self.log.exception("Failed to setup database schema", e)
            raise e

    def execute_query(self, query, params=None):
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text(query), params)
                return result.fetchall()
        except Exception as e:
            self.log.exception("Failed to execute query", e)
            raise e

    def upsert_data(
        self,
        df: pl.DataFrame,
        table_name: str,
        primary_keys: list[str],
    ):
        try:
            stmt = insert(
                table=Table(
                    table_name,
                    MetaData(),
                    schema=self.schema,
                    autoload_with=self.engine,
                )
            ).values(df.to_pandas().to_dict(orient="records"))
            stmt = stmt.on_conflict_do_update(
                index_elements=primary_keys, set_=stmt.excluded
            )
            with self.engine.connect() as conn:
                conn.execute(stmt)
                conn.commit()
            self.log.info(f"Data upserted successfully to {self.schema}.{table_name}")
        except Exception as e:
            self.log.exception(
                f"Failed to upsert data to {self.schema}.{table_name}", e
            )
            raise e

    def close(self):
        if self.engine:
            self.engine.dispose()
