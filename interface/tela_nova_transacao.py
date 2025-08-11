from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from datetime import date

class TelaNovaTransacao(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', padding=10, spacing=10, **kwargs)

        self.add_widget(Label(text="Descrição:"))
        self.input_descricao = TextInput(multiline=False)
        self.add_widget(self.input_descricao)

        self.add_widget(Label(text="Valor:"))
        self.input_valor = TextInput(multiline=False, input_filter='float')
        self.add_widget(self.input_valor)

        self.add_widget(Label(text="Tipo:"))
        self.spinner_tipo = Spinner(
            text='Selecione',
            values=['receita', 'despesa']
        )
        self.add_widget(self.spinner_tipo)

        self.btn_salvar = Button(text="Salvar")
        self.btn_salvar.bind(on_press=self.salvar_transacao)
        self.add_widget(self.btn_salvar)

        self.label_status = Label(text="")
        self.add_widget(self.label_status)

    def salvar_transacao(self, instance):
        descricao = self.input_descricao.text
        valor = self.input_valor.text
        tipo = self.spinner_tipo.text

        if not descricao or not valor or tipo == 'Selecione':
            self.label_status.text = "Preencha todos os campos."
            return

        try:
            valor_float = float(valor)
        except ValueError:
            self.label_status.text = "Valor inválido."
            return



        self.label_status.text = f"Transação '{descricao}' de R$ {valor_float:.2f} ({tipo}) salva."
        self.input_descricao.text = ""
        self.input_valor.text = ""
        self.spinner_tipo.text = "Selecione"

class NovaTransacaoApp(App):
    def build(self):
        return TelaNovaTransacao()

if __name__ == "__main__":
    NovaTransacaoApp().run()
