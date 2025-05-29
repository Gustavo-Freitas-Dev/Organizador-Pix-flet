import re
import unicodedata
from database.models import Bancos
from database.connection import session


# 🔹 Normaliza e limpa o texto de entrada
def limpar_entrada(texto: str) -> str:
    texto = unicodedata.normalize('NFKC', texto)
    texto = re.sub(r'\*+', ' ', texto)
    texto = texto.replace('\r', '\n')
    texto = re.sub(r'[ \t]+', ' ', texto)
    texto = re.sub(r'(?i)(PIX\s+(?:CPF|CNPJ|Email|Fone)?\s*[\d@+\-.\s]+)', r'\n\1', texto)
    texto = re.sub(r'\n{2,}', '\n', texto)
    return texto.strip()


# 🔹 Limpa os campos da interface
def limpar_dados(e, origem_field, dados_tratados):
    origem_field.value = ""
    dados_tratados.value = ""
    origem_field.update()
    dados_tratados.update()


# 🔹 Lógica principal de tratamento de dados
def tratar_dados(e, origem_field, dados_tratados):
    texto_limpo = limpar_entrada(origem_field.value)
    linhas = texto_limpo.split('\n')
    transacoes = extrair_transacoes(linhas)
    resultado, total_valor, total_contas = montar_resultado(transacoes)

    dados_tratados.value = (
        resultado +
        f"Total de transações: {total_contas}\n"
        f"Total em valor: R$ {formatar_valor_final(total_valor)}\n"
        if resultado else "Nenhuma transação válida encontrada."
    )

    dados_tratados.update()


# 🔹 Busca o nome padronizado do banco via SQLAlchemy
def buscar_banco_padronizado(nome_banco_raw: str) -> str | None:
    try:
        banco = session.query(Bancos).filter(
            Bancos.variacao.ilike(nome_banco_raw.strip())
        ).first()
        return banco.nome_padronizado if banco else None
    finally:
        session.close()


# 🔹 Extrai transações com regex e padroniza banco
def extrair_transacoes(linhas: list[str]) -> list[dict]:
    padrao = re.compile(
        r"(?:(?P<banco>.+?)\s*-\s*)?"  # Banco (opcional) antes do hífen
        r"(?P<nome>[A-Za-zÀ-ÖØ-öø-ÿ0-9&\s.\-]+?)\s+PIX\s+"
        r"(?:(?:CPF|CNPJ)\s*(?P<chave>[\d. /-]+)|"
        r"Email\s*(?P<email>[\w.\-]+@[a-zA-Z0-9.\-]+)|"
        r"Fone\s*(?P<fone>\+?[0-9\s()\-]+))\s*"
        r"(?:AG\s*(?P<agencia>[0-9\-A-Za-z]+))?\s*"
        r"(?:C[\/\s]?(?:C|POUP|C/C|CC|CPOUP|CNPJ|C/POUP)?\s*(?P<conta>[\w.\-]+))?\s*"
        r"R\$\s*(?P<valor>\d{1,3}(?:[.,]?\d{3})*[.,]\d{2})",
        flags=re.IGNORECASE
    )

    texto = "\n".join(linhas)
    transacoes = []

    for match in padrao.finditer(texto):
        dados = {k.lower(): v for k, v in match.groupdict().items()}
        banco_bruto = dados.get("banco") or ""
        
        # Tenta encontrar nome padronizado no banco de dados
        nome_padronizado = buscar_banco_padronizado(banco_bruto.strip())
        dados["banco"] = nome_padronizado if nome_padronizado else "Não informado"

        transacoes.append(dados)

    return transacoes



# 🔹 Monta resultado e calcula totais
def montar_resultado(transacoes: list[dict]) -> tuple[str, float, int]:
    resultados = []
    total_valor = 0.0
    total_contas = 0

    for dados in transacoes:
        banco = dados.get("banco") or "Não informado"
        banco = banco.strip()
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


# 🔹 Formata CPF/CNPJ como link ou chave limpa
def formatar_chave_pix(chave: str) -> str:
    if not chave:
        return "Não informado"

    chave_num = re.sub(r"[^\d]", "", chave)
    if len(chave_num) == 14:
        return f"CNPJ: www.pixcnpj.com/{chave_num}"
    elif len(chave_num) == 11:
        return f"CPF: {chave_num}"
    return chave.strip()


# 🔹 Trata valor e retorna em float + string formatada
def tratar_valor(valor_str: str) -> tuple[str, float]:
    try:
        valor_str = valor_str.strip().replace(" ", "")
        if re.match(r"^\d+\.\d{2}$", valor_str):
            valor_float = float(valor_str)
        else:
            valor_str = valor_str.replace(".", "").replace(",", ".")
            valor_float = float(valor_str)

        valor_formatado = f"{valor_float:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except Exception:
        valor_float = 0.0
        valor_formatado = "0,00"

    return valor_formatado, valor_float


# 🔹 Formata valor total final
def formatar_valor_final(valor_float: float) -> str:
    return f"{valor_float:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
