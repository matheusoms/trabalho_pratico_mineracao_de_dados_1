### Mineração de Dados 
# Trabalho Prático - Fase 1 
## Coleta, Tratamento e Análise Exploratória de Dados via Web Scraping

| Modalidade | Entrega do Relatório | Apresentação | Base Mínima |
|---|---|---|---|
| Individual ou em dupla | Até 15/04/2026 (máx. 10 páginas) | 16/04/2026 (máx. 15 minutos) | 1.000 registros, 6 campos (3 numéricos + 2 categóricos) |

**Observação:** esta fase será a base de dados para o dashboard final da disciplina. O dataset construído agora será reutilizado e incrementado nas próximas etapas. 
---

### 1. Objetivo Escolher um domínio de interesse e um site público como fonte de dados, realizar a coleta automatizada via web scraping, e aplicar o processo de KDD até a etapa de pré-processamento, documentando todas as decisões e transformações em um relatório técnico no formato IΕΕΕ. 
### 2. Etapas do Trabalho 

**2.1 Definição do Problema e da Fonte de Dados** 
* Escolher um tema/domínio de interesse (ex.: mercado imobiliário, esportes, empregos, clima, produtos de e-commerce, filmes, livros, dados públicos governamentais, entre outros). 
* Justificar a escolha do site e do tipo de dado: por que esse dado é interessante para mineração? 
* Identificar quais perguntas ou conhecimentos se espera extrair desses dados ao longo da disciplina. 

**2.2 Web Scraping (Raspagem de Dados)** 
* Implementar um script (preferencialmente em Python, utilizando bibliotecas como BeautifulSoup, Scrapy ou Selenium) para coletar os dados do site escolhido. 
* A base coletada deve conter no mínimo 1.000 registros. 
* A base deve possuir no mínimo 6 campos (atributos), sendo: pelo menos 3 campos numéricos e pelo menos 2 campos categóricos.  Os demais campos podem ser de qualquer tipo (data, texto livre, booleano, etc.). 
* Documentar no relatório: qual site, quais páginas, quais campos foram extraídos, quantos registros coletados e se houve alguma limitação técnica ou ética (robots.txt, termos de uso). 
* Entregar o código-fonte como anexo ou link para repositório (ex.: GitHub). 

**2.3 ETL (Extração, Transformação e Carga)** 
* Descrever o processo de extração (o próprio scraping), as transformações aplicadas para estruturar os dados brutos (parsing de HTML, normalização de campos, tratamento de tipos) e a carga final em um formato estruturado (CSV, JSON ou banco de dados SQLite). 
* Apresentar um diagrama ou fluxo simplificado do pipeline ETL utilizado. 

**2.4 Pré-processamento e Limpeza de Dados** 
* Identificar e tratar problemas reais encontrados nos dados coletados: valores ausentes, duplicatas, inconsistências, outliers, dados ruidosos, formatos heterogêneos. 
* Documentar com exemplos concretos. Ex.: "O campo X tinha 15% de valores nulos tratamento adotado: ..." ou "Encontradas 42 linhas duplicadas critério de remoção: ...". 
* Aplicar transformações de dados quando pertinente: normalização, discretização, codificação de variáveis categóricas, entre outras. 

**2.5 Apresentação do Estado da Base de Dados** 
* Apresentar um panorama geral da base final: quantidade de registros, quantidade de atributos, tipos de cada variável (numérica, categórica, data, texto, etc.). 
* Incluir estatísticas descritivas básicas: contagem de valores nulos por coluna, quantidade de registros antes e depois da limpeza, valores únicos em campos-chave, médias/medianas/mínimos/máximos para variáveis numéricas. 
* Mostrar amostras dos dados (ex.: tabela com as primeiras linhas ou recortes que ilustrem a estrutura da base). 
* Relacionar o estado atual da base com o processo KDD: em qual etapa estamos?  O que viria a seguir na disciplina? 

