from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from interface.tela_nova_transacao import TelaNovaTransacao

class TransacoesListView(RecycleView):
    def __init__(self, transacoes, **kwargs):
        super().__init__(**kwargs)
        self.data = [{'text': t} for t in transacoes]

class TelaPrincipal(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)

        self.add_widget(Label(text="Transações Recentes", size_hint=(1, 0.1)))

        transacoes = [
            "01/08 - Salário - R$ 2500,00",
            "02/08 - Alimentação - R$ 150,00",
            "03/08 - Transporte - R$ 50,00",
        ]

        self.lista = TransacoesListView(transacoes=transacoes, size_hint=(1, 0.7))
        self.add_widget(self.lista)

        btn_nova = Button(text="Nova Transação", size_hint=(1, 0.1))
        btn_nova.bind(on_press=self.abrir_formulario)
        self.add_widget(btn_nova)

    def abrir_formulario(self, instance):
        formulario = TelaNovaTransacao()
        popup = Popup(title="Nova Transação", content=formulario, size_hint=(0.8, 0.8))
        popup.open()

class ControleFinanceiroApp(App):
    def build(self):
        return TelaPrincipal()

if __name__ == "__main__":
    ControleFinanceiroApp().run()
