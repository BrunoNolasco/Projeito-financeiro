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

def date:
    a =input("Enter Your Date of Birth : ")
    a = date.datetime.strptime(a, "%d/%m/%Y").date()

q="insert into usuarios values('{}','{}','{}','{}','{}','{}','{}','{}')".format(ut,p,z,a,s,d,f,k)
            cursor.execute(q)
            conexao.commit()
            print("\n")
            print("_________________________________________________________________________")
            print("***********Account Has Been Created Successfully Kindly Login************")
            print("_________________________________________________________________________")
            
print(resultado)