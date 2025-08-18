import mysql.connector as mysql

conexao = mysql.connect(
    host="localhost",
    user="Brunopy",
    password="",
    database='controle_financeiro'
)
cursor = conexao.cursor()

def login(usuario, senha):
    query = "SELECT * FROM banco WHERE nome = %s AND senha_hash = SHA2(%s, 256)"
    cursor.execute(query, (usuario, senha))
    resultado = cursor.fetchone()
    return resultado is not None

def signup(nome, sobrenome, senha, telefone, endereco):
    try:
        query = """INSERT INTO banco (nome, sobrenome, senha_hash, telefone, endereco)
                   VALUES (%s, %s, SHA2(%s, 256), %s, %s)"""
        cursor.execute(query, (nome, sobrenome, senha, telefone, endereco))
        conexao.commit()
        return True
    except Exception as e:
        print("Erro no signup:", e)
        return False
