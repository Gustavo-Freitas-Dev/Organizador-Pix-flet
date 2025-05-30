import flet as ft
from database.connection import session
from database.models import Bancos

def viewer_database(page: ft.Page):
    data_table = ft.DataTable(
        columns=[
            ft.DataColumn(label=ft.Text("ID", weight=ft.FontWeight.BOLD)),
            ft.DataColumn(label=ft.Text("Variação", weight=ft.FontWeight.BOLD)),
            ft.DataColumn(label=ft.Text("Padronizado", weight=ft.FontWeight.BOLD)),
            ft.DataColumn(label=ft.Text("Ações", weight=ft.FontWeight.BOLD)),
        ],
        rows=[],
        column_spacing=50,
        width=950
    )

    def abrir_tela_edicao(banco_id):
        banco = session.query(Bancos).filter(Bancos.id == banco_id).first()

        if not banco:
            page.open(ft.SnackBar(
                content=ft.Text("Banco não encontrado."),
                duration=5000,
                bgcolor=ft.Colors.RED_400
                ))
            page.update()
            return

        input_variacao = ft.TextField(label="Variação", value=banco.variacao, width=680, border_radius=30)
        input_padronizado = ft.TextField(label="Nome Padronizado", value=banco.nome_padronizado, width=680, border_radius=30)

        def salvar_edicao(e):
            banco.variacao = input_variacao.value.strip()
            banco.nome_padronizado = input_padronizado.value.strip()
            session.commit()

            page.open(ft.SnackBar(
                content=ft.Text("Banco atualizado com sucesso!"),
                duration=5000,
                bgcolor=ft.Colors.GREEN_400
                )
            )
            page.update()
        

        page.views.append(
            ft.View(
                route=f"/editar-banco/{banco_id}",
                padding=30,
                controls=[
                    ft.Column([
                        ft.Row([
                            ft.Text("Editar Banco", size=30, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_700),
                            ft.IconButton(
                                icon=ft.Icons.CLOSE,
                                tooltip="Cancelar",
                                icon_color=ft.Colors.RED_600,
                                on_click=lambda e: page.go("/adicionar-banco")
                            )
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),

                        ft.Divider(),
                        # Área de resultado
                        ft.Container(
                            content=ft.Column(
                                controls=[
                                    ft.Text("Dados Tratados", size=16, weight=ft.FontWeight.BOLD),
                                    input_variacao,
                                ],
                                spacing=10,
                            ),
                            padding=20,
                            border_radius=20,
                            bgcolor=ft.Colors.GREY_50,
                            shadow=ft.BoxShadow(blur_radius=15, color=ft.Colors.GREY_400)
                        ),
                        
                        ft.Container(
                            content=ft.Column(
                                controls=[
                                    ft.Text("Dados Tratados", size=16, weight=ft.FontWeight.BOLD),
                                    input_padronizado,
                                ],
                                spacing=10,
                            ),
                            padding=20,
                            border_radius=20,
                            bgcolor=ft.Colors.GREY_50,
                            shadow=ft.BoxShadow(blur_radius=15, color=ft.Colors.GREY_400)
                        ),

                        ft.Row([
                            ft.ElevatedButton(
                                text="Salvar Alterações",
                                icon=ft.Icons.SAVE,
                                bgcolor=ft.Colors.GREEN_600,
                                color=ft.Colors.WHITE,
                                on_click=salvar_edicao
                            )
                        ], alignment=ft.MainAxisAlignment.END)
                    ])
                ]
            )
        )
        page.update()

    def remover_banco(banco_id):
        banco = session.query(Bancos).filter(Bancos.id == banco_id).first()
        if banco:
            session.delete(banco)
            session.commit()
            atualizar_tabela()
            
            page.open(ft.SnackBar(
                content=ft.Text("Banco removido com sucesso!"),
                duration=5000,
                bgcolor=ft.Colors.GREEN_400    
            ))
        else:
            page.open(ft.SnackBar(
                content=ft.Text("Banco não encontrado."),
                duration=5000,
                bgcolor=ft.Colors.RED_400
            ))
        
        page.update()

    def atualizar_tabela(filtro=""):
        bancos_filtrados = session.query(Bancos).order_by(Bancos.id).all()

        if filtro:
            filtro_lower = filtro.lower()
            bancos_filtrados = [
                b for b in bancos_filtrados
                if filtro_lower in b.variacao.lower() or filtro_lower in b.nome_padronizado.lower()
            ]

        tabela_bancos = []

        for i, banco in enumerate(bancos_filtrados, start=1):
            acoes_menu = ft.PopupMenuButton(
                items=[
                    ft.PopupMenuItem(text="Editar", on_click=lambda e, id=banco.id: abrir_tela_edicao(id)),
                    ft.PopupMenuItem(text="Remover", on_click=lambda e, id=banco.id: remover_banco(id)),
                ]
            )

            tabela_bancos.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(i))),
                        ft.DataCell(ft.Text(banco.variacao)),
                        ft.DataCell(ft.Text(banco.nome_padronizado)),
                        ft.DataCell(acoes_menu),
                    ]
                )
            )

        data_table.rows = tabela_bancos
        page.update()

    filtro_input = ft.TextField(
        label="Filtrar por nome ou variação...",
        width=400,
        border_radius=30,
        prefix_icon=ft.Icons.SEARCH,
        on_change=lambda e: atualizar_tabela(filtro_input.value)
    )

    atualizar_tabela()

    page.views.append(
        ft.View(
            route="/ver-banco",
            padding=30,
            controls=[
                ft.Column(
                    controls=[
                        ft.Row(
                            [
                                ft.Text("Visualizar Banco de Dados", size=30, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_700),
                                ft.IconButton(
                                    icon=ft.Icons.ARROW_BACK,
                                    tooltip="Voltar",
                                    icon_color=ft.Colors.BLUE_700,
                                    on_click=lambda e: page.go("/adicionar-banco")
                                )
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                        ),
                        filtro_input,
                        ft.Divider(),
                        ft.ListView(
                            controls=[
                                ft.Container(
                                    content=data_table,
                                    padding=20,
                                    bgcolor=ft.Colors.GREY_50,
                                    border_radius=15,
                                    shadow=ft.BoxShadow(blur_radius=12, color=ft.Colors.GREY_300),
                                )
                            ],
                            height=400,
                            spacing=10
                        )
                    ],
                    expand=True,
                    spacing=25
                )
            ]
        )
    )
