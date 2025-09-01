from kivy.app import App
from kivy.lang import Builder
from sign_up_backend import SignupBackend
from login_backend import login as backend_login
from operacoes_backend import (
    get_saldo, add_transacao, listar_transacoes,
    editar_transacao, excluir_transacao,
    get_perfil, atualizar_perfil, excluir_conta
)

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
            
    def ui_get_saldo(self):
        uid = self._uid()
        saldo = get_saldo(uid)
        self.root.ids.balance_value.text = f"R$ {saldo:,.2f}"

    def ui_listar_transacoes(self, limite=5):
        uid = self._uid()
        itens = listar_transacoes(uid, limite)
        rv = self.root.ids.history_rv
        rv.data = [
            {"tx_id": str(i["id"]), "tx_tipo": i["tipo"], "tx_valor": f'R$ {i["valor"]:,.2f}',
             "tx_desc": i["descricao"], "tx_data": i["data"]}
            for i in itens
        ]

    def ui_add_transacao(self, tipo, valor, descricao):
        uid = self._uid()
        res = add_transacao(uid, tipo, valor, descricao or "")
        msg = res.get("erro") if not res.get("ok") else "Transação adicionada"
        self.root.ids.ops_feedback.text = msg
        if res.get("ok"):
            self.ui_get_saldo()
            self.ui_listar_transacoes()

    def ui_editar_transacao(self, transacao_id, novo_tipo=None, novo_valor=None, nova_descricao=None):
        uid = self._uid()
        res = editar_transacao(uid, int(transacao_id), novo_tipo, novo_valor, nova_descricao)
        msg = res.get("erro") if not res.get("ok") else "Transação editada"
        self.root.ids.ops_feedback.text = msg
        if res.get("ok"):
            self.ui_get_saldo()
            self.ui_listar_transacoes()

    def ui_excluir_transacao(self, transacao_id):
        uid = self._uid()
        res = excluir_transacao(uid, int(transacao_id))
        msg = res.get("erro") if not res.get("ok") else "Transação excluída"
        self.root.ids.ops_feedback.text = msg
        if res.get("ok"):
            self.ui_get_saldo()
            self.ui_listar_transacoes()

    def ui_carregar_perfil(self):
        uid = self._uid()
        p = get_perfil(uid) or {}
        self.root.ids.perfil_nome.text = p.get("nome", "")
        self.root.ids.perfil_email.text = p.get("email", "")

    def ui_atualizar_perfil(self, nome, email):
        uid = self._uid()
        res = atualizar_perfil(uid, nome or None, email or None)
        self.root.ids.perfil_feedback.text = res.get("erro") if not res.get("ok") else "Perfil atualizado"

    def ui_excluir_conta(self):
        uid = self._uid()
        res = excluir_conta(uid)
        self.root.ids.perfil_feedback.text = res.get("erro") if not res.get("ok") else "Conta excluída"
        if res.get("ok"):
            # redirecionar para tela de login
            self.current_user_id = 0
            self.root.current = "login"




if __name__ == "__main__":
    MeuApp().run()
