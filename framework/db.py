import mysql.connector as mysql

def get_connection():
    return mysql.connect(
        host="localhost",
        user="Brunopy",
        password="",
        database="controle_financeiro"
    )
