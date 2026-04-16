# Estrutura do Relatório IEEE — Mineração de Dados Fase 1

## Título
**Coleta e Análise Exploratória de Dados de Livros via Web Scraping: Uma Abordagem KDD Aplicada ao Mercado Editorial Online**

**Autores:** [Seu Nome] — [seu.email@fatec.sp.gov.br]
**Instituição:** Fatec — Faculdade de Tecnologia de São Paulo

---

## Abstract (150–250 palavras)
> *Escreva por último, após terminar o artigo*

Este trabalho apresenta a primeira fase de um processo de descoberta de conhecimento em bases de dados (KDD) aplicado ao domínio de livros comercializados online. O site books.toscrape.com foi utilizado como fonte de dados pública e de acesso livre, adequada para prática de raspagem de dados. Um pipeline automatizado de web scraping foi implementado em Python utilizando as bibliotecas Requests e BeautifulSoup, coletando [XXX] registros com [7] atributos — três numéricos (preço, avaliação e estoque) e dois categóricos (gênero e disponibilidade). O processo de ETL envolveu normalização de tipos de dados, remoção de duplicatas, tratamento de valores ausentes por imputação de mediana e identificação de outliers pelo método IQR. A análise exploratória revelou padrões como a distribuição de preços entre £10 e £50, com mediana de £[X], e a predominância de livros disponíveis em estoque ([X]%). As transformações aplicadas e os resultados descritivos são documentados neste artigo, posicionando o dataset como base sólida para aplicação de técnicas de mineração nas fases subsequentes da disciplina.

**Palavras-chave:** Web Scraping, KDD, ETL, Pré-processamento de Dados, Análise Exploratória.

---

## I. INTRODUÇÃO

### Contextualização
O crescimento do comércio eletrônico gerou grandes volumes de dados públicos e estruturados que podem ser explorados para extração de conhecimento. O mercado de livros online, em particular, apresenta padrões ricos em preços, avaliações e disponibilidade que se prestam a análises multidimensionais.

### Motivação
A capacidade de coletar, estruturar e analisar dados da web de forma automatizada é uma habilidade fundamental em ciência de dados. Este trabalho aplica essa capacidade a um domínio cotidiano, tornando os resultados mais interpretáveis.

### Perguntas de Pesquisa
1. Existe correlação entre o preço de um livro e sua avaliação?
2. Quais gêneros apresentam maior e menor custo médio?
3. A disponibilidade em estoque está associada a alguma faixa de preço ou avaliação?

### Objetivos
- Coletar automaticamente dados de livros via web scraping
- Aplicar um pipeline ETL robusto sobre os dados brutos
- Apresentar o estado final da base como ponto de partida para mineração de dados

### Organização do Artigo
A Seção II apresenta a fundamentação teórica. A Seção III descreve a metodologia. A Seção IV apresenta os resultados da análise exploratória. A Seção V conclui o trabalho.

---

## II. FUNDAMENTAÇÃO TEÓRICA

### A. Processo KDD
O KDD (Knowledge Discovery in Databases) é um processo iterativo composto pelas etapas de seleção, pré-processamento, transformação, mineração e interpretação de dados [1]. Este trabalho cobre as três primeiras etapas.

### B. Web Scraping
Web scraping é a técnica de extração automatizada de dados de páginas HTML. Ferramentas como BeautifulSoup permitem parsear o DOM de páginas web e extrair elementos específicos com precisão [2].

### C. ETL (Extração, Transformação e Carga)
O processo ETL estrutura dados brutos em um formato adequado para análise: extração da fonte, transformação (limpeza, normalização, codificação) e carga em um destino estruturado [3].

### D. Pré-processamento de Dados
O pré-processamento abrange tratamento de valores ausentes, remoção de duplicatas, detecção de outliers e transformações como normalização e discretização — etapas que impactam diretamente a qualidade das análises subsequentes [4].

---

## III. METODOLOGIA

### A. Fonte de Dados
- **Site:** books.toscrape.com
- **Justificativa:** Site criado especificamente para prática de web scraping. Sem restrições no `robots.txt`, sem termos de uso proibitivos, sem necessidade de autenticação.
- **Escopo:** Todas as categorias disponíveis, cobrindo [XXX] gêneros literários.

### B. Ferramentas e Bibliotecas
| Biblioteca | Versão | Finalidade |
|---|---|---|
| requests | 2.31.0 | Requisições HTTP |
| beautifulsoup4 | 4.12.3 | Parsing HTML |
| pandas | 2.2.2 | Manipulação de dados |
| matplotlib | 3.8.4 | Visualizações |
| seaborn | 0.13.2 | Visualizações estatísticas |

### C. Processo de Web Scraping
O script `scraper.py` realiza:
1. Enumeração de todas as categorias da página inicial
2. Para cada categoria, paginação completa extraindo dados da listagem
3. Acesso individual a cada livro para obter a quantidade em estoque
4. Delay de 0,2–0,3s entre requisições para não sobrecarregar o servidor

