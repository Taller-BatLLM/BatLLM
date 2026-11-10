"""
Prueba mínima de escritura en Kivy (fuera de BatLLM).

Abre una ventana con un área de texto. Al escribir, la terminal muestra
cada evento de teclado que recibe Kivy:
  [tecla] -> se apretó una tecla (código interno)
  [texto] -> Kivy recibió un carácter para escribir
Cerrar la ventana para terminar.
"""

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput


def al_apretar_tecla(_ventana, tecla, codigo, texto, modificadores):
    print(f"[tecla] código={tecla} texto={texto!r} modificadores={modificadores}")
    return False  # no bloquear la tecla


def al_recibir_texto(_ventana, texto):
    print(f"[texto] {texto!r}")
    return False


class PruebaApp(App):
    def build(self):
        Window.bind(on_key_down=al_apretar_tecla, on_textinput=al_recibir_texto)
        caja = BoxLayout(orientation="vertical", padding=20, spacing=10)
        caja.add_widget(Label(text="Hacé clic en el área de abajo y escribí algo", size_hint_y=0.2))
        caja.add_widget(TextInput(multiline=True, font_size=24))
        return caja


if __name__ == "__main__":
    PruebaApp().run()
