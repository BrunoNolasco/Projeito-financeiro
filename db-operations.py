import mysql.connector
from datetime import date

def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="Brunopy",
        password="12345678900000",
        database='controle_financeiro'
    )

def inserir_transacao(usuario_id, categoria_id, valor, data_transacao, descricao):
    db = conectar()
    cursor = db.cursor()
    sql = """
    INSERT INTO transacoes (usuario_id, categoria_id, valor, data, descricao)
    VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(sql, (usuario_id, categoria_id, valor, data_transacao, descricao))
    db.commit()
    cursor.close()
    db.close()

def listar_transacoes():
    db = conectar()
    cursor = db.cursor()
    cursor.execute("""
    SELECT t.id, u.nome, c.nome, t.valor, t.data, t.descricao
    FROM transacoes t
    JOIN usuarios u ON t.usuario_id = u.id
    JOIN categorias c ON t.categoria_id = c.id
    ORDER BY t.data DESC
    """)
    resultados = cursor.fetchall()
    cursor.close()
    db.close()
    return resultados

def atualizar_transacao(id_transacao, categoria_id, valor, data_transacao, descricao):
    db = conectar()
    cursor = db.cursor()
    sql = """
    UPDATE transacoes
    SET categoria_id=%s, valor=%s, data=%s, descricao=%s
    WHERE id=%s
    """
    cursor.execute(sql, (categoria_id, valor, data_transacao, descricao, id_transacao))
    db.commit()
    cursor.close()
    db.close()

def deletar_transacao(id_transacao):
    db = conectar()
    cursor = db.cursor()
    sql = "DELETE FROM transacoes WHERE id=%s"
    cursor.execute(sql, (id_transacao,))
    db.commit()
    cursor.close()
    db.close()

if __name__ == "__main__":
    # Exemplo de uso:
    # Inserir uma transação
    inserir_transacao(1, 1, 2500.00, date.today(), "Salário do mês")
    # Listar todas
    transacoes = listar_transacoes()
    for t in transacoes:
        print(t)
