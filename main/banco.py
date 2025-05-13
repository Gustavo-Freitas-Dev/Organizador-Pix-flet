import sqlite3

CAMINHO_DB = r'Z:\Compras\1. GUSTAVO - DATA USER\Python\Organizador Pix\main\bancos.db'

def conectar():
    return sqlite3.connect(CAMINHO_DB)

def inicializar_banco():
    """Cria a tabela se ela não existir."""
    with conectar() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS bancos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                variacao TEXT UNIQUE,
                nome_padronizado TEXT
            )
        """)
        conn.commit()

def adicionar_banco(variacao, nome_padronizado):
    """Adiciona uma nova variação com nome nome_padronizado."""
    with conectar() as conn:
        conn.execute("""
            INSERT OR REPLACE INTO bancos (variacao, nome_padronizado)
            VALUES (?, ?)
        """, (variacao.strip(), nome_padronizado.strip()))
        conn.commit()

def listar_bancos():
    """Retorna todas as variações e nomes nome_padronizados como dicionário."""
    with conectar() as conn:
        cursor = conn.execute("SELECT variacao, nome_padronizado FROM bancos")
        return {variacao: nome_padronizado for variacao, nome_padronizado in cursor.fetchall()}