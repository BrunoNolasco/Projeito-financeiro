
import datetime  as date

SpecialSym =['$', '@', '#', '%']
dates1=date.datetime.now()


def logii():
    while True:
        print("\n")
        print("___________________________________________________________________________")
        print("                      Bem-vindo à Personal Finance                      ")
        print("____________________________________________________________________________")
        print("Aperte 1 para Sign Up ")
        print("Aperte 2 para Sign In ")

        try:
            ch=int(input("Introduza sua escolha: "))
            if str(ch).isalpha() or ch >= 3:

                raise Exception ("Não é um número válido, tente novamente: ")




            elif(ch==1):
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
                        if (a in ut) or (a1 in ut) or (a3 in ut) or (a4 in ut) or (a5 in ut) or (a6 in ut) or (a7 in ut) or (a8 in ut) or (a9 in ut):
                            raise TypeError 
                        break
                    except TypeError:
                        print("Caracteres especiais como . , @ # < > ? / ; não são aceitos. ")
                while True:
                    try:
                        a='.'
                        a1='#'
                        a2='$'
                        a3='*'
                        a4='&'
                        a5='='
                        a6=','
                        a8='?'
                        a9='@'
                        p=input("Introduza o seu sobrenome: ")
                        if(a in p) or (a1 in p) or (a2 in p) or (a3 in p) or (a4 in p) or (a5 in p) or (a6 in p) or (a7 in p) or (a8 in p) or (a9 in p):
                            raise TypeError 
                        break
                    except TypeError as m:
                        print("Caracteres especiais como . , @ # < > ? / ; não são aceitos. ")
                while True:        
                    try:

                        z=input("Introduza sua Password: ")
                        if (len(z)<6):
                            raise ValueError ("A password deve ter pelo menos 6 caracteres. ")
                        if not any(char.isdigit() for char in z):
                            raise ValueError ("A password deve ter pelo menos um número. ")
                        if not any(char.isupper() for char in z):
                            raise KeyError ()
                        if not any(char.islower() for char in z):
                            raise KeyError
                        if not any(char in SpecialSym for char in z ):
                            raise KeyError
                        break
                    except ValueError:
                        print("A password deve conter pelo menos 1 letra maiúscula, 1 letra minúscula, um caracter especial e pelo menos 7 caracteres")
                    except KeyError:
                        print("A password deve conter pelo menos 1 letra maiúscula, 1 letra minúscula, um caracter especial e pelo menos 7 caracteres")


                k=int(input("Introduza quanto dinheiro pretende depositar: "))
                while True:
                    try:
                        a=input("Introduza sua data de nascimento: ")
                        a = date.datetime.strptime(a, "%d/%m/%Y").date()
                        break
                    except ValueError:
                        print("Por favor, introduza a data de nascimento no formato DD/MM/YYYY")

                s=input("Introduza seu endereço: ")
                while True:
                    try:
                        d=input("Introduza seu número de telefone: ")
                        if (len(d)!=9) or (d.isalpha()):
                            raise ValueError("Por favor, introdura um número válido de 9 dígitos")
                        break
                    except ValueError as m:
                        print(m)
                while True:
                    try:
                        f=input("Introduza seu contribuinte: ")
                        if(len(f)!=9) or (f.isalpha()):
                            raise ValueError ("Por favor, introdura um número válido de 9 dígitos")
                        break
                    except ValueError as m:
                        print(m)
                #q="insert into bank values('{}','{}','{}','{}','{}','{}','{}','{}')".format(ut,p,z,a,s,d,f,k)
                #mycur.execute(q)
                #mycon.commit()
                print("\n")
                print("_________________________________________________________________________")
                print("          Sua conta na Personal Finance foi criada com sucesso!          ")
                print("_________________________________________________________________________")
            break
        except Exception:
            print("\n")
            print("_________________________________________________")
            print(" Esse nome de usuário não é válido ")
            print("_________________________________________________")

        #while True:
        #    if(ch==2):
        #        u=input("Enter Your Username : ")
        #        p=input("Enter Your Password : ")
        #        a="select * from bank where UserName='{}' and Password='{}'".format(u,p)
        #        mycur.execute(a)
        #        data=mycur.fetchall()