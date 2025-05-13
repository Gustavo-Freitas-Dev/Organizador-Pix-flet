import flet as ft
import re

def tratar_dados(e, origem_field, dados_tratados):
    dados_tratados.value = ''
    dados_tratados.update()

    texto = origem_field.value.split('\n')

    bancos = [
        # 🏦 Bancos Tradicionais  
        "Bradesco", "Bradeskoo", "Bradescco", "Braddesco", "Bradesko", "Bradescu", "Brad", "Bradesku",
        "Brasil", "Braasil", "Brasiil", "Brasill", "Bbrasil", "Bco Brasil", "Banco Brasil", "BB",
        "Itaú", "Itau", "Itaaú", "Itáu", "Itú", "Ituá", "Itauu", "Ittau", "Itaw", "Itaubank", "Itabank",
        "CEF", "Caixa Econômica", "Caixa Economica", "Caiixa Econômica", "Cxa Econômica", "Cxa Eco",
        "CaixaEconômica", "CaixaEcono", "C.E.F.", "C.E.F", "C E F", "Caixa", "Cx",
        "Nubank", "Nubamk", "Nubamkk", "Nobank", "NuBank", "Nu", "Nu Banq", "Nubenk", "Nubanco",
        "Santander", "Santandeer", "Santandre", "SantanderBank", "Santander Brasil", "Santander Banck",
        "Santander Bco", "Santanderr", "Sataander", "SantanderBank", "Santanderrrr",
        "Basa", "Banco da Amazônia", "Banco Amazonia", "Bancoo Amazonia", "Banco Amazônia", "BASA",

        # 🏦 Bancos Específicos  
        "Banco do Brasil", "Banco d Brasil", "Banco Brasil", "Banco do Brasiil", "Bancoo do Brasil",
        "Banco do Brásill", "Bco Brasil", "Bancoo Brasil", "BancoBrasill", "BBrasil",
        "Banco Safra", "Safra", "BancoSaffra", "Saffra", "Safrabank", "Safrabanco",
        "Banrisul", "Banrisull", "Banrisuul", "Bannrisul", "Banrisool", "Banriisul", "BanriSul",
        "Banestes", "Banestess", "Banesteees", "Banco do Estado do Espírito Santo", "Banestes Bco",

        # 💳 Bancos Digitais e Fintechs  
        "Banco Original", "Original", "BancoOrig", "BancoOrigin", "Origbank", "Orig Banq",
        "BTG", "BTG Pactual", "BTGPatual", "BTG Bank", "BtgP", "BTG Pctual",
        "XP Investimentos", "XP", "XP Invest", "XPInves", "XP Inc", "XP Finance", "XP Banco", "XPB",
        "Neon", "Banco Neon", "Nneon", "NeoBank", "Neo", "Neo Banq", "NeoBanck", "Neo Bco",
        "C6 Bank", "C6", "C6Bank", "C6 (336)", "C 6", "Banco C6", "C6Banck", "Cseis", "C-6",
        "Stone", "StoneBank", "Stone Pagamentos", "Stonne", "Stonn", "StoneP", "StoneBco",
        "Picpay", "Pic Pay", "PikPay", "PICPAY", "PiccPay", "Picp", "PickPay", "Pikpay",
        
        # 💰 Cooperativas de Crédito  
        "Sicredi", "Sicred", "Sicrredi", "Siccreddi", "Siccredi", "SicredBank", "Sicredy",
        "Sicoob", "Sicob", "Sicobb", "Sicoobb", "Sicoob Banco", "Sicobbank", "Sicob Bco",
        
        # 💵 Outros  
        "Inter", "Banco Inter", "Intter", "Bco Inter", "Inter Bank", "Interbank", "Interbanco", "InterBanck",
        "PIX", "Pix", "PIX Banco", "PixBank", "Pix Banck", "PixBanc", "Pix Bancoo", "PixB", "Pix Finance"
    ]


    bancos_regex = "|".join(re.escape(banco) for banco in bancos)
 
    padrao = re.compile(
        rf"(?P<banco>{bancos_regex})\s*"  
        r"(?P<nome>[A-Za-zÀ-ÖØ-öø-ÿ0-9&\s.\-]+?)\s+PIX\s+"  
        r"(?:(?:CPF|CNPJ)\s*(?P<chave>[\d. /-]+)|"
        r"Email\s*(?P<email>[\w.\-]+@[a-zA-Z0-9.\-]+)|"  
        r"Fone\s*(?P<fone>\+?[0-9\s()\-]+))\s*"  
        r"(?:AG\s*(?P<agencia>[0-9\-A-Za-z]+))?\s*"  
        r"(?:C[\/\s]?(?:C|POUP|C/C|CC|CPOUP|CNPJ|C/POUP)?\s*(?P<conta>[\w.\-]+))?\s*"  
        r"R\$\s*(?P<valor>\d{1,3}(?:[.,]?\d{3})*[.,]\d{2})",  
        flags=re.IGNORECASE
    )

    resultados = []
    total_valor = 0.0
    total_contas = 0

    for match in padrao.finditer("\n".join(texto)):
        dados = match.groupdict()
        banco = dados['banco'] or 'Não informado'
        chave_pix = dados.get('chave') or dados.get('email') or dados.get('fone') or 'Não informado'
        agencia = dados.get('agencia', 'Não informada')
        conta = dados.get('conta', 'Não informada')
        valor_texto = dados.get('valor', '0,00')

        
        if len(valor_texto) >=2:
            casa_decimais = valor_texto[-2:]
            centena = valor_texto[:-3]
            total_valor += float(f'{centena.replace('.','').replace(',', '')}.{casa_decimais}')
            valor_formatado = f'{centena},{casa_decimais}'
            print(valor_formatado)
    

        

        resultado = (
            f"Banco: {banco}\n"
            f"Nome: {dados['nome'].strip()}\n"
            f"Chave Pix: {chave_pix}\n"
            f"Agência: {agencia}\n"
            f"Conta: {conta}\n"
            f"Valor: {valor_formatado}\n"
            f"{'-'*40}\n"
        )

        if resultado not in resultados:  # Evita duplicações
            resultados.append(resultado)
            total_contas += 1
    print(total_valor)
    valor_total_formatado = f"R$ {total_valor:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

    if resultados:
        dados_tratados.value = "\n".join(resultados) + f"\nTotal de transações: {total_contas}\nTotal em valor: {valor_total_formatado}\n"
    else:
        dados_tratados.value = "Nenhuma transação válida encontrada."

    dados_tratados.update()

    
