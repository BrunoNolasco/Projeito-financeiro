from db_config import get_connection

def listar_usuarios():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios")
    usuarios = cursor.fetchall()
    conn.close()
    return usuarios

def adicionar_usuario(nome, email, senha_hash):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO usuarios (nome, email, senha_hash) VALUES (%s, %s, %s)",
        (nome, email, senha_hash)
    )
    conn.commit()
    conn.close()
