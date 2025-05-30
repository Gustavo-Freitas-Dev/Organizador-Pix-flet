import flet as ft
from database.models import adicionar_banco
from database.utils import limpar_dados


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
            sucesso = adicionar_banco(variacao, padronizado)

            if sucesso:
                mensagem = ft.SnackBar(
                    content=ft.Text("Banco salvo com sucesso!"),
                    duration=5000,
                    bgcolor=ft.Colors.GREEN_400
                )
            else:
                mensagem = ft.SnackBar(
                    content=ft.Text("Erro: variação já cadastrada."),
                    duration=5000,
                    bgcolor=ft.Colors.RED_400
                )

            page.open(mensagem)
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

    view_database = ft.ElevatedButton(
        text="Visualizar Banco",
        icon=ft.Icons.REMOVE_RED_EYE_OUTLINED,
        bgcolor=ft.Colors.BLUE_600,
        color=ft.Colors.WHITE,
        tooltip="Abrir banco de dados",
        on_click=lambda e: page.go("/ver-banco")
    )


    page.views.append(
        ft.View(
            route="/adicionar-banco",
            padding=30,
            controls=[
                ft.Column(
                    controls=[
                        ft.Row(
                            controls=[
                                ft.Text("Adicionar Novo Banco", size=30, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_600),
                                view_database
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                        ),
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
                            alignment=ft.MainAxisAlignment.SPACE_EVENLY
                        ),
                        ft.Container(
                            content=ft.Row(
                                controls=[
                                    ft.Text(
                                        value="🛠 Feito por @gustavo.python • ⚙ Powered by Python • © 2025",
                                        size=12,
                                        color=ft.Colors.GREY,
                                        opacity=0.6
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                                # expand=True
                            ),
                            # alignment=ft.alignment.bottom_center,
                            padding=190,
                        ),
                    ],
                    expand=True
                )
            ]
        )
    )

