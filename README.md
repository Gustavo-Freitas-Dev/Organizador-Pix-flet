# 💸 Organizador Pix

O **Organizador Pix** é uma ferramenta desenvolvida em Python com o objetivo de **padronizar e organizar extratos de transações Pix**, facilitando a leitura, conferência e tratamento de dados brutos.

---

## 📌 Funcionalidades

- 🧹 Limpeza automática de texto colado de extratos
- 🏦 Padronização de nomes de bancos (ex: "Brasil", "Bco do Brasil" → "Banco do Brasil")
- 💳 Agrupamento de dados de forma estruturada
- 📋 Botão de cópia rápida do resultado tratado
- 💾 Exportação dos dados tratados
- 🔍 Compatível com registros contendo caracteres especiais como `*`, múltiplas quebras de linha, etc.

---

## 🛠️ Tecnologias Utilizadas

- `Python`
- `Streamlit` (interface web)
- `SQLite` (base de dados local para variações de bancos)
- `Pandas` (tratamento e formatação de dados)
- `Flet` (ou alternativa visual, se aplicável)

---

## 🖥️ Como Executar

1. Clone o repositório:
   ```bash
   git clone https://github.com/Gustavo-Freitas-Dev/Organizador-Pix.git
   cd Organizador-Pix
