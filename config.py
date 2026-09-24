import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "development-secret-key"
    )

    _database_url = os.getenv("DATABASE_URL")
    if _database_url and _database_url.startswith("mysql://"):
        _database_url = _database_url.replace(
            "mysql://", "mysql+pymysql://", 1
        )

    SQLALCHEMY_DATABASE_URI = _database_url

    SQLALCHEMY_TRACK_MODIFICATIONS = False


