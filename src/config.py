import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    GOODWE_USERNAME = os.getenv("GOODWE_USERNAME")
    GOODWE_PASSWORD = os.getenv("GOODWE_PASSWORD")
    GOODWE_API_URL = "http://hk.semsportal.com:82/api/"
    DEFAULT_HEADERS = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "secret": "",
        "token": "",
    }

    POSTGRES_IP = os.getenv("POSTGRES_IP")
    POSTGRES_PORT = os.getenv("POSTGRES_PORT")
    if POSTGRES_PORT:
        POSTGRES_PORT = int(POSTGRES_PORT)
    POSTGRES_DB = os.getenv("POSTGRES_DB")
    POSTGRES_SCHEMA = os.getenv("POSTGRES_SCHEMA")
    POSTGRES_USERNAME = os.getenv("POSTGRES_USERNAME")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_SETUP = os.getenv("POSTGRES_SETUP")
