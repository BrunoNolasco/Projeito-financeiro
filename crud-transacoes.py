import mysql.connector
from datetime import date

def conectar():
    return mysql.connector.connect(
        host='localhost',
        user="Brunopy",
        password="12345678900000",
        database='controle_financeiro'
    )

# ---------- Garantir dados básicos ----------
def garantir_usuario(nome, email, senha_hash):
    db = conectar()
    cursor = db.cursor()
    cursor.execute("SELECT id FROM usuarios WHERE email=%s", (email,))
    usuario = cursor.fetchone()
    if not usuario:
        cursor.execute(
            "INSERT INTO usuarios (nome, email, senha_hash) VALUES (%s, %s, %s)",
            (nome, email, senha_hash)
        )
        db.commit()
        usuario_id = cursor.lastrowid
    else:
        usuario_id = usuario[0]
    cursor.close()
    db.close()
    return usuario_id

def garantir_categoria(nome, tipo):
    db = conectar()
    cursor = db.cursor()
    cursor.execute("SELECT id FROM categorias WHERE nome=%s", (nome,))
    categoria = cursor.fetchone()
    if not categoria:
        cursor.execute(
            "INSERT INTO categorias (nome, tipo) VALUES (%s, %s)",
            (nome, tipo)
        )
        db.commit()
        categoria_id = cursor.lastrowid
    else:
        categoria_id = categoria[0]
    cursor.close()
    db.close()
    return categoria_id

# ---------- CRUD transações ----------
def inserir_transacao(usuario_id, categoria_id, valor, data_transacao, descricao):
    db = conectar()
    cursor = db.cursor()
    cursor.execute("""
        INSERT INTO transacoes (usuario_id, categoria_id, valor, data, descricao)
        VALUES (%s, %s, %s, %s, %s)
    """, (usuario_id, categoria_id, valor, data_transacao, descricao))
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
    cursor.execute("""
        UPDATE transacoes
        SET categoria_id=%s, valor=%s, data=%s, descricao=%s
        WHERE id=%s
    """, (categoria_id, valor, data_transacao, descricao, id_transacao))
    db.commit()
    cursor.close()
    db.close()

def deletar_transacao(id_transacao):
    db = conectar()
    cursor = db.cursor()
    cursor.execute("DELETE FROM transacoes WHERE id=%s", (id_transacao,))
    db.commit()
    cursor.close()
    db.close()

# ---------- Teste ----------
if __name__ == "__main__":
    usuario_id = garantir_usuario("Bruno", "bruno@email.com", "hash_senha_exemplo")
    categoria_id = garantir_categoria("Salário", "receita")

    # Inserir nova transação
    inserir_transacao(usuario_id, categoria_id, 2500.00, date.today(), "Salário do mês")

    # Listar
    print("Transações antes da atualização:")
    for t in listar_transacoes():
        print(t)

    # Atualizar (exemplo usando o último ID inserido)
    ultima_transacao = listar_transacoes()[0][0]
    atualizar_transacao(ultima_transacao, categoria_id, 3000.00, date.today(), "Salário atualizado")

    print("\nTransações após atualização:")
    for t in listar_transacoes():
        print(t)

    # Deletar
    deletar_transacao(ultima_transacao)
    print("\nTransações após deletar:")
    for t in listar_transacoes():
        print(t)
