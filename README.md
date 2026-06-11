# ⛽ DRE Dashboard — Posto de Combustível

Dashboard interativo de **Demonstrativo de Resultados** para posto de combustível,
construído com **Streamlit** e **Plotly**. Todos os dados são fictícios e destinados
a fins demonstrativos de portfólio.

---

## 📸 Funcionalidades

| Seção | O que mostra |
|---|---|
| **Visão Geral** | KPIs principais, waterfall do resultado, receita vs CMV por combustível |
| **Combustíveis** | Distribuição em pizza, tabela de margens, detalhamento de vendas à vista |
| **Produtos & Serviços** | Lubrificantes, aditivos, filtros, lava jato e troca de óleo |
| **Despesas** | Folha por setor, análise vertical (% sobre receita bruta) |
| **Cartões** | Receita bruta e taxas por operadora (Rede, Cielo, Alelo, Ticketlog…) |

---

## 🚀 Como rodar

### Pré-requisitos
- Python 3.9+
- pip

### Instalação

```bash
# Clone ou baixe a pasta dre_dashboard
cd dre_dashboard

# Instale as dependências
pip install -r requirements.txt

# Inicie o dashboard
streamlit run app.py
```

O navegador abrirá automaticamente em `http://localhost:8501`.

---

## 🖥️ Uso no VSCode

1. Instale a extensão **Streamlit** (ou rode via terminal integrado)
2. Abra `app.py`
3. No terminal: `streamlit run app.py`

---

## 📁 Estrutura

```
dre_dashboard/
├── app.py            ← Dashboard principal
├── requirements.txt  ← Dependências Python
└── README.md         ← Este arquivo
```

---

## ⚙️ Personalização / Dados Reais

Todos os dados estão concentrados na seção **`DADOS MOCKUP`** do `app.py` (linhas ~30–90).
Para conectar dados reais, substitua os dicionários e DataFrames por consultas ao seu banco
ou planilha (ex: `pd.read_csv(...)`, `pd.read_sql(...)`, API REST).

---

## 🛠️ Stack

- [Streamlit](https://streamlit.io) — interface web interativa
- [Plotly](https://plotly.com/python) — gráficos interativos
- [Pandas](https://pandas.pydata.org) — manipulação de dados

---

> **Nota:** Este projeto é de portfólio. Os dados exibidos são completamente fictícios
> e não representam nenhuma empresa real.
