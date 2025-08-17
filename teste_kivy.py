#from kivy.app import App
#from kivy.uix.button import Button
#
#class TestApp(App):
# def build(self):
#  return Button(text='Olá, Kivy!')
#
#TestApp().run()

from kivy.app import App
from kivy.lang import Builder

GUI = Builder.load_file("tela.kv")

class MeuAplicativo(App):
    def build(self):
        return GUI

MeuAplicativo().run()

