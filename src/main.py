from .goodwe_client import GoodWeClient
from .config import Config
from .logger import Logger
from .data_processor import GoodweDataProcessor
from .db_client import SQLClient


def initialization(log_file):
    log = Logger(f"logs/{log_file}", clear=True)
    api_client = GoodWeClient(
        Config.GOODWE_USERNAME,
        Config.GOODWE_PASSWORD,
        Config.GOODWE_API_URL,
        Config.DEFAULT_HEADERS,
        log,
    )

    sql_client = SQLClient(
        Config.POSTGRES_DB,
        Config.POSTGRES_USERNAME,
        Config.POSTGRES_PASSWORD,
        Config.POSTGRES_IP,
        Config.POSTGRES_PORT,
        Config.POSTGRES_SCHEMA,
        Config.POSTGRES_SETUP,
        log,
    )

    dtp = GoodweDataProcessor(log)

    return log, api_client, sql_client, dtp
