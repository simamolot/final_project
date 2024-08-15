import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()


def get_read_connection():
    db_config = {
        'host': os.getenv('DB_HOST_R'),
        'user': os.getenv('DB_USER_R'),
        'password': os.getenv('DB_PASSWORD_R'),
        'database': os.getenv('DB_DATA_R')
    }
    return mysql.connector.connect(**db_config)


def get_write_connection():
    db_config = {
        'host': os.getenv('DB_HOST_W'),
        'user': os.getenv('DB_USER_W'),
        'password': os.getenv('DB_PASSWORD_W'),
        'database': os.getenv('DB_DATA_W')
    }
    return mysql.connector.connect(**db_config)
