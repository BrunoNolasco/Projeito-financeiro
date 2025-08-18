from kivy.app import App
from kivy.lang import Builder
from sign_up_backend import SignupBackend

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
            label.color = (0, 1, 0, 1)  # verde
        else:
            label.text = msg
            label.color = (1, 0, 0, 1)  # vermelho


    def validar_sobrenome(self, sobrenome):
        valido, msg = self.backend.validar_sobrenome(sobrenome)
        self.root.get_screen("signup").ids.mensagem.text = msg

    def validar_senha(self, senha):
        valido, msg = self.backend.validar_senha(senha)
        self.root.get_screen("signup").ids.mensagem.text = msg

    def validar_nascimento(self, nascimento_str):
        valido, msg = self.backend.validar_nascimento(nascimento_str)
        self.root.get_screen("signup").ids.mensagem.text = msg

    def validar_telefone(self, telefone):
        valido, msg = self.backend.validar_telefone(telefone)
        self.root.get_screen("signup").ids.mensagem.text = msg

    def validar_contribuinte(self, contribuinte):
        valido, msg = self.backend.validar_contribuinte(contribuinte)
        self.root.get_screen("signup").ids.mensagem.text = msg

    def criar_conta(self, deposito, endereco):
        sucesso, msg = self.backend.criar_conta(deposito, endereco)
        self.root.get_screen("signup").ids.mensagem.text = msg

if __name__ == "__main__":
    MeuApp().run()
