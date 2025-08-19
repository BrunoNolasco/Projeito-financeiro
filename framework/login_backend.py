import mysql.connector as mysql
from db import get_connection

def login(nome, senha):
    try:
        conexao = get_connection()
        cursor = conexao.cursor()
        query = "SELECT * FROM banco WHERE nome = %s AND senha_hash = SHA2(%s, 256)"
        cursor.execute(query, (nome, senha))
        resultado = cursor.fetchone()
        return resultado is not None
    finally:
        cursor.close()
        conexao.close()
