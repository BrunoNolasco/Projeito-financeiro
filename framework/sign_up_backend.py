from datetime import datetime
from db import get_connection

SpecialSym = ['$', '@', '#', '%']

class SignupBackend:

    def __init__(self):
        self.nome = None
        self.sobrenome = None
        self.senha = None
        self.deposito = None
        self.nascimento = None
        self.endereco = None
        self.telefone = None
        self.contribuinte = None

    def validar_nome(self, nome):
        if any(c in nome for c in ['.', '#', '$', '*', '&', '=', ',', '@', '?', '/']):
            return False, "Caracteres especiais não são aceitos"
        if len(nome) < 2:
            return False, "Nome muito curto"
        return True, ""

    def validar_sobrenome(self, sobrenome):
        if any(c in sobrenome for c in ['.', '#', '$', '*', '&', '=', ',', '@', '?', '/']):
            return False, "Caracteres especiais não são aceitos."
        self.sobrenome = sobrenome
        return True, f"Sobrenome válido: {sobrenome}"

    def validar_senha(self, senha):
        if (len(senha) < 6 or
            not any(char.isdigit() for char in senha) or
            not any(char.isupper() for char in senha) or
            not any(char.islower() for char in senha) or
            not any(char in SpecialSym for char in senha)):
            return False, "Senha inválida."
        self.senha = senha
        return True, "Senha válida."

    def validar_nascimento(self, nascimento_str):
        try:
            self.nascimento = datetime.strptime(nascimento_str, "%d/%m/%Y").date()
            return True, f"Data válida: {self.nascimento}"
        except ValueError:
            return False, "Formato inválido. Use DD/MM/AAAA."

    def validar_telefone(self, telefone):
        if len(telefone) != 9 or not telefone.isdigit():
            return False, "Telefone inválido."
        self.telefone = telefone
        return True, f"Telefone válido: {telefone}"

    def validar_contribuinte(self, contribuinte):
        if len(contribuinte) != 9 or not contribuinte.isdigit():
            return False, "Contribuinte inválido."
        self.contribuinte = contribuinte
        return True, f"Contribuinte válido: {contribuinte}"

    # --- Criar conta ---
    def criar_conta(self, deposito, endereco):
        if not all([self.nome, self.sobrenome, self.senha, self.nascimento,
                    self.telefone, self.contribuinte]):
            return False, "Preencha todos os campos corretamente."

        self.deposito = deposito
        self.endereco = endereco

        try:
            conexao = get_connection()
            cursor = conexao.cursor()
            query = """
                INSERT INTO banco (nome, sobrenome, senha_hash, saldo, nascimento, endereco, telefone, contribuinte)
                VALUES (%s, %s, SHA2(%s, 256), %s, %s, %s, %s, %s)
            """
            valores = (self.nome, self.sobrenome, self.senha, self.deposito,
                       self.nascimento, self.endereco, self.telefone, self.contribuinte)
            cursor.execute(query, valores)
            conexao.commit()
            return True, "Conta criada com sucesso!"
        except Exception as e:
            return False, f"Erro ao criar conta: {e}"
        finally:
            cursor.close()
            conexao.close()
