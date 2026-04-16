## 🔍 Explicação Detalhada de Cada Arquivo

---

### `main.py` — Orquestrador do Pipeline

**O que faz:** Coordena a execução das 3 etapas em ordem. É o único arquivo que você precisa rodar.

```python
# Verifica se o usuário pediu para pular o scraping
skip_scraping = "--skip-scraping" in sys.argv
```

**Fluxo:**
```
main.py
  │
  ├─ 1. Chama scraper.main()   → gera data/raw/livros_raw.csv
  ├─ 2. Chama etl.main()       → gera data/processed/livros_final.csv
  └─ 3. Chama analise.main()   → gera data/plots/*.png
```

---

### `src/scraper.py` — Web Scraping (Etapa 1 do KDD: Seleção)

**O que faz:** Acessa o site `books.toscrape.com` automaticamente e coleta dados de ~1000 livros.

#### Por que esse site?
- Foi criado **especificamente para prática de web scraping**
- `robots.txt` não proíbe bots
- Não exige login nem CAPTCHA
- Dados estáticos (sem JavaScript)

#### Como funciona internamente:

**1. Função `get_categorias()`**
```python
# Acessa a página inicial e extrai os links de cada gênero
# Ex: Mystery, Romance, Travel, Fiction...
categorias = get_categorias()
# Retorna: [("Mystery", "http://...mystery_3/"), ("Romance", "http://...")]
```

**2. Função `get_soup(url)`**
```python
# Faz a requisição HTTP e converte o HTML em objeto navegável
response = requests.get(url, headers=HEADERS, timeout=10)
return BeautifulSoup(response.text, "lxml")
```
O `BeautifulSoup` transforma o HTML bruto em uma estrutura que pode ser pesquisada como um dicionário.

**3. Função `parse_livro(article, genero, url)`**
```python
# Extrai os campos de cada card de livro na listagem
titulo  = article.h3.a["title"]           # Texto do atributo title
preco   = float(preco_raw.replace("£","")) # Remove símbolo da moeda
rating  = RATING_MAP[rating_class]         # "Three" → 3
```

**4. Função `get_estoque(url_livro)`**
```python
# Acessa a página INDIVIDUAL de cada livro para pegar o estoque
# Ex: "In stock (22 available)" → extrai o número 22
```
> [!NOTE]
> Isso é o que torna o scraper um pouco lento — ele visita cada livro individualmente para obter o campo `estoque`, que só aparece na página de detalhes.

**5. Função `scrape_categoria()`**
```python
# Percorre todas as páginas de uma categoria (paginação)
# Cada página tem 20 livros → percorre page-1, page-2, page-3...
while url_atual and coletados < max_por_categoria:
    # Coleta livros da página atual
    # Busca link "next" para ir à próxima página
    next_btn = soup.find("li", class_="next")
```

**Delay respeitoso:**
```python
time.sleep(0.2)  # 200ms entre cada livro
time.sleep(0.3)  # 300ms entre cada página de categoria
```
Isso evita sobrecarregar o servidor — critério ético avaliado no trabalho.

**Saída:** `data/raw/livros_raw.csv` com colunas:
```
titulo | preco | rating | genero | disponibilidade | estoque | url
```

---

### `src/etl.py` — Pipeline ETL (Etapa 2 do KDD: Pré-processamento)

**O que faz:** Lê os dados brutos, identifica e corrige todos os problemas de qualidade, e salva o dataset limpo.

#### Problemas encontrados e tratamentos:

**1. `tratar_tipos()` — Padronização de tipos**
```python
df["preco"]  = pd.to_numeric(df["preco"],  errors="coerce")  # str → float
df["rating"] = pd.to_numeric(df["rating"], errors="coerce")  # str → int
df["genero"] = df["genero"].str.strip().str.title()           # "mystery" → "Mystery"
```
> Por que? O CSV lê tudo como texto. Sem isso, `"50.0" > "9.0"` seria falso (comparação de string).

**2. `remover_duplicatas()` — Limpeza de redundâncias**
```python
df = df.drop_duplicates(subset=["titulo", "genero"])
```
> Por que `titulo + genero`? Um mesmo título pode existir em gêneros diferentes legitimamente. A combinação dos dois é o identificador único.

**3. `tratar_nulos()` — Imputação inteligente**
```python
# Preço nulo → mediana do mesmo gênero (não da base toda)
df["preco"] = df.groupby("genero")["preco"].transform(
    lambda x: x.fillna(x.median())
)
# Estoque = -1 significa que não conseguiu coletar → trata como nulo
df["estoque"] = df["estoque"].replace(-1, pd.NA)
```
> Por que mediana por gênero? Livros de "Academic" costumam custar muito mais que "Romance". Usar a mediana global distorceria o dado.

**4. `tratar_outliers()` — Identificação via IQR**
```python
Q1  = df[col].quantile(0.25)
Q3  = df[col].quantile(0.75)
IQR = Q3 - Q1
# Outlier: valor < Q1 - 1.5*IQR  OU  > Q3 + 1.5*IQR
```
> Os outliers são **documentados mas mantidos** — livros podem legitimamente ter preços extremos. A remoção seria uma decisão de modelagem posterior.

**5. `converter_rating_categorico()` — Discretização**
```python
labels = ["Muito Ruim", "Ruim", "Regular", "Bom", "Excelente"]
df["rating_cat"] = pd.cut(df["rating"], bins=[0,1,2,3,4,5], labels=labels)
```
> Cria uma variável categórica ordinal a partir do rating numérico — útil para algoritmos que funcionam melhor com categorias.

**6. `normalizar_preco()` — Min-Max Scaling**
```python
df["preco_normalizado"] = (df["preco"] - preco_min) / (preco_max - preco_min)
# Resultado: valores entre 0.0 e 1.0
```
> Prepara o campo para uso em algoritmos de ML nas fases futuras (k-NN, SVM, etc. são sensíveis à escala).

**Saída:** `data/processed/livros_final.csv` com 8 colunas:
```
titulo | preco | rating | genero | disponibilidade | estoque | rating_cat | preco_normalizado
```

---

### `src/analise.py` — EDA e Visualizações (Etapa de Apresentação do Estado da Base)

**O que faz:** Gera as estatísticas e os 7 gráficos que comporão a **Seção IV (Resultados)** do relatório IEEE.

#### Gráficos gerados (salvos em `data/plots/`):

| Arquivo | O que mostra | por que importa |
|---|---|---|
| `distribuicao_precos.png` | Histograma de preços + boxplot por rating | Distribuição e assimetria do preço |
| `top_generos.png` | Top 15 gêneros por volume | Quais gêneros têm mais livros |
| `preco_medio_genero.png` | Preço médio por gênero | Gêneros mais caros/baratos |
| `distribuicao_rating.png` | Barras de frequência por rating | Tendência de avaliações |
| `disponibilidade.png` | Pie chart In stock vs Out of stock | Proporção de livros disponíveis |
| `correlacao.png` | Heatmap de correlação numérica | Relação entre preço, rating e estoque |
| `estoque_distribuicao.png` | Histograma de estoque | Concentração de unidades |

**Exemplo do código de correlação:**
```python
corr = df[["preco", "rating", "estoque", "preco_normalizado"]].corr()
sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm")
```
> O heatmap mostra se variáveis como preço e rating têm correlação positiva, negativa ou nula — responde diretamente à pergunta de pesquisa do trabalho.
