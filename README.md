# Trabalho Prático — Mineração de Dados (Fase 1)
**Fatec | Disciplina: Mineração de Dados**

> Coleta, Tratamento e Análise Exploratória via Web Scraping

---

## 🎯 Tema: Mercado de Livros Online
**Fonte:** [books.toscrape.com](http://books.toscrape.com) *(site público criado para prática de scraping)*

**Perguntas de pesquisa:**
1. Existe correlação entre preço e avaliação?
2. Quais gêneros têm maior custo médio?
3. A disponibilidade em estoque está associada ao preço ou avaliação?

---

## ⚡ Como Executar

### 1. Instalar Python
Baixe em **https://www.python.org/downloads/** e marque **"Add Python to PATH"**.

### 2. Instalar dependências
```bash
pip install -r requirements.txt
```

### 3. Rodar o pipeline completo
```bash
python main.py
```

> O processo leva ~15–30 min. Para pular o scraping se o CSV já existir:
> ```bash
> python main.py --skip-scraping
> ```

---

## 📁 Estrutura

```
├── main.py                        # Orquestrador do pipeline
├── requirements.txt               # Dependências
├── src/
│   ├── scraper.py                 # Web Scraping (BeautifulSoup)
│   ├── etl.py                     # ETL: limpeza e transformação
│   └── analise.py                 # EDA: estatísticas e gráficos
├── data/
│   ├── raw/livros_raw.csv         # Dados brutos (gerado)
│   └── processed/livros_final.csv # Dados limpos (gerado)
│       plots/                     # Gráficos gerados (gerado)
└── relatorio/
    └── relatorio_ieee_template.md # Template do relatório
```

---

## 📊 Campos Coletados

| Campo | Tipo | Descrição |
|---|---|---|
| `titulo` | Texto | Nome do livro |
| `preco` | **Numérico** | Preço em £ |
| `rating` | **Numérico** | Avaliação 1–5 |
| `estoque` | **Numérico** | Quantidade em estoque |
| `genero` | **Categórico** | Gênero literário |
| `disponibilidade` | **Categórico** | In stock / Out of stock |
| `rating_cat` | Ordinal | Rating discretizado |
| `preco_normalizado` | Numérico | Preço Min-Max (0–1) |

✅ **Requisito:** 3 numéricos + 2 categóricos + ≥ 1000 registros

---

## 🛠️ Tecnologias
`Python 3.12` · `requests` · `BeautifulSoup4` · `pandas` · `matplotlib` · `seaborn`