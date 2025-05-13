import re
import unicodedata



def limpar_entrada(texto):
    """Remove caracteres problemáticos e normaliza espaços."""
    texto = unicodedata.normalize('NFKC', texto)
    texto = re.sub(r'\*+', ' ', texto)  # Remove asteriscos
    texto = texto.replace('\r', '\n')
    texto = re.sub(r'[ \t]+', ' ', texto)  # Remove espaços excessivos
    texto = re.sub(r'\n{2,}', '\n', texto)  # Remove linhas em branco duplicadas
    return texto.strip()

def limpar_dados(e, origem_field, dados_tratados):
    origem_field.value = ""
    dados_tratados.value = ""
    origem_field.update()
    dados_tratados.update()

def tratar_dados(e, origem_field, dados_tratados):
    """Executa o tratamento dos dados brutos e exibe o resultado formatado."""
    texto_limpo = limpar_entrada(origem_field.value)
    linhas = texto_limpo.split('\n')
    transacoes = extrair_transacoes(linhas)
    resultado, total_valor, total_contas = montar_resultado(transacoes)

    if resultado:
        dados_tratados.value = (
            resultado +
            f"Total de transações: {total_contas}\n"
            f"Total em valor: R$ {formatar_valor_final(total_valor)}\n"
        )
    else:
        dados_tratados.value = "Nenhuma transação válida encontrada."

    dados_tratados.update()


def extrair_transacoes(linhas):
    """Extrai transações do texto com base em expressão regular."""
    padrao = re.compile(
        r"(?P<banco>[\w\s().-]+?)\s+"
        r"(?P<nome>[A-Za-zÀ-ÖØ-öø-ÿ0-9&\s.\-]+?)\s+PIX\s+"
        r"(?:(?:CPF|CNPJ)\s*(?P<chave>[\d. /-]+)|"
        r"Email\s*(?P<email>[\w.\-]+@[a-zA-Z0-9.\-]+)|"
        r"Fone\s*(?P<fone>\+?[0-9\s()\-]+))\s*"
        r"(?:AG\s*(?P<agencia>[0-9\-A-Za-z]+))?\s*"
        r"(?:C[\/\s]?(?:C|POUP|C/C|CC|CPOUP|CNPJ|C/POUP)?\s*(?P<conta>[\w.\-]+))?\s*"
        r"R\$\s*(?P<valor>\d{1,3}(?:[.,]?\d{3})*[.,]\d{2})",
        flags=re.IGNORECASE
    )
    return [match.groupdict() for match in padrao.finditer("\n".join(linhas))]

def montar_resultado(transacoes):
    """Monta a saída formatada e calcula totais."""
    resultados = []
    total_valor = 0.0
    total_contas = 0

    for dados in transacoes:
        banco = dados.get("banco", "").strip() or "Não informado"
        nome = dados.get("nome", "").strip() or "Não informado"
        agencia = (dados.get("agencia") or "-").strip()
        conta = (dados.get("conta") or "-").strip()
        chave_pix = formatar_chave_pix(
            dados.get("chave") or dados.get("email") or dados.get("fone") or "Não informado"
        )

        valor_formatado, valor_float = tratar_valor(dados.get("valor", "0,00"))
        total_valor += valor_float

        texto_formatado = (
            f"🏦 Banco: {banco}\n"
            f"👤 Nome: {nome}\n"
            f"🔑 Chave Pix: {chave_pix}\n"
            f"🏢 Agência: {agencia}\n"
            f"💳 Conta: {conta}\n"
            f"💰 Valor: R$ {valor_formatado}\n"
            f"{'─'*40}\n"
        )

        if texto_formatado not in resultados:
            resultados.append(texto_formatado)
            total_contas += 1

    return "".join(resultados), total_valor, total_contas

def formatar_chave_pix(chave):
    """Formata CPF/CNPJ como link ou limpa chave numérica."""
    if not chave:
        return "Não informado"
    if re.fullmatch(r"[\d.\-/ ()]+", chave):
        chave_num = re.sub(r"[^\d]", "", chave)
        if len(chave_num) == 14:
            return f"CNPJ: www.pixcnpj.com/{chave_num}"
        elif len(chave_num) == 11:
            return f"CPF: {chave_num}"
        return chave_num
    return chave

def tratar_valor(valor_str):
    """Formata valor em R$ e retorna também como float."""
    try:
        valor_str = valor_str.strip().replace(" ", "")

        # Caso seja no formato americano com ponto decimal (ex: 750.00)
        if re.match(r"^\d+\.\d{2}$", valor_str):
            valor_float = float(valor_str)
        else:
            # Trata vírgula como separador decimal (formato brasileiro)
            valor_str = valor_str.replace(".", "").replace(",", ".")
            valor_float = float(valor_str)

        # Formata de volta para padrão brasileiro com vírgula
        valor_formatado = f"{valor_float:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except Exception:
        valor_float = 0.0
        valor_formatado = "0,00"

    return valor_formatado, valor_float


def formatar_valor_final(valor_float):
    """Formata valor total no padrão brasileiro."""
    return f"{valor_float:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
