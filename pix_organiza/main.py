import flet as ft
import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from interface.tratamento_dos_dados import construir_interface
from interface.adicionar_bancos import construir_tela_adicionar_banco

def main(page: ft.Page):
    def rota_mudou(e):
        page.views.clear()

        match page.route:
            case "/":
                construir_interface(page)
            case "/adicionar-banco":
                construir_tela_adicionar_banco(page)
        page.update()
        
# Caminho base para modo normal ou empacotado (.exe)
    if getattr(sys, 'frozen', False):
        BASE_DIR = sys._MEIPASS
    else:
        BASE_DIR = os.path.abspath(".")

    ICON_PATH = os.path.join(BASE_DIR, "pix_organiza", "assets", "logo-pix.ico")

    page.window.width = 800
    page.window.height = 700
    page.window.resizable = False
    page.window.maximizable = False
    page.padding = 20
    page.window.icon = ICON_PATH
    page.title = "Pix Organiza"
    page.theme_mode = ft.ThemeMode.LIGHT

    page.on_route_change = rota_mudou
    page.go("/")

ft.app(target=main)

