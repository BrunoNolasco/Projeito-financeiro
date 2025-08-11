from db_config import get_connection

def listar_categorias():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM categorias")
    categorias = cursor.fetchall()
    conn.close()
    return categorias

def adicionar_categoria(nome, tipo):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO categorias (nome, tipo) VALUES (%s, %s)",
        (nome, tipo)
    )
    conn.commit()
    conn.close()