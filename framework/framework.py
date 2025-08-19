from kivy.app import App
from kivy.lang import Builder
from sign_up_backend import SignupBackend
from login_backend import login as backend_login

class MeuApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.backend = SignupBackend()

    def build(self):
        return Builder.load_file("tela.kv")

    def validar_nome(self, nome):
        valido, msg = self.backend.validar_nome(nome)
        label = self.root.get_screen("signup").ids.mensagem
        if valido:
            label.text = "Nome válido"
            label.color = (0, 1, 0, 1)  
        else:
            label.text = "Nome muito curto ou caracteres não aceitos"
            label.color = (1, 0, 0, 1)  

    def validar_sobrenome(self, sobrenome):
        valido, msg = self.backend.validar_sobrenome(sobrenome)
        label = self.root.get_screen("signup").ids.mensagem
        if valido:
            label.text = "Sobrenome válido"
            label.color = (0, 1, 0, 1)  
        else:
            label.text = "Caracteres especiais não são aceitos."
            label.color = (1, 0, 0, 1)  

    def validar_senha(self, senha):
        valido, msg = self.backend.validar_senha(senha)
        label = self.root.get_screen("signup").ids.mensagem
        if valido:
            label.text = "Senha válida."
            label.color = (0, 1, 0, 1)  
        else:
            label.text = "Senha inválida."
            label.color = (1, 0, 0, 1)  

    def validar_nascimento(self, nascimento_str):
        valido, msg = self.backend.validar_nascimento(nascimento_str)
        label = self.root.get_screen("signup").ids.mensagem
        if valido:
            label.text = "Data válida"
            label.color = (0, 1, 0, 1)  
        else:
            label.text = "Formato inválido. Use DD/MM/AAAA."
            label.color = (1, 0, 0, 1)  

    def validar_telefone(self, telefone):
        valido, msg = self.backend.validar_telefone(telefone)
        label = self.root.get_screen("signup").ids.mensagem
        if valido:
            label.text = "Telefone válido"
            label.color = (0, 1, 0, 1)  
        else:
            label.text = "Telefone inválido"
            label.color = (1, 0, 0, 1)  

    def validar_contribuinte(self, contribuinte):
        valido, msg = self.backend.validar_contribuinte(contribuinte)
        label = self.root.get_screen("signup").ids.mensagem
        if valido:
            label.text = "Contribuinte válido"
            label.color = (0, 1, 0, 1)  
        else:
            label.text = "Contribuinte inválido"
            label.color = (1, 0, 0, 1)  

    def validar_deposito(self, deposito):
        valido, msg = self.backend.validar_deposito(deposito)
        label = self.root.get_screen("signup").ids.mensagem
        if valido:
            label.text = "deposito válido"
            label.color = (0, 1, 0, 1)  
        else:
            label.text = "deposito inválido"
            label.color = (1, 0, 0, 1)
            
    def validar_endereco(self, endereco):
        valido, msg = self.backend.validar_endereco(endereco)
        label = self.root.get_screen("signup").ids.mensagem
        if valido:
            label.text = "endereco válido"
            label.color = (0, 1, 0, 1)  
        else:
            label.text = "endereco inválido"
            label.color = (1, 0, 0, 1)

    def criar_conta(self):
        tela = self.root.get_screen("signup")
        
        self.backend.nome = tela.ids.nome.text.strip()
        self.backend.sobrenome = tela.ids.sobrenome.text.strip()
        self.backend.senha = tela.ids.senha.text.strip()
        self.backend.nascimento = tela.ids.nascimento.text.strip()
        self.backend.telefone = tela.ids.telefone.text.strip()
        self.backend.contribuinte = tela.ids.contribuinte.text.strip()
        self.backend.deposito = tela.ids.deposito.text.strip()
        self.backend.endereco = tela.ids.endereco.text.strip()

        sucesso, msg = self.backend.criar_conta()
        label = tela.ids.mensagem
        label.text = msg
        label.color = (0, 1, 0, 1) if sucesso else (1, 0, 0, 1)  
            
    def login(self, nome, senha):
        tela = self.root.get_screen("login")
        sucesso = backend_login(nome.strip(), senha.strip())
        label = tela.ids.mensagem_login
        if sucesso:
            label.text = "Login realizado com sucesso!"
            label.color = (0, 1, 0, 1)
        else:
            label.text = "Usuário ou senha incorretos."
            label.color = (1, 0, 0, 1)



if __name__ == "__main__":
    MeuApp().run()
