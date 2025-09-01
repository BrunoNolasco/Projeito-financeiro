import mysql.connector

DB_CONFIG = {
    "host": "localhost",
    "user": "Brunopy",
    "password": "",
    "database": "controle_financeiro",
    "autocommit": False,
}

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)