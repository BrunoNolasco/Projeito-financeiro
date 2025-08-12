import mysql.connector


conn = mysql.connector.connect(
    host="localhost",
    user="Brunopy",
    password="12345678900000",
    database='controle_financeiro'
)
cursor = conn.cursor()


cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    senha VARCHAR(100) NOT NULL
);
""")


cursor.execute("""
CREATE TABLE IF NOT EXISTS transacoes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    descricao VARCHAR(255) NOT NULL,
    valor DECIMAL(10,2) NOT NULL,
    data DATE NOT NULL,
    tipo ENUM('entrada', 'saida') NOT NULL,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);
""")

conn.commit()
cursor.close()
conn.close()

print("Tabelas criadas no MySQL com sucesso!")
