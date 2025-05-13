import flet as ft
from main import tratar_dados, limpar_dados
from banco import adicionar_banco, inicializar_banco


def construir_interface(page: ft.Page):
    origem_field = ft.TextField(
        label="Digite os dados a serem tratados",
        width=680,
        bgcolor=ft.Colors.GREY_100,
        border_radius=20,
        focused_border_color="#2196F3",
        expand=True
    )

    dados_tratados = ft.TextField(
        label="Dados tratados",
        multiline=True,
        expand=True,
        bgcolor=ft.Colors.GREY_100,
        border_radius=20,
        focused_border_color="#2196F3",
        read_only=True,
    )

    def copiar_para_area_de_transferencia(e):
        page.set_clipboard(dados_tratados.value)
        page.snack_bar = ft.SnackBar(ft.Text("Dados copiados com sucesso!"), duration=2000)
        page.snack_bar.open = True
        page.update()

    btn_copiar_dados = ft.TextButton(
        text="Copiar Dados",
        icon=ft.Icons.COPY,
        icon_color=ft.Colors.WHITE,
        tooltip="Copiar Dados",
        width=170,
        style=ft.ButtonStyle(bgcolor=ft.Colors.BLUE_400, color=ft.Colors.WHITE),
        on_click=copiar_para_area_de_transferencia
    )

    btn_limpar_dados = ft.TextButton(
        text="Limpar Dados",
        icon=ft.Icons.DELETE_OUTLINE,
        icon_color=ft.Colors.WHITE,
        tooltip="Limpar Dados",
        width=170,
        style=ft.ButtonStyle(bgcolor=ft.Colors.RED_400, color=ft.Colors.WHITE),
        on_click=lambda e: limpar_dados(e, origem_field, dados_tratados)
    )

    btn_tratar_dados = ft.TextButton(
        text="Tratar os Dados",
        icon=ft.Icons.FORMAT_LIST_BULLETED,
        icon_color=ft.Colors.WHITE,
        tooltip="Tratar Dados",
        width=170,
        style=ft.ButtonStyle(bgcolor=ft.Colors.GREEN_400, color=ft.Colors.WHITE),
        on_click=lambda e: tratar_dados(e, origem_field, dados_tratados)
    )

    btn_adicionar_bancos = ft.TextButton(
        text="Adicionar banco",
        icon=ft.Icons.ADD,
        icon_color=ft.Colors.WHITE,
        tooltip="Adicionar banco",
        width=170,
        style=ft.ButtonStyle(bgcolor=ft.Colors.INDIGO_400, color=ft.Colors.WHITE),
        on_click=lambda e: page.go('/adicionar-banco')
    )

    page.views.append(
        ft.View(
            route="/",
            padding=30,
            controls=[
                ft.Column(
                    controls=[
                        ft.Text("Organizador de Pix", size=30, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_600),
                        ft.Divider(),
                        ft.Container(
                            content=ft.Column(
                                controls=[
                                    ft.Text("Dados das Transações", size=16, weight=ft.FontWeight.BOLD),
                                    ft.Row([origem_field], alignment=ft.MainAxisAlignment.START),
                                ],
                                spacing=10
                            ),
                            padding=20,
                            border_radius=20,
                            bgcolor=ft.Colors.GREY_50,
                            shadow=ft.BoxShadow(blur_radius=15, color=ft.Colors.GREY_400)
                        ),
                        ft.Divider(),
                        ft.Container(
                            content=ft.Column(
                                controls=[
                                    ft.Text("Dados Tratados", size=16, weight=ft.FontWeight.BOLD),
                                    dados_tratados,
                                ],
                                spacing=10,
                                expand=True
                            ),
                            padding=20,
                            border_radius=20,
                            bgcolor=ft.Colors.GREY_50,
                            shadow=ft.BoxShadow(blur_radius=15, color=ft.Colors.GREY_400),
                            expand=True,
                        ),
                        ft.Row(
                            [btn_adicionar_bancos, btn_limpar_dados, btn_copiar_dados, btn_tratar_dados],
                            alignment=ft.MainAxisAlignment.END
                        ),
                        ft.Container(
                            content=ft.Row(
                                controls=[
                                    ft.Text(
                                        value="🛠 Feito por @gustavo.python • ⚙ Powered by Python • © 2025",
                                        size=12,
                                        color=ft.Colors.GREY,
                                        opacity=0.7
                                    )
                                ],
                                alignment=ft.MainAxisAlignment.CENTER
                            ),
                            alignment=ft.alignment.bottom_center,
                        )
                    ],
                    expand=True
                )
            ]
        )
    )


