# Trabalho Prático – Mineração de Dados (Fase 1)
## Coleta, Tratamento e Análise Exploratória via Web Scraping
---

## Domínio Escolhido: Mercado de Livros Online

**Site:** [books.toscrape.com](http://books.toscrape.com)
> [!IMPORTANT]
> Este site foi criado **especificamente para prática de web scraping**, sem restrições no `robots.txt`, sem necessidade de autenticação e sem risco de violação de termos de uso.

**Justificativa para mineração:** Permite comparar preços, avaliações e disponibilidade por gênero literário, identificar padrões de precificação e relação entre nota e disponibilidade.

**Perguntas de pesquisa:**
1. Gêneros com maior e menor custo médio?
2. Existe correlação entre avaliação (rating) e preço?
3. Quais gêneros têm mais livros esgotados?

---

## Campos Coletados (≥ 6 campos, requisito atendido)

| Campo | Tipo | Descrição |
|---|---|---|
| `titulo` | Texto | Nome do livro |
| `preco` | **Numérico** | Preço em libras (£) |
| `rating` | **Numérico** | Avaliação de 1 a 5 |
| `estoque` | **Numérico** | Quantidade em estoque |
| `genero` | **Categórico** | Gênero/categoria do livro |
| `disponibilidade` | **Categórico** | "In stock" / "Out of stock" |
| `url` | Texto | URL da página do livro |

Total: **3 numéricos** (`preco`, `rating`, `estoque`) + **2 categóricos** (`genero`, `disponibilidade`) ✅

---

## Arquitetura do Projeto

```
trabalho_pratico_mineracao_de_dados_1/
│
├── src/
│   ├── scraper.py          # Web scraping (BeautifulSoup)
│   ├── etl.py              # Transformação e carga
│   └── analise.py          # Pré-processamento e EDA
│
├── data/
│   ├── raw/
│   │   └── livros_raw.csv  # Dados brutos coletados
│   └── processed/
│       └── livros_final.csv # Dados tratados
│
├── relatorio/
│   └── relatorio_ieee.docx  # Relatório no padrão IEEE
│
├── requirements.txt
└── README.md
```

---

## Proposed Changes

### Scraping & ETL

#### [NEW] src/scraper.py
Script de raspagem de dados do books.toscrape.com.
Coleta título, preço, rating, estoque, gênero e disponibilidade de todas as páginas (≥ 1000 registros esperados — o site tem ~1000 livros).

#### [NEW] src/etl.py
Pipeline ETL: parsing dos tipos, normalização de campos (ex: "One" → 1 para ratings), conversão de moeda, carga em CSV estruturado.

#### [NEW] src/analise.py
Pré-processamento: detecção de nulos, duplicatas, outliers, estatísticas descritivas e geração de visualizações básicas (histogramas, boxplots).

#### [NEW] requirements.txt
Dependências: `requests`, `beautifulsoup4`, `pandas`, `matplotlib`, `seaborn`.

---

## Fluxo ETL

```mermaid
graph LR
    A[Site: books.toscrape.com] -->|scraper.py - requests + BS4| B[Dados Brutos - HTML]
    B -->|Parsing HTML| C[CSV Bruto - livros_raw.csv]
    C -->|etl.py - Transformações| D[Limpeza e Normalização]
    D -->|Carga| E[CSV Final - livros_final.csv]
    E -->|analise.py - pandas + seaborn| F[Análise Exploratória]
```

---

## Estrutura do Relatório IEEE

| # | Seção | Conteúdo Principal |
|---|---|---|
| — | Título + Autores + Abstract | Título, nome, e-mail, resumo 150-250 palavras |
| I | Introdução | Contexto, motivação, perguntas de pesquisa |
| II | Fundamentação Teórica | KDD, Web Scraping, ETL, Pré-processamento |
| III | Metodologia | Fonte, ferramentas, scraping, ETL, limpeza + diagrama |
| IV | Resultados | Estatísticas descritivas, antes/depois, amostras |
| V | Conclusão | Aprendizados, limitações, próximos passos |
| — | Referências | [1] BS4 docs, [2] pandas docs, [3] livro KDD |

Limite: **10 páginas** máximo.

---

## Verification Plan

### Após rodar o código:
- [ ] `livros_raw.csv` deve ter ≥ 1000 linhas
- [ ] `livros_final.csv` deve ter ≥ 6 colunas com tipos corretos
- [ ] Script de análise gera estatísticas descritivas sem erros
- [ ] Sem valores nulos não tratados no CSV final
