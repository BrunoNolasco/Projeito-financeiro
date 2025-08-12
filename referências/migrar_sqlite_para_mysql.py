import sqlite3
import mysql.connector


sqlite_conn = sqlite3.connect("dados_financeiros.db")
sqlite_cursor = sqlite_conn.cursor()


mysql_conn = mysql.connector.connect(
    host="localhost",
    user="Brunopy",
    password="12345678900000",
    database='controle_financeiro'
)
mysql_cursor = mysql_conn.cursor()

sqlite_cursor.execute("SELECT nome, email, senha FROM usuarios")
for row in sqlite_cursor.fetchall():
    mysql_cursor.execute("""
        INSERT INTO usuarios (nome, email, senha) VALUES (%s, %s, %s)
    """, row)


sqlite_cursor.execute("SELECT usuario_id, descricao, valor, data, tipo FROM transacoes")
for row in sqlite_cursor.fetchall():
    mysql_cursor.execute("""
        INSERT INTO transacoes (usuario_id, descricao, valor, data, tipo)
        VALUES (%s, %s, %s, %s, %s)
    """, row)

mysql_conn.commit()

sqlite_cursor.close()
sqlite_conn.close()
mysql_cursor.close()
mysql_conn.close()

print("Migração concluída com sucesso!")
