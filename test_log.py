import mysql.connector as mysql
mysql

from sign_up import signup
from log_in import login

def sign_log():
    while True:
        print("\n")
        print("___________________________________________________________________________")
        print("                       Bem-vindo à Personal Finance                        ")
        print("___________________________________________________________________________")
        print("\n")
        print("Aperte 1 para Sign Up ")
        print("Aperte 2 para Log in ")

        try:
            esc = int(input("Introduza sua escolha: "))
            if esc >= 3 or esc < 1:
                raise ValueError("Opção inválida")
            
            
            elif esc == 1:
                signup()
                break
            
            elif esc == 2:
                login()
                break

        except ValueError as e:
            print(e)
            
sign_log()

