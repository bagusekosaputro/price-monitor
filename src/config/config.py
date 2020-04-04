import configparser
import os

from pathlib import Path 
from dotenv import load_dotenv


class Config:
    env_path = Path("/app/.env")
    load_dotenv(dotenv_path=env_path)
    # App Environment
    FLASK_ENV = os.environ.get('flask_env')
    FLASK_DEBUG = os.environ.get('flask_debug')

    db_host = os.environ.get('db_host')
    db_user = os.environ.get('db_user')
    db_pass = os.environ.get('db_password')
    db_port = os.environ.get('db_port')
    db_name = os.environ.get('db_name')
    
    SQLALCHEMY_DATABASE_URI = f"mysql://{db_user}:{db_pass}@product_db:{db_port}/{db_name}"

    SQLALCHEMY_TRACK_MODIFICATIONS = False