def construir_tela_adicionar_banco(page: ft.Page):
    variacao_banco = ft.TextField(
        label="Digite a variação do banco",
        width=680,
        bgcolor=ft.Colors.GREY_100,
        border_radius=20,
        focused_border_color="#2196F3",
        expand=True
    )

    banco_padronizado = ft.TextField(
        label="Digite o nome padronizado",
        width=680,
        bgcolor=ft.Colors.GREY_100,
        border_radius=20,
        focused_border_color="#2196F3",
        expand=True
    )

    def salvar_novo_banco(e):
        variacao = variacao_banco.value.strip()
        padronizado = banco_padronizado.value.strip()
        if variacao and padronizado:
            adicionar_banco(variacao, padronizado)
            page.open(ft.SnackBar(ft.Text("Banco salvo com sucesso!"),duration=5000, bgcolor=ft.Colors.GREEN_400))
            page.update()

    btn_salvar_banco = ft.TextButton(
        text="Salvar",
        icon=ft.Icons.SAVE,
        icon_color=ft.Colors.WHITE,
        tooltip="Salvar Banco",
        width=170,
        style=ft.ButtonStyle(bgcolor=ft.Colors.GREEN_400, color=ft.Colors.WHITE),
        on_click=salvar_novo_banco
    )

    btn_limpar_banco = ft.TextButton(
        text="Limpar Campos",
        icon=ft.Icons.DELETE_OUTLINE,
        icon_color=ft.Colors.WHITE,
        tooltip="Limpar Campos",
        width=170,
        style=ft.ButtonStyle(bgcolor=ft.Colors.RED_400, color=ft.Colors.WHITE),
        on_click=lambda e: limpar_dados(e, variacao_banco, banco_padronizado)
    )

    voltar = ft.TextButton(
        text="Voltar",
        icon=ft.Icons.KEYBOARD_BACKSPACE_ROUNDED,
        icon_color=ft.Colors.WHITE,
        tooltip="Página Anterior",
        width=170,
        style=ft.ButtonStyle(bgcolor=ft.Colors.BLUE_GREY_400, color=ft.Colors.WHITE),
        on_click=lambda e: page.go('/')
    )

    page.views.append(
        ft.View(
            route="/adicionar-banco",
            padding=30,
            controls=[
                ft.Column(
                    controls=[
                        ft.Text("Adicionar Novo Banco", size=30, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_600),
                        ft.Divider(),
                        ft.Container(
                            content=ft.Column(
                                controls=[
                                    ft.Text('Variação do nome do banco', size=16, weight=ft.FontWeight.BOLD),
                                    variacao_banco
                                ]
                            ),
                            padding=20,
                            border_radius=20,
                            bgcolor=ft.Colors.GREY_50,
                            shadow=ft.BoxShadow(blur_radius=15, color=ft.Colors.GREY_400)
                        ),
                        ft.Divider(),
                        ft.Container(
                            content=ft.Column(
                                controls=[
                                    ft.Text('Nome padronizado', size=16, weight=ft.FontWeight.BOLD),
                                    banco_padronizado
                                ]
                            ),
                            padding=20,
                            border_radius=25,
                            bgcolor=ft.Colors.GREY_50,
                            shadow=ft.BoxShadow(blur_radius=15, color=ft.Colors.GREY_400)
                        ),
                        ft.Row(
                            [voltar, btn_limpar_banco, btn_salvar_banco],
                            alignment=ft.MainAxisAlignment.END
                        ),
                        ft.Container(
                            content=ft.Row(
                                controls=[
                                    ft.Text(
                                        value="🛠 Feito por @gustavo.python • ⚙ Powered by Python • © 2025",
                                        size=12,
                                        color=ft.Colors.GREY,
                                        opacity=0.7
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.CENTER
                            ),
                            alignment=ft.alignment.bottom_center,
                            padding=10,
                        ),
                    ],
                    expand=True
                )
            ]
        )
    )
