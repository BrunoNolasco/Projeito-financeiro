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
                    bp="insert into transacao values('{}','{}','{}','{}')".format(creditado,a1,usuario_logado,dates1)
                    cursor.execute(bp)
                    conexao.commit()
                    gf="SET FOREIGN_KEY_CHECKS=1"
                    cursor.execute(gf)
                    conexao.commit()
                    np9="select saldo from banco where nome='{}'".format(usuario_logado)
                    cursor.execute(np9)
                    bal1=cursor.fetchone()[0]
                    print("\n")
                    print("____________________________________________________________________")
                    print("Você, " ,usuario_logado , "debitou " , a1 ,"no dia " , dates1)
                    print("O Saldo disponível atual é de: " , bal1, "")
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

                        mn="insert into transacao values('{}','{}','{}','{}')".format(a11,debitado,usuario_logado,dates1)
                        cursor.execute(mn)
                        conexao.commit()
                        np9="select saldo from banco where nome='{}'".format(usuario_logado)
                        cursor.execute(np9)
                        bal2=cursor.fetchone()[0]
                        print("\n")
                        print("____________________________________________________________________")
                        print("Você, " ,usuario_logado , "creditou" , a11 ,"no dia " , dates1)
                        print("O Saldo disponível atual é de: " , bal2, "")
                        print("________________________________________________________________________")
                        break
                except TypeError:
                    print("erro")
                except IntegrityError:
                    print("erro")
        elif(escolha==3):
            prt="Select creditado,debitado,data from transacao where nome1='{}'".format(usuario_logado)
            cursor.execute(prt)
            print("______________________________________________________________________________")
            print("*************** Os detalhes da transação são *********************")
            print("\n")
            for i in cursor:
                print("___________________________________________________________________________")
                print("creditado , debitado : " ,i)
                print("___________________________________________________________________________")
        elif(escolha==4):
            nmm="Select nome, sobrenome, senha_hash, endereco, telefone, contribuinte, saldo from banco where nome='{}'".format(usuario_logado)
            cursor.execute(nmm)
            print("______________________________________________________________________________")
            print("**************************** Detalhes da Conta ******************************")
            print("______________________________________________________________________________")
            print("\n")
            print("_______________________________________________________________________________")
            print("    Nome      Sobrenome    Endereço     Telefone \t   Contribuinte    Saldo")
            print("_______________________________________________________________________________")
            print("\n")
            for i in cursor:
                print("______________________________________________________________________________")
                print(i)
                print("______________________________________________________________________________")
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
            if(escolha2==1):
                try:
                    novo_nome=input ("Insira seu novo nome: ")
                    ns="update banco set novo_nome='{}' where senha_hash='{}'".format(novo_nome,senha_logada)

                    cursor.execute(ns)
                    conexao.commit()
                    print("_________________________________________________________________________")
                    print ("                     Nome atualizado com sucesso!                       ")
                    print("_________________________________________________________________________")
                except IndexError:
                    print("Algo deu errado")
            elif(escolha2==2):
                try:
                    gf="SET FOREIGN_KEY_CHECKS=0"
                    cursor.execute(gf)
                    conexao.commit()
                    mp=input("Insira seu novo Sobrenome: ")
                    novo_sobrenome="update banco set novo_sobrenome='{}' where nome='{}'".format(mp,usuario_logado)
                    cursor.execute(novo_sobrenome)
                    conexao.commit()
                    print("_________________________________________________________________________")
                    print ("                   Sobrenome atualizado com sucesso!                    ")
                    print("_________________________________________________________________________")

                    gf1="SET FOREIGN_KEY_CHECKS=1"
                    cursor.execute(ns)
                    conexao.commit(gf1)

                except Exception:
                    print("")
            elif(escolha2==3):
                try:
                    nova_senha=input("Insira sua nova senha: ")
                    us="update banco set nova_senha='{}' where nome='{}'".format(nova_senha,usuario_logado)
                    cursor.execute(us)
                    conexao.commit()
                    print ("          Senha atualizada com sucesso!          ")
                except IndexError:
                    print("Algo deu errado")
            elif(escolha2==4):
                while True:
                    try:
                        novo_telefone=(input("Insira o seu novo número de telefone: "))
                        if(len(novo_telefone)!=9) or novo_telefone.isalpha():
                            raise ValueError ("")


                        us="update banco set telefone='{}' where  nome='{}'".format(novo_telefone,usuario_logado)
                        cursor.execute(us)
                        conexao.commit()
                        print("_________________________________________________________________________")
                        print ("                  Telefone foi atualizado com sucesso!                  ")
                        print("_________________________________________________________________________")

                    except ValueError:
                        print("________________________________________________________")
                        print("          Insira um número válido de 9 dígitos          ")
                        print("________________________________________________________")
                        print("\n")
                        continue
                    break
                
            elif(escolha2==5):
                try:
                    novo_endereco=input("Insira o seu novo endereco: ")
                    ns1="update banco set endereco='{}' where nome='{}'".format(novo_endereco,usuario_logado)
                    cursor.execute(ns1)
                    conexao.commit()
                    print("_________________________________________________________________________")
                    print("                    Endereço atualizado com sucesso!                     ") 
                    print("_________________________________________________________________________")
                except IndexError:
                    print("Algo deu errado")
        elif(escolha==6):
            ns="SET FOREIGN_KEY_CHECKS=0"
            cursor.execute(ns)
            conexao.commit()
            ps="delete from banco where senha_hash='{}'".format(senha_logada)
            cursor.execute(ps)
            conexao.commit()
            gs="delete from transacao where nome1='{}'".format(usuario_logado)
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
            
if __name__ == "__main__":
    opera()