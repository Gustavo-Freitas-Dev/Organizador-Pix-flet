from interface import construir_interface,construir_tela_adicionar_banco
import flet as ft


def main(page: ft.Page):
    def rota_mudou(e):
        page.views.clear()

        if page.route == "/":
            construir_interface(page)

        elif page.route == "/adicionar-banco":
           construir_tela_adicionar_banco(page)

        page.update()

    # Configurações da janela
    page.window.width = 800
    page.window.height = 700
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window.resizable = False
    page.window.maximizable = False
    page.title = "Pix Organiza"
    page.padding = 20
    page.window.icon = r"Z:\Programas\Assents\pix_icon_198027.ico"

    # Ativa escuta da rota e navega para a inicial
    page.on_route_change = rota_mudou
    page.go("/")
    
ft.app(target=main)