**Campos extraídos:**
- `titulo` — título do livro (texto)
- `preco` — preço em libras (numérico)
- `rating` — avaliação de 1 a 5 (numérico)
- `genero` — categoria literária (categórico)
- `disponibilidade` — In stock / Out of stock (categórico)
- `estoque` — quantidade disponível (numérico)

### D. Pipeline ETL

```
[books.toscrape.com]
       │
       ▼ scraper.py (requests + BeautifulSoup)
[livros_raw.csv — dados brutos]
       │
       ▼ etl.py (pandas)
  ├── Ajuste de tipos (float, int, str)
  ├── Remoção de duplicatas (título + gênero)
  ├── Tratamento de nulos (mediana por grupo)
  ├── Identificação de outliers (IQR)
  ├── Discretização do rating → rating_cat
  └── Normalização do preço (Min-Max)
       │
       ▼
[livros_final.csv — dados tratados]
       │
       ▼ analise.py (pandas + seaborn)
[Estatísticas descritivas + Gráficos]
```

### E. Pré-processamento — Problemas Encontrados e Soluções
| Problema | Frequência | Tratamento Adotado |
|---|---|---|
| Rating textual ("One", "Two"...) | 100% dos registros | Mapeamento para inteiro 1–5 |
| Símbolo £ e Â no preço | 100% dos registros | Remoção via `.replace()` |
| Estoque indisponível (-1) | [X]% dos registros | Substituído por 0 (out of stock) ou 1 (in stock sem info) |
| Duplicatas por categoria | [X] registros | Removidos por título + gênero |
| Preços nulos | [X] registros | Imputação pela mediana do gênero |

---

## IV. RESULTADOS

### A. Panorama Geral da Base Final
- **Registros:** [XXX] livros
- **Atributos:** 8 colunas (3 numéricas, 2 categóricas, 1 ordinal, 2 texto)
- **Registros antes da limpeza:** [XXX]
- **Registros após a limpeza:** [XXX] (removidos: [X])

### B. Estatísticas Descritivas
*[Inserir tabela gerada pelo analise.py]*

### C. Visualizações
*[Inserir gráficos de data/plots/]:*
- Distribuição de preços (histograma + boxplot por rating)
- Top 15 gêneros por volume
- Preço médio por gênero
- Distribuição de avaliações
- Pie chart de disponibilidade
- Matriz de correlação
- Distribuição de estoque

### D. Posicionamento no Processo KDD
Atualmente o trabalho se encontra na etapa de **pré-processamento e transformação** do KDD. A próxima etapa — a ser realizada nas fases seguintes da disciplina — envolve a **mineração de dados** propriamente dita (classificação, agrupamento e regras de associação), seguida pela **interpretação e visualização** final no dashboard.

---

## V. CONCLUSÃO

Este trabalho cumpriu os objetivos propostos: coletou [XXX] registros do site books.toscrape.com com 6+ atributos, construiu um pipeline ETL documentado e apresentou análise exploratória completa do dataset resultante.

**Principais aprendizados:**
- Web scraping requer tratamento cuidadoso de variações de formato no HTML
- A etapa de ETL revelou mais problemas de qualidade do que o esperado (especialmente no campo de estoque)
- Análise exploratória antecipa quais variáveis serão mais informativas na mineração

**Limitações:**
- O site agrupa livros em até 50 categorias com listas limitadas — expandir para múltiplas páginas aumenta a cobertura
- Preços em libras (£) não foram convertidos para BRL (fora do escopo)

**Próximos passos:**
O dataset será incrementado nas fases seguintes com técnicas de classificação (prever rating a partir de preço e gênero), agrupamento (clustering de livros por perfil) e associação (co-ocorrência de gêneros), culminando em um dashboard analítico.

---

## REFERÊNCIAS

[1] U. M. Fayyad, G. Piatetsky-Shapiro, P. Smyth, "From Data Mining to Knowledge Discovery in Databases," *AI Magazine*, vol. 17, no. 3, pp. 37–54, 1996.

[2] Richardson, L., "Beautiful Soup Documentation," Crummy.com, 2024. [Online]. Disponível em: https://www.crummy.com/software/BeautifulSoup/bs4/doc/

[3] Kimball, R., Ross, M., "The Data Warehouse Toolkit," 3rd ed., Wiley, 2013.

[4] Han, J., Kamber, M., Pei, J., "Data Mining: Concepts and Techniques," 3rd ed., Morgan Kaufmann, 2011.

[5] McKinney, W., "pandas: a Foundational Python Library for Data Analysis and Statistics," *Python for High Performance and Scientific Computing*, 2011. Disponível em: https://pandas.pydata.org/

[6] Waskom, M., "seaborn: statistical data visualization," *Journal of Open Source Software*, 6(60), 3021, 2021.