### 3. Formato do Relatório 
**Padrão IEEE** 
O relatório deve ser escrito seguindo o modelo IEEE Conference Proceedings em formato A4.  O template pode ser obtido no site oficial do IEEE:  https://www.ieee.org/conferences/publishing/templates.html 
Estão disponíveis versões em Word (.docx) e LaTeX. Para quem preferir LaTeX, o template IEEE também está disponível no Overleaf (basta buscar por "IEEE Conference Template").  Em qualquer caso, utilizar o formato A4. 

### 4. Seções Obrigatórias do Artigo 
O relatório deve conter as seguintes seções, respeitando a estrutura de um artigo científico no padrão IEEE: 

| Seção  | Descrição  |
|---|---|
| Título, Autores e Resumo (Abstract)  | Título do trabalho, nome(s) do(s) autor(es), e-mail institucional. Resumo de 150 a 250 palavras descrevendo objetivo, metodologia e principais resultados.  |
| I. Introdução  | Contextualização do tema, motivação, perguntas de pesquisa e objetivos do trabalho. Descrever brevemente o que será apresentado nas seções seguintes.  |
| II. Fundamentação Teórica  | Breve contextualização do processo KDD, conceitos de web scraping, ETL e pré-processamento. Situar o trabalho dentro do framework de descoberta de conhecimento.  |
| III. Metodologia  | Descrição detalhada das etapas realizadas: fonte de dados escolhida, ferramentas e bibliotecas utilizadas, processo de scraping, pipeline ETL, técnicas de limpeza e transformação aplicadas. Incluir diagrama do fluxo ETL. Apresentação do estado final da base: estatísticas descritivas, amostras dos dados, comparativo antes/depois da limpeza, panorama dos atributos e tipos de variáveis.  |
| IV. Resultados  |  |
| V. Conclusão  | Síntese dos aprendizados, dificuldades encontradas, limitações do trabalho e próximos passos (visão de como a base será usada nas fases seguintes e no dashboard final).  |
| Referências  | Referências no padrão IEEE (numeradas entre colchetes: [1], [2], ...). Incluir documentação das bibliotecas utilizadas e fontes consultadas.  |

Limite total: no máximo 10 páginas incluindo referências. 

### 5. Critérios de Avaliação 

| Critério  | O que será observado  |
|---|---|
| Coleta de dados  | Scraping funcional, base com no mínimo 1.000 registros e ao menos 6 campos (3 numéricos e 2 categóricos), diversidade de atributos.  |
| Documentação do ETL  | Clareza na descrição do pipeline, diagrama do fluxo, justificativa das transformações.  |
| Pré-processamento  | Tratamento adequado de problemas reais (nulos, duplicatas, outliers, inconsistências).  |
| Estado da base  | O leitor consegue entender a estrutura, volume e qualidade dos dados?  |
| Conexão com KDD  | O aluno demonstra compreensão de onde o trabalho se insere no processo de descoberta de conhecimento?  |
| Formatação e escrita  | Uso correto do template IEEE, clareza textual, organização, referências adequadas.  |
| Apresentação oral  | Domínio do conteúdo, clareza na exposição, capacidade de responder perguntas. Todos os integrantes do grupo devem apresentar.  |

### 6. Observações Finais 
* O código-fonte do scraping deve ser entregue como anexo ou via link para repositório (GitHub, GitLab, etc.). 
* A base de dados final (CSV, JSON ou SQLite) também deve ser entregue junto com o relatório. 
* Respeitar questões éticas e legais: verificar o robots.txt do site e seus termos de uso.  Não realizar requisições excessivas que possam sobrecarregar o servidor. 
* Na apresentação oral, todos os integrantes do grupo devem falar.  A apresentação deve cobrir as seções de Introdução, Metodologia, Resultados e Conclusão.  A seção de Fundamentação Teórica não precisa ser apresentada oralmente, apenas constar no relatório escrito.  A apresentação deverá ter no máximo 15 minutos. 
* Este trabalho será incrementado nas fases seguintes da disciplina com técnicas de mineração de dados (classificação, agrupamento, associação, etc.), culminando na construção de um dashboard ao final do semestre. 

Bom trabalho! 