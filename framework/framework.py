import hashlib
from datetime import datetime
from kivy.app import App
from kivy.lang import Builder
from kivy.clock import Clock
from db import get_connection

from operacoes_backend import (
    get_saldo,
    add_transacao,
    listar_transacoes,
    editar_transacao,
    excluir_transacao,
    get_perfil,
    atualizar_perfil,
    criar_conta_banco,
    autenticar_usuario
)

KV = """
ScreenManager:
    MenuScreen:
        name: "menu"
    SignupScreen:
        name: "signup"
    LoginScreen:
        name: "login"
    OperationsScreen:
        name: "operations"


<MenuScreen@Screen>:
    name: "menu"
    BoxLayout:
        orientation: "vertical"
        spacing: 20
        padding: 50

        Label:
            text: "Bem-vindo a Personal Finance"
            font_size: 32

        Button:
            text: "Sign up"
            size_hint_y: None
            height: 50
            on_release: root.manager.current = "signup"

        Button:
            text: "Log in"
            size_hint_y: None
            height: 50
            on_release: root.manager.current = "login"


<SignupScreen@Screen>:
    ScrollView:
        BoxLayout:
            orientation: "vertical"
            padding: 20
            spacing: 15
            size_hint_y: None
            height: self.minimum_height

            Label:
                text: "Cadastro"
                font_size: 28
                size_hint_y: None
                height: 50

            TextInput:
                id: nome
                hint_text: "Nome"
                multiline: False
                size_hint_y: None
                height: 40

            TextInput:
                id: sobrenome
                hint_text: "Sobrenome"
                multiline: False
                size_hint_y: None
                height: 40

            TextInput:
                id: senha
                hint_text: "Senha"
                password: True
                multiline: False
                size_hint_y: None
                height: 40

            TextInput:
                id: nascimento
                hint_text: "Data de nascimento (DD/MM/AAAA)"
                multiline: False
                size_hint_y: None
                height: 40

            TextInput:
                id: telefone
                hint_text: "Telefone (9 dígitos)"
                multiline: False
                size_hint_y: None
                height: 40

            TextInput:
                id: contribuinte
                hint_text: "Contribuinte (9 dígitos)"
                multiline: False
                size_hint_y: None
                height: 40

            TextInput:
                id: endereco
                hint_text: "Endereço"
                multiline: False
                size_hint_y: None
                height: 40

            TextInput:
                id: deposito
                hint_text: "Depósito inicial"
                multiline: False
                size_hint_y: None
                height: 40

            Button:
                text: "Cadastrar"
                size_hint_y: None
                height: 50
                on_release: app.criar_conta()

            Label:
                id: mensagem
                text: ""
                color: 1,0,0,1
                size_hint_y: None
                height: 30

            Button:
                text: "Voltar ao Menu"
                size_hint_y: None
                height: 50
                on_release: app.root.current = "menu"


<LoginScreen@Screen>:
    ScrollView:
        BoxLayout:
            orientation: "vertical"
            padding: 20
            spacing: 15
            size_hint_y: None
            height: self.minimum_height

            Label:
                text: "Login"
                font_size: 28
                size_hint_y: None
                height: 50

            TextInput:
                id: nome_login
                hint_text: "Nome"
                multiline: False
                size_hint_y: None
                height: 40

            TextInput:
                id: senha_login
                hint_text: "Senha"
                password: True
                multiline: False
                size_hint_y: None
                height: 40

            Button:
                text: "Entrar"
                size_hint_y: None
                height: 50
                on_release: app.login(nome_login.text, senha_login.text)

            Label:
                id: mensagem_login
                text: ""
                color: 1,0,0,1
                size_hint_y: None
                height: 30

            Button:
                text: "Voltar ao Menu"
                size_hint_y: None
                height: 50
                on_release: app.root.current = "menu"


<OperationsScreen@Screen>:
    ScrollView:
        BoxLayout:
            orientation: "vertical"
            padding: 12
            spacing: 12
            size_hint_y: None
            height: self.minimum_height

            Label:
                text: "Personal Finance"
                font_size: "20sp"

            BoxLayout:
                size_hint_y: None
                height: 40
                spacing: 8
                Label:
                    text: "Saldo:"
                    size_hint_x: None
                    width: 60
                Label:
                    id: balance_value
                    text: "R$ 0,00"

            # Adicionar Transação
            BoxLayout:
                size_hint_y: None
                height: 40
                spacing: 8
                Spinner:
                    id: add_tipo
                    text: "deposito"
                    values: ["deposito","retirada"]
                    size_hint_x: None
                    width: 120
                TextInput:
                    id: add_valor
                    hint_text: "Valor"
                    input_filter: "float"
                TextInput:
                    id: add_desc
                    hint_text: "Descrição"
                Button:
                    text: "Adicionar"
                    on_release:
                        app.ui_add_transacao(add_tipo.text, add_valor.text, add_desc.text)
                        add_valor.text = ""
                        add_desc.text = ""

            # Feedback de operações
            Label:
                id: ops_feedback
                text: ""
                color: 1,0,0,1
                size_hint_y: None
                height: 24

            # Histórico
            Label:
                text: "Últimas transações"
                size_hint_y: None
                height: 24

            RecycleView:
                id: history_rv
                viewclass: "HistoryItem"
                RecycleBoxLayout:
                    default_size: None, 56
                    default_size_hint: 1, None
                    size_hint_y: None
                    height: self.minimum_height
                    orientation: 'vertical'

            # Editar / Excluir
            BoxLayout:
                size_hint_y: None
                height: 40
                spacing: 8
                TextInput:
                    id: edit_id
                    hint_text: "ID transação"
                    input_filter: "int"
                    size_hint_x: None
                    width: 120
                Spinner:
                    id: edit_tipo
                    text: "deposito"
                    values: ["deposito","retirada"]
                    size_hint_x: None
                    width: 120
                TextInput:
                    id: edit_valor
                    hint_text: "Novo valor"
                    input_filter: "float"
                TextInput:
                    id: edit_desc
                    hint_text: "Nova descrição"
                Button:
                    text: "Editar"
                    on_release:
                        app.ui_editar_transacao(edit_id.text, edit_tipo.text, edit_valor.text if edit_valor.text else None, edit_desc.text if edit_desc.text else None)
                        edit_valor.text = ""
                        edit_desc.text = ""
                Button:
                    text: "Excluir"
                    on_release:
                        app.ui_excluir_transacao(edit_id.text)
                        edit_id.text = ""

            Label:
                text: "Atualizar Dados"
                size_hint_y: None
                height: dp(24)

            # Perfil
            GridLayout:
                cols: 2
                size_hint_y: None
                height: self.minimum_height
                row_default_height: dp(40)
                spacing: dp(8)

                Label:
                    text: "Nome:"
                    size_hint_x: None
                    width: dp(100)
                TextInput:
                    id: perfil_nome
                    hint_text: "Nome"

                Label:
                    text: "Sobrenome:"
                    size_hint_x: None
                    width: dp(100)
                TextInput:
                    id: perfil_sobrenome
                    hint_text: "Sobrenome"

                Label:
                    text: "Endereço:"
                    size_hint_x: None
                    width: dp(100)
                TextInput:
                    id: perfil_endereco
                    hint_text: "Endereço"

                Label:
                    text: "Telefone:"
                    size_hint_x: None
                    width: dp(100)
                TextInput:
                    id: perfil_telefone
                    hint_text: "Telefone"

                Label:
                    text: "Contribuinte:"
                    size_hint_x: None
                    width: dp(100)
                TextInput:
                    id: perfil_contribuinte
                    hint_text: "Contribuinte"

            BoxLayout:
                size_hint_y: None
                height: dp(40)
                spacing: dp(8)
                Button:
                    text: "Carregar Perfil"
                    on_release: app.ui_carregar_perfil()
                Button:
                    text: "Atualizar Perfil"
                    on_release: app.ui_atualizar_perfil(perfil_nome.text, perfil_sobrenome.text, perfil_endereco.text, perfil_telefone.text, perfil_contribuinte.text)

            Label:
                id: perfil_feedback
                text: ""
                size_hint_y: None
                height: dp(20)

            BoxLayout:
                size_hint_y: None
                height: 40
                spacing: 8
                Button:
                    text: "Atualizar Saldo/Histórico"
                    on_release:
                        app.ui_get_saldo()
                        app.ui_listar_transacoes()
                Button:
                    text: "Sair"
                    on_release:
                        app.current_user_id = None
                        app.root.current = "login"

<HistoryItem@BoxLayout>:
    orientation: "horizontal"
    size_hint_y: None
    height: 40

    Label:
        id: tipo
        text: root.tipo if hasattr(root, "tipo") else ""
        size_hint_x: 0.3

    Label:
        id: valor
        text: root.valor if hasattr(root, "valor") else ""
        size_hint_x: 0.3

    Label:
        id: descricao
        text: root.descricao if hasattr(root, "descricao") else ""
        size_hint_x: 0.4


"""

