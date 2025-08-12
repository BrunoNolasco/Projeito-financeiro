import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="Brunopy",
        password="12345678900000",
        database='controle_financeiro'
    )
