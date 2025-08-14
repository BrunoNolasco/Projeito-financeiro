import mysql.connector as mysql
import datetime as date

SpecialSym = ['$', '@', '#', '%']

conexao = mysql.connect(
    host="localhost",
    user="Brunopy",
    password="",
    database='controle_financeiro'
)
cursor = conexao.cursor()

def signup():
    
    conexao = mysql.connect(
        host="localhost",
        user="Brunopy",
        password="",
        database="controle_financeiro"
    )
    cursor = conexao.cursor()
    
    while True:
        try: 
            a='.'
            a1='#'
            a2='$'
            a3='*'
            a4='&'
            a5='='
            a6=','
            a7='@'
            a8='?'
            a9='/'
            ut=input("Introduza o seu nome: ")
            if (a in ut) or (a2 in ut) or (a1 in ut) or (a3 in ut) or (a4 in ut) or (a5 in ut) or (a6 in ut) or (a7 in ut) or (a8 in ut) or (a9 in ut):
                raise TypeError 
            break
        except TypeError:
            print("Caracteres especiais como . , @ # < > ? / ; não são aceitos.")
            
        # --- Sobrenome ---
    while True:
        try:
            a='.'
            a1='#'
            a2='$'
            a3='*'
            a4='&'
            a5='='
            a6=','
            a7='@'
            a8='?'
            a9='/'
            p=input("Introduza o seu sobrenome: ")
            if (a in p) or (a2 in p) or (a1 in p) or (a3 in p) or (a4 in p) or (a5 in p) or (a6 in p) or (a7 in p) or (a8 in p) or (a9 in p):
                raise TypeError 
            break
        except TypeError:
            print("Caracteres especiais como . , @ # < > ? / ; não são aceitos.")
            
        # --- Senha ---
    while True:
        try:
            z = input("Introduza a sua Password: ")
            if len(z) < 6:
                raise ValueError
            if not any(char.isdigit() for char in z):
                raise ValueError
            if not any(char.isupper() for char in z):
                raise ValueError
            if not any(char.islower() for char in z):
                raise ValueError
            if not any(char in SpecialSym for char in z):
                raise ValueError
            break
        except ValueError:
            print("A senha deve conter 1 letra maiúscula, 1 letra minúscula, 1 número, 1 caracter especial e pelo menos 6 caracteres.")
            
        # --- Depósito de abertura ---
        k = str(input("Introduza quanto dinheiro pretende depositar: "))
        
        # --- Data de nascimento ---
    while True:
        try:
            a = input("Introduza sua data de nascimento (DD/MM/AAAA): ")
            nascimento = date.datetime.strptime(a, "%d/%m/%Y").date()
            break
        except ValueError:
            print("Formato inválido. Use DD/MM/AAAA.")
            
        # --- Endereço ---
        s = input("Introduza seu endereço: ")
        
        # --- Telefone ---
    while True:
        try:
            d = input("Introduza seu número de telefone: ")
            if len(d) != 9 or not d.isdigit():
                raise ValueError("Número de telefone inválido")
            break
        except ValueError as m:
            print(m)
            
        # --- Contribuinte ---
    while True:
        try:
            f = input("Introduza seu contribuinte: ")
            if len(f) != 9 or not f.isdigit():
                raise ValueError("Contribuinte inválido")
            break
        except ValueError as m:
            print(m)
            
        # --- Inserir no banco ---
        query = """
        INSERT INTO banco (nome, sobrenome, senha_hash, deposito_abertura, nascimento, endereço, telefone, contribuinte)
        VALUES (%s, %s, SHA2(%s, 256), %s, %s, %s, %s, %s)
        """
        valores = (ut, p, z, k, nascimento, s, d, f)
        cursor.execute(query, valores)
        conexao.commit()
        print("\n")
        print("_________________________________________________________________________")
        print("          Sua conta na Personal Finance foi criada com sucesso!          ")
        print("_________________________________________________________________________")
        print("\n")

cursor.close()
conexao.close()
