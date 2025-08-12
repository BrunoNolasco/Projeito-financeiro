import sqlite3
conn = sqlite3.connect("dados_financeiros.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS transacoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    descricao TEXT NOT NULL,
    valor REAL NOT NULL,
    data TEXT NOT NULL
)
""")
conn.commit()
conn.close()
