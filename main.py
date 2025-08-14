import mysql.connector as mysql

conexao = mysql.connect(
        host="localhost",
        user="Brunopy",
        password="",
        database='controle_financeiro'
    )
cursor = conexao.cursor()

cursor.execute("select * from usuarios")
resultado = cursor.fetchall()
