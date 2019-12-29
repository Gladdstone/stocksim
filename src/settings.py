import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
TRADIER_API_KEY = os.environ.get("TRADIER_API_KEY")
HOST = os.environ.get("HOST")
PORT = os.environ.get("PORT")
PSQL_DATABASE = os.environ.get("PSQL_DATABASE")
PSQL_USER = os.environ.get("PSQL_USER")
PSQL_PASSWORD = os.environ.get("PSQL_PASSWORD")
