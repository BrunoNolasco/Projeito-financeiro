from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.button import Button
import sqlite3

DB_PATH = "dados_financeiros.db"

class ListaTransacoes(RecycleView):
    def __init__(self, **kwargs):
        super(ListaTransacoes, self).__init__(**kwargs)
        self.refresh_list()

    def refresh_list(self):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT descricao, valor, data FROM transacoes ORDER BY data DESC")
        dados = cursor.fetchall()
        conn.close()

        self.data = [
            {"text": f"{desc} | {valor:.2f}€ | {data}"}
            for desc, valor, data in dados
        ]

class TelaPrincipal(BoxLayout):
    def __init__(self, **kwargs):
        super(TelaPrincipal, self).__init__(orientation='vertical', **kwargs)

        self.lista = ListaTransacoes()
        self.add_widget(self.lista)

        btn_atualizar = Button(text="Atualizar Lista", size_hint_y=None, height=40)
        btn_atualizar.bind(on_release=lambda x: self.lista.refresh_list())
        self.add_widget(btn_atualizar)

class FinanceiroApp(App):
    def build(self):
        return TelaPrincipal()

if __name__ == "__main__":
    FinanceiroApp().run()
