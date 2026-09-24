import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "development-secret-key"
    )

    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

# import os

# class Config:
#     SECRET_KEY = os.environ.get("SECRET_KEY", "change-this-secret-key")
#     SQLALCHEMY_DATABASE_URI = os.environ.get(
#         "DATABASE_URL",
#         "mysql+pymysql://students:password@localhost/edusupport"
#     )
#     SQLALCHEMY_TRACK_MODIFICATIONS = False