# Função para limpar os dados (limpa os campos de texto)
def limpar_dados(e, origem_field, dados_tratados):
    origem_field.value = ""  # Limpa o campo de origem
    dados_tratados.value = ""  # Limpa o campo de dados tratados
    origem_field.update()  # Atualiza o campo origem
    dados_tratados.update()  # Atualiza o campo de dados tratados

# Função para a interface do usuário
def main(page: ft.Page):
    global origem_field, dados_tratados

    # Função para copiar os dados tratados para a área de transferência
    def copiar_para_area_de_transferencia(e):
        page.set_clipboard(dados_tratados.value)  # Copia os dados para a área de transferência
        page.open(ft.SnackBar(ft.Text("Dados copiados com sucesso!"), duration=2000))  # Exibe uma notificação
        page.update()

    # Configuração inicial da página
    page.window.width = 800
    page.window.height = 700
    page.theme_mode = ft.ThemeMode.LIGHT  # Tema claro
    page.padding = 30
    page.window.resizable = False  # Não permite redimensionamento
    page.title = 'Pix Organiza'  # Título da página

    # Definição dos campos de texto
    origem_field = ft.TextField(
        label="Digite os dados a serem tratados",
        width=680,
        bgcolor=ft.colors.GREY_100,
        border_radius=20,
        focused_border_color='2196F3',
        expand=True
    )

    dados_tratados = ft.TextField(
        label="Dados tratados",
        multiline=True,
        expand=True,
        bgcolor=ft.colors.GREY_100,
        border_radius=20,
        focused_border_color="#2196F3",
        disabled=False,
        read_only=True,
    )

    # Botões de ação
    btn_copiar_dados = ft.TextButton(
        text='Copiar Dados',
        icon=ft.icons.COPY,
        icon_color=ft.colors.WHITE,
        tooltip='Copiar Dados',
        width=200,
        style=ft.ButtonStyle(
            bgcolor=ft.colors.BLUE_300,
            color=ft.colors.WHITE,
        ),
        on_click=copiar_para_area_de_transferencia  # Ação de copiar os dados
    )

    btn_limpar_dados = ft.TextButton(
        text='Limpar Dados',
        icon=ft.icons.DELETE_OUTLINE,
        icon_color=ft.colors.WHITE,
        tooltip='Limpar Dados',
        width=200,
        style=ft.ButtonStyle(
            bgcolor=ft.colors.RED,
            color=ft.colors.WHITE,
        ),
       on_click=lambda e: limpar_dados(e, origem_field, dados_tratados)  # Ação de limpar os dados
    )

    btn_tratar_dados = ft.TextButton(
        text='Tratar os Dados',
        icon=ft.icons.FORMAT_LIST_BULLETED,
        icon_color=ft.colors.WHITE,
        tooltip='Tratar Dados',
        width=200,
        style=ft.ButtonStyle(
            bgcolor=ft.colors.GREEN,
            color=ft.colors.WHITE,
        ),
        on_click=lambda e: tratar_dados(e, origem_field, dados_tratados)  # Ação de tratar os dados
    )
    
    # Adicionando os controles à página
    page.add(
        ft.Column(
            controls=[ 
                ft.Text("Organizador de Pix", size=30, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_600),
                ft.Divider(),
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Text('Dados das Transações', size=16, weight=ft.FontWeight.BOLD),
                            ft.Row([origem_field], alignment=ft.MainAxisAlignment.START),
                        ],
                        spacing=10
                    ),
                    padding=20,
                    border_radius=20,
                    bgcolor=ft.colors.GREY_50,
                    shadow=ft.BoxShadow(blur_radius=15, color=ft.colors.GREY_400)
                ),
            ]
        ),
        ft.Column(
            controls=[
                ft.Divider(),
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Text('Dados Tratados', size=16, weight=ft.FontWeight.BOLD),
                            dados_tratados,  # Exibe os dados tratados
                        ],
                        spacing=10,
                        expand=True,
                    ),
                    padding=20,
                    border_radius=20,
                    bgcolor=ft.colors.GREY_50,
                    shadow=ft.BoxShadow(blur_radius=15, color=ft.colors.GREY_400),
                    expand=True,
                ),
            ],
            expand=True,
        ),
        ft.Row([btn_tratar_dados, btn_limpar_dados, btn_copiar_dados ], alignment=ft.MainAxisAlignment.END)
    )

    page.update()

# Iniciar o app
ft.app(target=main, view=ft.WEB_BROWSER, port=8550, host="0.0.0.0")

