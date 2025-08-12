import sqlite3

# Conectar ao banco SQLite
sqlite_conn = sqlite3.connect("dados_financeiros.db")
cursor = sqlite_conn.cursor()

# Listar tabelas
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tabelas = cursor.fetchall()

print("Tabelas no SQLite:")
for tabela in tabelas:
    print("-", tabela[0])

sqlite_conn.close()
