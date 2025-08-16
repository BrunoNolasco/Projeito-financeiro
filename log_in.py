import mysql.connector as mysql

conexao = mysql.connect(
    host="localhost",
    user="Brunopy",
    password="",
    database='controle_financeiro'
)
cursor = conexao.cursor()

def login():
    try:
        usuario = input("Digite seu nome: ")
        senha = input("Digite sua senha: ")

        query = "SELECT * FROM banco WHERE nome = %s AND senha_hash = SHA2(%s, 256)"
        cursor.execute(query, (usuario, senha))
        resultado = cursor.fetchone()

        if resultado:
            print("Login efetuado com sucesso!")
            return usuario,senha
        else:
            print("\n")
            print("            Nome ou senha inválidos            ")
            print("\n")
            
    except ValueError as e:
            print(e)

