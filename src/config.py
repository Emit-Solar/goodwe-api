import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    GOODWE_USERNAME = os.getenv("GOODWE_USERNAME")
    GOODWE_PASSWORD = os.getenv("GOODWE_PASSWORD")
    GOODWE_API_URL = "http://www.goodwe-power.com:82/api/v3"
    DEFAULT_HEADERS = {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    POSTGRES_IP = os.getenv("POSTGRES_IP")
    POSTGRES_PORT = os.getenv("POSTGRES_PORT")
    POSTGRES_DB = os.getenv("POSTGRES_DB")
    POSTGRES_USERNAME = os.getenv("POSTGRES_USERNAME")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
