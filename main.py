import mysql.connector

def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="Brunopy",
        password="12345678900000",
        database='controle_financeiro'
    )

def inserir_categoria(nome, tipo):
    db = conectar()
    cursor = db.cursor()
    sql = "INSERT INTO categorias (nome, tipo) VALUES (%s, %s)"
    cursor.execute(sql, (nome, tipo))
    db.commit()
    cursor.close()
    db.close()

def listar_categorias():
    db = conectar()
    cursor = db.cursor()
    cursor.execute("SELECT id, nome, tipo FROM categorias")
    resultados = cursor.fetchall()
    cursor.close()
    db.close()
    return resultados

if __name__ == "__main__":
    inserir_categoria("Salário", "receita")
    inserir_categoria("Alimentação", "despesa")
    categorias = listar_categorias()
    for cat in categorias:
        print(cat)