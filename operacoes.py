from mysql.connector import IntegrityError
import mysql.connector as mysql
import datetime as date
dates1 = date.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

from log_in import login
usuario_logado = login()
senha_logada = login()

conexao = mysql.connect(
    host="localhost",
    user="Brunopy",
    password="",
    database='controle_financeiro'
)
cursor = conexao.cursor()



def opera():
    while True:

        print("\n")
        print("___________________________________________________________________________")
        print("*************** Welcome To Colony banco Of India : *************************")
        print("___________________________________________________________________________")
        print("\n")
        print("Press 1 To Withdraw Money")
        print("Press 2 To Deposit Money")
        print("Press 3 to view Last Five transacao ")
        print("Press 4 To View Your Profile ")
        print("Press 5 To Update Account details")
        print("Press 6 to Delete Your Account Permanently : ")
        print("Press 7 for Log Out")
        try:
            escolha=int(input("Enter Your Choice : "))
            if(escolha>=8):
                raise TypeError ("")

        except TypeError:
            print("________________________________________________")
            print("     OOPs !!! That Was an Invalid Input :(  ")
            print("________________________________________________")

        if(escolha==1):

            try:
                np="select saldo from banco where nome='{}'".format(usuario_logado)
                cursor.execute(np)
                bal=cursor.fetchone()[0]
            except Exception:
                print("oops")
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
                    print("   ***OOPs that was an invalid input***  :)  ")
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
                    print("Your nome " ,usuario_logado , "is debitado with Rs" , a1 ,"on " , dates1)
                    print("towards Net bancoing. Available saldo is Rs : " , bal1, " ₹ only ")
                    print("________________________________________________________________________")
                elif(a1>bal):

                    print("________________________________________________________________________")
                    print("   ********* OOPS Insufficient saldo Please Try Again !  **********")
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
                        print("Your nome " ,usuario_logado , "is creditado with Rs" , a11 ,"on " , dates1)
                        print("towards Net bancoing. Available saldo is Rs : " , bal2, " ₹ only")
                        print("________________________________________________________________________")
                        break
                except TypeError:
                    print("oops")
                except IntegrityError:
                    print("oopss")
        elif(escolha==3):
            prt="Select creditado,debitado,data from transacao where nome1='{}'".format(usuario_logado)
            cursor.execute(prt)
            print("______________________________________________________________________________")
            print("*************** The transacao Details are as Follows*********************")
            print("\n")
            for i in cursor:
                print("___________________________________________________________________________")
                print("creditado , debitado  : " ,i)
                print("___________________________________________________________________________")
        elif(escolha==4):
            nmm="Select nome, sobrenome, senha_hash, endereco, telefone, contribuinte, saldo from banco where nome='{}'".format(usuario_logado)
            cursor.execute(nmm)
            print("______________________________________________________________________________")
            print("*******************************ACCOUNT DETAILS *******************************")
            print("______________________________________________________________________________")
            print("\n")
            print("_______________________________________________________________________________")
            print("    Nome      Sobrenome  Senha   Endereço     Telefone \t   Contribuinte    Saldo")
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

                print("Aperte 1 para atualizar o seu Name: ")
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
                    print("      ****OOP's That's Was an invalid input****    ")
                    print("___________________________________________________")
                    continue
                break
            if(escolha2==1):
                try:
                    novo_nome=input ("Insira seu novo nome: ")
                    ns="update banco set novo_nome='{}' where senha='{}'".format(novo_nome,senha_logada)

                    cursor.execute(ns)
                    conexao.commit()
                    print("_________________________________________________________________________")
                    print ("   ****Hurrey !!! Name is Updated Successfully***   :) ")
                    print("_________________________________________________________________________")
                except IndexError:
                    print("Oh Something Went Wrong !!!")
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
                    print ("   ****Hurrey !!! nome is Updated Successfully***   :) ")
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
                    print ("Hurrey !!! Password is Updated Successfully")
                except IndexError:
                    print("Oh Something Went Wrong")
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
                        print ("   ****Hurrey !!! Mobile Number is Updated Successfully***   :) ")
                        print("_________________________________________________________________________")

                    except ValueError:
                        print("________________________________________________________")
                        print("**** Please Enter a valid 9 digit Number ******")
                        print("________________________________________________________")
                        print("\n")
                        continue
                    break
                
            elif(escolha2==5):
                try:
                    novo_endereco=input("Insira o seu novo novo endereco: ")
                    ns1="update banco set endereco='{}' where nome='{}'".format(novo_endereco,usuario_logado)
                    cursor.execute(ns1)
                    conexao.commit()
                    print("_________________________________________________________________________")
                    print("   *** Hurrey !!! Address is Updated Successfully ***  :) ") 
                    print("_________________________________________________________________________")
                except IndexError:
                    print("OOPS Something Went Swrong !!! ")
        elif(escolha==6):
            ns="SET FOREIGN_KEY_CHECKS=0"
            cursor.execute(ns)
            conexao.commit()
            ps="delete from banco where senha='{}'".format(senha_logada)
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
            print("************* ACCOUNT HAS BEEN DELETED SUCCESSFULLY *******************")
            print("_________________________________________________________________________")
            print("\n")
            exit()
        elif(escolha==7):
            print("\n")
            print("_____________________________________________________________________________")
            print("*************Thanks For Choosing Colony banco Of India *****************")
            print("____________________________________________________________________________")
            exit()