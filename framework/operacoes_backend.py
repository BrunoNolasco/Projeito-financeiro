import datetime as date
from db import get_connection
from login_backend import login

def opera():
    conexao = get_connection()
    cursor = conexao.cursor()

    credenciais = login()
    if credenciais is None:
        return
    else:
        usuario_logado, senha_logada = credenciais
        cursor.execute("SELECT id FROM banco WHERE nome = %s", (usuario_logado,))
        id_banco = cursor.fetchone()[0]

    while True:
        print("\n1 - Retirar dinheiro")
        print("2 - Depositar dinheiro")
        print("3 - Últimas 5 transações")
        print("4 - Ver perfil")
        print("5 - Atualizar conta")
        print("6 - Deletar conta")
        print("7 - Log Out")

        escolha = input("Escolha: ")

        if escolha == "1":
            retirar(conexao, cursor, usuario_logado, id_banco)

        elif escolha == "2":
            depositar(conexao, cursor, usuario_logado, id_banco)

        elif escolha == "3":
            ver_transacoes(cursor, id_banco)

        elif escolha == "4":
            ver_perfil(cursor, usuario_logado)

        elif escolha == "5":
            atualizar(conexao, cursor, id_banco)

        elif escolha == "6":
            deletar(conexao, cursor, id_banco)

        elif escolha == "7":
            print("Log out feito. Até logo!")
            break

        else:
            print("Opção inválida.")

    cursor.close()
    conexao.close()

# --- Funções auxiliares ---
def retirar(conexao, cursor, usuario_logado, id_banco):
    valor = int(input("Quanto deseja retirar? "))
    cursor.execute("SELECT saldo FROM banco WHERE nome=%s", (usuario_logado,))
    saldo = cursor.fetchone()[0]

    if valor <= saldo:
        cursor.execute("UPDATE banco SET saldo = saldo - %s WHERE nome=%s", (valor, usuario_logado))
        conexao.commit()
        cursor.execute("INSERT INTO transacao (creditado, debitado, id_banco, data) VALUES (%s,%s,%s,%s)",
                       (0, valor, id_banco, date.datetime.now()))
        conexao.commit()
        print(f"Retirada de {valor} realizada.")
    else:
        print("Saldo insuficiente.")

def depositar(conexao, cursor, usuario_logado, id_banco):
    valor = int(input("Quanto deseja depositar? "))
    cursor.execute("UPDATE banco SET saldo = saldo + %s WHERE nome=%s", (valor, usuario_logado))
    conexao.commit()
    cursor.execute("INSERT INTO transacao (creditado, debitado, id_banco, data) VALUES (%s,%s,%s,%s)",
                   (valor, 0, id_banco, date.datetime.now()))
    conexao.commit()
    print(f"Depósito de {valor} realizado.")

def ver_transacoes(cursor, id_banco):
    cursor.execute("SELECT creditado, debitado, data FROM transacao WHERE id_banco=%s ORDER BY data DESC LIMIT 5", (id_banco,))
    linhas = cursor.fetchall()
    if linhas:
        for c, d, dt in linhas:
            print(f"Cred: {c}, Deb: {d}, Data: {dt}")
    else:
        print("Nenhuma transação encontrada.")

def ver_perfil(cursor, usuario_logado):
    cursor.execute("SELECT nome, sobrenome, endereco, telefone, contribuinte, saldo FROM banco WHERE nome=%s", (usuario_logado,))
    conta = cursor.fetchone()
    if conta:
        print("Perfil:", conta)
    else:
        print("Usuário não encontrado.")

def atualizar(conexao, cursor, id_banco):
    novo_nome = input("Digite novo nome: ")
    cursor.execute("UPDATE banco SET nome=%s WHERE id=%s", (novo_nome, id_banco))
    conexao.commit()
    print("Nome atualizado!")

def deletar(conexao, cursor, id_banco):
    confirm = input("Tem certeza que deseja deletar a conta? (sim/não): ").lower()
    if confirm == "sim":
        cursor.execute("DELETE FROM transacao WHERE id_banco=%s", (id_banco,))
        conexao.commit()
        cursor.execute("DELETE FROM banco WHERE id=%s", (id_banco,))
        conexao.commit()
        print("Conta deletada.")