class MeuApp(App):
    title = "Personal Finance"
    current_user_id = None  # guarda banco.id do usuário autenticado

    def build(self):
        return Builder.load_string(KV)

    # ---------- SIGNUP ----------
    def criar_conta(self):
        scr = self.root.get_screen('signup')
        ids = scr.ids
        try:
            nome = ids['nome'].text.strip()
            sobrenome = ids['sobrenome'].text.strip()
            senha = ids['senha'].text.strip()
            nascimento = ids['nascimento'].text.strip()
            telefone = ids['telefone'].text.strip()
            contribuinte = ids['contribuinte'].text.strip()
            endereco = ids['endereco'].text.strip()
            deposito = ids['deposito'].text.strip()

            if not (nome and sobrenome and senha and nascimento and telefone and contribuinte and endereco):
                ids['mensagem'].text = "Preencha todos os campos."
                return

            # dd/mm/aaaa -> yyyy-mm-dd
            try:
                d, m, a = nascimento.split('/')
                nascimento_sql = f"{a}-{m}-{d}"
            except Exception:
                ids['mensagem'].text = "Data de nascimento inválida."
                return

            valor_inicial = float(deposito.replace(',', '.')) if deposito.strip() else 0.0

            ok, msg = criar_conta_banco(
                nome=nome,
                sobrenome=sobrenome,
                senha_plana=senha,
                saldo_inicial=valor_inicial,
                nascimento=nascimento_sql,
                endereco=endereco,
                telefone=telefone,
                contribuinte=contribuinte
            )
            ids['mensagem'].text = msg
            if ok:
                self.root.current = "login"
        except Exception as e:
            ids['mensagem'].text = f"Erro: {e}"

    # ---------- LOGIN ----------
    def login(self, nome: str, senha: str):
        scr = self.root.get_screen('login')
        msg = scr.ids['mensagem_login']
        try:
            uid = autenticar_usuario(nome.strip(), senha.strip())
            if not uid:
                msg.text = "Credenciais inválidas."
                return
            self.current_user_id = uid
            self.root.current = 'operations'
            Clock.schedule_once(lambda dt: (self.ui_get_saldo(), self.ui_listar_transacoes()))
        except Exception as e:
            msg.text = f"Erro: {e}"

    # ---------- helpers ----------
    def _ops_ids(self):
        return self.root.get_screen('operations').ids

    def ui_get_saldo(self):
        if not self.current_user_id:
            return
        saldo = get_saldo(self.current_user_id)
        self._ops_ids()['balance_value'].text = f"R$ {saldo:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

    def ui_listar_transacoes(self, limite: int = 10):
        if not self.current_user_id:
            return
        rv = self._ops_ids()['history_rv']
        itens = listar_transacoes(self.current_user_id, limite)
        data = []
        for it in itens:
            data.append({
                'tipo': it['tipo'],
                'valor': f"R$ {it['valor']:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'),
                'descricao': f"{it.get('descricao','')} (id {it['id']})",
            })
        rv.data = data

    def ui_add_transacao(self, tipo: str, valor: str, descricao: str):
        if not self.current_user_id:
            return
        res = add_transacao(self.current_user_id, tipo, valor, descricao or "")
        fb = self._ops_ids()['ops_feedback']
        if res.get("ok"):
            fb.text = "Transação adicionada."
            self.ui_get_saldo()
            self.ui_listar_transacoes()
        else:
            fb.text = f"Erro: {res.get('erro','')}"

    def ui_editar_transacao(self, transacao_id: str, tipo: str, valor: str | None, descricao: str | None):
        if not self.current_user_id:
            return
        try:
            tid = int(transacao_id)
        except:
            self._ops_ids()['ops_feedback'].text = "ID inválido."
            return
        res = editar_transacao(self.current_user_id, tid, tipo, valor, descricao)
        fb = self._ops_ids()['ops_feedback']
        if res.get("ok"):
            fb.text = "Transação editada."
            self.ui_get_saldo()
            self.ui_listar_transacoes()
        else:
            fb.text = f"Erro: {res.get('erro','')}"

    def ui_excluir_transacao(self, transacao_id: str):
        if not self.current_user_id:
            return
        try:
            tid = int(transacao_id)
        except:
            self._ops_ids()['ops_feedback'].text = "ID inválido."
            return
        res = excluir_transacao(self.current_user_id, tid)
        fb = self._ops_ids()['ops_feedback']
        if res.get("ok"):
            fb.text = "Transação excluída."
            self.ui_get_saldo()
            self.ui_listar_transacoes()
        else:
            fb.text = f"Erro: {res.get('erro','')}"

    def ui_carregar_perfil(self):
        if not self.current_user_id:
            return

        from db import get_connection
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT nome, sobrenome, endereco, telefone, contribuinte FROM banco WHERE id = %s",
            (self.current_user_id,)
        )
        perfil = cursor.fetchone()
        cursor.close()
        conn.close()

        if perfil:
            tela = self.root.get_screen("operations")
            tela.ids.perfil_nome.text = perfil["nome"]
            tela.ids.perfil_sobrenome.text = perfil["sobrenome"]
            tela.ids.perfil_endereco.text = perfil["endereco"]
            tela.ids.perfil_telefone.text = perfil["telefone"]
            tela.ids.perfil_contribuinte.text = perfil["contribuinte"]

    def ui_atualizar_perfil(self, nome, sobrenome, endereco, telefone, contribuinte):
        if not self.current_user_id:
            return

        try:
            from db import get_connection
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE banco
                SET nome = %s, sobrenome = %s, endereco = %s, telefone = %s, contribuinte = %s
                WHERE id = %s
            """, (nome, sobrenome, endereco, telefone, contribuinte, self.current_user_id))

            conn.commit()
            linhas_afetadas = cursor.rowcount
            cursor.close()
            conn.close()

            tela = self.root.get_screen("operations")
            if linhas_afetadas > 0:
                tela.ids.perfil_feedback.text = "Perfil atualizado com sucesso!"
                tela.ids.perfil_feedback.color = (0, 1, 0, 1)
            else:
                tela.ids.perfil_feedback.text = "Nenhuma alteração realizada."
                tela.ids.perfil_feedback.color = (1, 0.5, 0, 1)

        except Exception as e:
            tela = self.root.get_screen("operations")
            tela.ids.perfil_feedback.text = f"Erro ao atualizar: {e}"
            tela.ids.perfil_feedback.color = (1, 0, 0, 1)




if __name__ == "__main__":
    MeuApp().run()
