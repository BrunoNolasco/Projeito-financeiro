from mysql.connector import IntegrityError
import mysql.connector as mysql
import datetime as date
dates1 = date.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

conexao = mysql.connect(
    host="localhost",
    user="Brunopy",
    password="",
    database='controle_financeiro'
)
cursor = conexao.cursor()

def opera():

    from log_in import login
    credenciais = login()
    if credenciais is None:
        exit()
    else:
        usuario_logado, senha_logada = credenciais
        cursor.execute("SELECT id FROM banco WHERE nome = %s", (usuario_logado,))
        id_banco = cursor.fetchone()[0]
        
    while True:
        print("\n")
        print("Aperte 1 para Retirar dinheiro")
        print("Aperte 2 para Depositar dinheiro")
        print("Aperte 3 para ver as últimas 5 transações")
        print("Aperte 4 para ver o seu perfil")
        print("Aperte 5 para atualizar detalhes da Conta")
        print("Aperte 6 para deletar sua Conta permanentemente: ")
        print("Aperte 7 para fazer Log Out")
        try: 
            escolha=int(input("Insira sua escolha: "))
            if(escolha>=8):
                raise TypeError ("")

        except TypeError:
            print("________________________________________________")
            print("                 Imput inválido                 ")
            print("________________________________________________")

        if(escolha==1):

            try:
                np="select saldo from banco where nome='{}'".format(usuario_logado)
                cursor.execute(np)
                bal=cursor.fetchone()[0]
            except Exception:
                print("erro")
            print("\n")
            print("________________________________ ")
            print("O seu saldo bancario é: " ,bal)
            print("_________________________________")
            print("\n")
            while True:
                try:
                    a1=int(input("Insira o quanto que deseja retirar: "))

                except ValueError:
                    print("_______________________________________________________________________ ")
                    print("                             Imput inválido                             ")
                    print("_______________________________________________________________________ ")
                    print("\n")
                    continue
                
                
                if a1<=bal:
                    creditado=0

                    t6= "update banco set saldo=GREATEST(0,saldo - '{}') where nome='{}'".format(a1,usuario_logado)
                    cursor.execute(t6)
                    conexao.commit()
                    gfn="SET FOREIGN_KEY_CHECKS=0"
                    cursor.execute(gfn)
                    conexao.commit()
                    bp = "INSERT INTO transacao (creditado, debitado, id_banco, data) VALUES (%s, %s, %s, %s)"
                    cursor.execute(bp, (creditado, a1, id_banco, dates1))
                    conexao.commit()
                    gf="SET FOREIGN_KEY_CHECKS=1"
                    cursor.execute(gf)
                    conexao.commit()
                    np9="select saldo from banco where nome='{}'".format(usuario_logado)
                    cursor.execute(np9)
                    bal1=cursor.fetchone()[0]
                    print("\n")
                    print("____________________________________________________________________")
                    print("Você," ,usuario_logado,", creditou" , a1 ,"euros no dia" , dates1)
                    print("O Saldo disponível atual é de:" , bal1, "euros.")
                    print("________________________________________________________________________")
                elif(a1>bal):

                    print("________________________________________________________________________")
                    print(             "Saldo insuficiente, por favor tente novamente!"             )
                    print("________________________________________________________________________")
                break

        elif(escolha==2): 
            debitado=0 


            while True:
                try:   
                    a11=(input("Insira o quanto quer depositar: "))
                    if a11.isalpha():
                        raise Exception("")
                    else:

                        t6= "update banco set saldo=saldo +'{}' where nome='{}'".format(a11,usuario_logado)
                        cursor.execute(t6)
                        conexao.commit()

                        mn = "INSERT INTO transacao (creditado, debitado, id_banco, data) VALUES (%s, %s, %s, %s)"
                        cursor.execute(mn, (a11, debitado, id_banco, dates1))
                        conexao.commit()

                        np9="select saldo from banco where nome='{}'".format(usuario_logado)
                        cursor.execute(np9)
                        bal2=cursor.fetchone()[0]
                        print("\n")
                        print("____________________________________________________________________")
                        print("Você," ,usuario_logado,", debitou" , a11 ,"euros no dia" , dates1)
                        print("O Saldo disponível atual é de:" , bal2, "euros.")
                        print("________________________________________________________________________")
                        break
                except TypeError:
                    print("erro")
                except IntegrityError:
                    print("erro")
        elif escolha == 3:
            prt = "SELECT creditado, debitado, data FROM transacao WHERE id_banco=%s"
            cursor.execute(prt, (id_banco,))
            linhas = cursor.fetchall()

            if linhas:
                print("_____________________________________________________________________")
                print(f"{'Creditado':>10} | {'Debitado':>10} | {'Data':>12}")
                print("_____________________________________________________________________")
                for creditado, debitado, data in linhas:
                    print(f"{creditado:>10.2f} | {debitado:>10.2f} | {data}")
                print("_____________________________________________________________________")
            else:
                print("Nenhuma transação encontrada.")

        elif escolha == 4:
            nmm = "SELECT nome, sobrenome, endereco, telefone, contribuinte, saldo FROM banco WHERE nome=%s"
            cursor.execute(nmm, (usuario_logado,))
            conta = cursor.fetchone()
            
            if conta:
                nome, sobrenome, endereco, telefone, contribuinte, saldo = conta
                
                print("______________________________________________________________________________")
                print("**************************** Detalhes da Conta ******************************")
                print("\n")
                print(f"{'Nome':<10} {'Sobrenome':<12} {'Endereço':<20} {'Telefone':<12} {'Contribuinte':<12} {'Saldo':>10}")
                print("\n")
                print(f"{nome:<10} {sobrenome:<12} {endereco:<20} {telefone:<12} {contribuinte:<12} {saldo:>10.2f}")
                print("______________________________________________________________________________")
            else:
                print("Usuário não encontrado.")

        elif(escolha==5):
            while True:
                print("\n")
                print("_____________________________________________________")
                print("                Configuração da Conta                ")
                print("_____________________________________________________")

                print("Aperte 1 para atualizar o seu Nome: ")
                print("Aperte 2 para atualizar o seu Sobrenome: ")                        
                print("Aperte 3 para atualizar a sua Senha: ")
                print("Aperte 4 para atualizar o seu Telefone: ")
                print("Aperte 5 para atualizar o seu Endereço: ")

                try:
                    escolha2=int(input("Insira sua escolha : "))
                    if(escolha2>=6):
                        raise ValueError ("")

                except Exception:
                    print("___________________________________________________")
                    print("              ****Imput inválido****               ")
                    print("___________________________________________________")
                    continue
                break
        if escolha2 == 1:
            try:
                novo_nome = input("Insira seu novo nome: ")
                ns = "UPDATE banco SET nome = %s WHERE id = %s"
                cursor.execute(ns, (novo_nome, id_banco))
                conexao.commit()
                print("_________________________________________________________________________")
                print("                     Nome atualizado com sucesso!                       ")
                print("_________________________________________________________________________")
            except Exception as e:
                print("Algo deu errado:", e)
        
        elif escolha2 == 2:
            try:
                novo_sobrenome = input("Insira seu novo Sobrenome: ")
                ns = "UPDATE banco SET sobrenome = %s WHERE id = %s"
                cursor.execute(ns, (novo_sobrenome, id_banco))
                conexao.commit()
                print("_________________________________________________________________________")
                print("                   Sobrenome atualizado com sucesso!                    ")
                print("_________________________________________________________________________")
            except Exception as e:
                print("Algo deu errado:", e)
        
        elif escolha2 == 3:
            try:
                nova_senha = input("Insira sua nova senha: ")
                ns = "UPDATE banco SET senha_hash = SHA2(%s, 256) WHERE id = %s"
                cursor.execute(ns, (nova_senha, id_banco))
                conexao.commit()
                print("_________________________________________________________________________")
                print("                  Senha atualizada com sucesso!                          ")
                print("_________________________________________________________________________")
            except Exception as e:
                print("Algo deu errado:", e)
        
        elif escolha2 == 4:
            while True:
                try:
                    novo_telefone = input("Insira o seu novo número de telefone: ")
                    if len(novo_telefone) != 9 or not novo_telefone.isdigit():
                        raise ValueError("Número inválido")
                    ns = "UPDATE banco SET telefone = %s WHERE id = %s"
                    cursor.execute(ns, (novo_telefone, id_banco))
                    conexao.commit()
                    print("_________________________________________________________________________")
                    print("                  Telefone atualizado com sucesso!                       ")
                    print("_________________________________________________________________________")
                    break
                except ValueError:
                    print("________________________________________________________")
                    print("          Insira um número válido de 9 dígitos          ")
                    print("________________________________________________________")
                    continue
                
        elif escolha2 == 5:
            try:
                novo_endereco = input("Insira o seu novo endereço: ")
                ns = "UPDATE banco SET endereco = %s WHERE id = %s"
                cursor.execute(ns, (novo_endereco, id_banco))
                conexao.commit()
                print("_________________________________________________________________________")
                print("                    Endereço atualizado com sucesso!                     ")
                print("_________________________________________________________________________")
            except Exception as e:
                print("Algo deu errado:", e)

        elif(escolha==6):
            ns="SET FOREIGN_KEY_CHECKS=0"
            cursor.execute(ns)
            conexao.commit()
            ps="delete from banco where senha_hash='{}'".format(senha_logada)
            cursor.execute(ps)
            conexao.commit()
            gs="delete from transacao where id_banco='{}'".format(id_banco)
            cursor.execute(gs)
            conexao.commit()

            ns1="SET FOREIGN_KEY_CHECKS=1"
            cursor.execute(ns1)
            conexao.commit()
            print("\n")
            print("_________________________________________________________________________")
            print("                       Conta deletada com sucesso!                       ")
            print("_________________________________________________________________________")
            print("\n")
            exit()
        elif(escolha==7):
            print("\n")
            print("____________________________________________________________________________")
            print("                  Obrigado por escolher a Personal Finance                  ")
            print("____________________________________________________________________________")
            exit()
