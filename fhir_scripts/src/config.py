# POSTGRES DB Config #
import os

POSTGRES_HOST = os.environ.get("POSTGRES_HOST")
POSTGRES_PORT = int(os.environ.get("POSTGRES_PORT"))
POSTGRES_DB = os.environ.get("POSTGRES_DB")
POSTGRES_USER = os.environ.get("POSTGRES_USER")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
