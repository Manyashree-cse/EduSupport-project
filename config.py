# import os
# from dotenv import load_dotenv

# load_dotenv()


# class Config:
#     SECRET_KEY = os.getenv(
#         "SECRET_KEY",
#         "development-secret-key"
#     )

#     SQLALCHEMY_DATABASE_URI = os.getenv(
#         "DATABASE_URL"
#     )

#     SQLALCHEMY_TRACK_MODIFICATIONS = False


import os
from dotenv import load_dotenv

load_dotenv()

database_url = os.getenv("DATABASE_URL")

# Railway may provide mysql://
# Convert it to the PyMySQL driver
if database_url and database_url.startswith("mysql://"):
    database_url = database_url.replace(
        "mysql://",
        "mysql+pymysql://",
        1
    )

class Config:
    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "development-secret-key"
    )

    SQLALCHEMY_DATABASE_URI = database_url

    SQLALCHEMY_TRACK_MODIFICATIONS = False