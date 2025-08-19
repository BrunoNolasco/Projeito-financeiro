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
        self.nome = nome
        return True, f"Nome válido: {nome}"

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
    
    def validar_deposito(self, deposito):
        if not deposito.isdigit():
            return False, "Depósito inválido."
        self.deposito = deposito
        return True, f"Depósito válido: {deposito}"
    
    def validar_endereco(self, endereco):
        if len(endereco) < 5:
            return False, "Endereço muito curto."
        self.endereco = endereco
        return True, f"Endereço válido: {endereco}"

    def criar_conta(self):
        if not all([self.nome, self.sobrenome, self.senha, self.nascimento,
                    self.telefone, self.contribuinte, self.deposito, self.endereco]):
            return False, "Preencha todos os campos corretamente."

        try:
            conexao = get_connection()
            cursor = conexao.cursor()

            if isinstance(self.nascimento, str):
                try:
                    nascimento_date = datetime.strptime(self.nascimento, "%d/%m/%Y").date()
                except ValueError:
                    return False, "Data de nascimento inválida. Use DD/MM/AAAA."
            else:
                nascimento_date = self.nascimento

            nascimento_formatado = nascimento_date.strftime("%Y-%m-%d")

            query = """
                INSERT INTO banco (nome, sobrenome, senha_hash, saldo, nascimento, endereco, telefone, contribuinte)
                VALUES (%s, %s, SHA2(%s, 256), %s, %s, %s, %s, %s)
            """
            valores = (self.nome, self.sobrenome, self.senha, self.deposito,
                       nascimento_formatado, self.endereco, self.telefone, self.contribuinte)

            cursor.execute(query, valores)
            conexao.commit()
            return True, "Conta criada com sucesso!"
        except Exception as e:
            return False, f"Erro ao criar conta: {e}"
        finally:
            cursor.close()
            conexao.close()