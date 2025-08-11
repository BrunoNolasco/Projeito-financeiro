# main.py
from crud.crud_usuarios import listar_usuarios
from crud.crud_categorias import listar_categorias

if __name__ == "__main__":
    print("📌 Lista de usuários:")
    for u in listar_usuarios():
        print(u)

    print("\n📌 Lista de categorias:")
    for c in listar_categorias():
        print(c)
