"""
analise.py - Análise Exploratória de Dados (EDA) + Pré-processamento
Disciplina: Mineração de Dados - Trabalho Prático Fase 1

Gera estatísticas descritivas e visualizações para o relatório.
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
import os
import warnings

warnings.filterwarnings("ignore")
matplotlib.use("Agg")  # Modo sem janela (salva como arquivo)

# ─── Configuração ─────────────────────────────────────────────────────────────
PROCESSED_FILE = os.path.join(
    os.path.dirname(__file__), "..", "data", "processed", "livros_final.csv"
)
PLOTS_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "plots")

sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams["figure.dpi"] = 120
plt.rcParams["font.family"] = "DejaVu Sans"


# ─── Carregamento ─────────────────────────────────────────────────────────────

def carregar():
    df = pd.read_csv(PROCESSED_FILE, encoding="utf-8")
    print(f"\n✅ Dataset carregado: {len(df)} registros, {len(df.columns)} colunas")
    return df


# ─── Seção IV do Relatório: Resultados ─────────────────────────────────────────

def secao_panorama_geral(df: pd.DataFrame):
    """2.5 - Apresentação do Estado da Base de Dados"""
    print("\n" + "="*60)
    print("PANORAMA GERAL DO DATASET FINAL")
    print("="*60)

    print(f"\n📊 Registros  : {len(df)}")
    print(f"📋 Atributos  : {len(df.columns)}")
    print(f"\nTipos de variáveis:")
    print(df.dtypes.to_string())

    print(f"\n{'─'*40}")
    print("Primeiras 5 linhas (amostra):")
    print(df.head().to_string(index=False))

    print(f"\n{'─'*40}")
    print("Nulos por coluna:")
    nulos = df.isnull().sum()
    pct = (nulos / len(df) * 100).round(2)
    print(pd.DataFrame({"Nulos": nulos, "%": pct}).to_string())


def secao_descritivas(df: pd.DataFrame):
    """Estatísticas descritivas das variáveis numéricas."""
    print("\n" + "="*60)
    print("ESTATÍSTICAS DESCRITIVAS (VARIÁVEIS NUMÉRICAS)")
    print("="*60)
    desc = df[["preco", "rating", "estoque"]].describe().T
    desc.columns = ["N", "Média", "Desvio Pad.", "Mín", "Q1", "Mediana", "Q3", "Máx"]
    print(desc.round(2).to_string())

    print(f"\n{'─'*40}")
    print("Distribuição de 'rating_cat':")
    print(df["rating_cat"].value_counts().to_string())

    print(f"\n{'─'*40}")
    print("Distribuição de 'disponibilidade':")
    print(df["disponibilidade"].value_counts().to_string())

    print(f"\n{'─'*40}")
    print(f"Gêneros únicos: {df['genero'].nunique()}")
    print("Top 10 gêneros por volume:")
    print(df["genero"].value_counts().head(10).to_string())


# ─── Visualizações ─────────────────────────────────────────────────────────────

def plot_distribuicao_precos(df: pd.DataFrame):
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    # Histograma
    axes[0].hist(df["preco"], bins=30, color="#4C72B0", edgecolor="white", alpha=0.85)
    axes[0].set_title("Distribuição de Preços (£)")
    axes[0].set_xlabel("Preço (£)")
    axes[0].set_ylabel("Frequência")

    # Boxplot por rating
    df.boxplot(column="preco", by="rating", ax=axes[1],
               color=dict(boxes="#4C72B0", whiskers="#4C72B0",
                          medians="#DD8452", caps="#4C72B0"))
    axes[1].set_title("Preço por Rating")
    axes[1].set_xlabel("Rating (1–5)")
    axes[1].set_ylabel("Preço (£)")
    plt.suptitle("")

    plt.tight_layout()
    path = os.path.join(PLOTS_DIR, "distribuicao_precos.png")
    plt.savefig(path, bbox_inches="tight")
    plt.close()
    print(f"  ✅ Salvo: {path}")


def plot_top_generos(df: pd.DataFrame):
    top15 = df["genero"].value_counts().head(15).reset_index()
    top15.columns = ["genero", "count"]

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=top15, x="count", y="genero", palette="Blues_r", ax=ax)
    ax.set_title("Top 15 Gêneros por Quantidade de Livros")
    ax.set_xlabel("Quantidade")
    ax.set_ylabel("Gênero")

    plt.tight_layout()
    path = os.path.join(PLOTS_DIR, "top_generos.png")
    plt.savefig(path, bbox_inches="tight")
    plt.close()
    print(f"  ✅ Salvo: {path}")


def plot_preco_medio_por_genero(df: pd.DataFrame):
    top_gen = df["genero"].value_counts().head(12).index
    df_top = df[df["genero"].isin(top_gen)]
    media_genero = df_top.groupby("genero")["preco"].mean().sort_values(ascending=False)

    fig, ax = plt.subplots(figsize=(10, 6))
    media_genero.plot(kind="barh", ax=ax, color="#4C72B0", alpha=0.85)
    ax.set_title("Preço Médio por Gênero (Top 12)")
    ax.set_xlabel("Preço Médio (£)")
    ax.set_ylabel("Gênero")

    plt.tight_layout()
    path = os.path.join(PLOTS_DIR, "preco_medio_genero.png")
    plt.savefig(path, bbox_inches="tight")
    plt.close()
    print(f"  ✅ Salvo: {path}")


def plot_distribuicao_rating(df: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(8, 5))
    contagem = df["rating"].value_counts().sort_index()
    contagem.plot(kind="bar", ax=ax, color="#DD8452", edgecolor="white", alpha=0.85)
    ax.set_title("Distribuição de Avaliações (Rating 1–5)")
    ax.set_xlabel("Rating")
    ax.set_ylabel("Quantidade de Livros")
    ax.set_xticklabels(["1 ⭐", "2 ⭐", "3 ⭐", "4 ⭐", "5 ⭐"], rotation=0)

    plt.tight_layout()
    path = os.path.join(PLOTS_DIR, "distribuicao_rating.png")
    plt.savefig(path, bbox_inches="tight")
    plt.close()
    print(f"  ✅ Salvo: {path}")


def plot_disponibilidade(df: pd.DataFrame):
    contagem = df["disponibilidade"].value_counts()

    fig, ax = plt.subplots(figsize=(6, 6))
    cores = ["#4C72B0", "#DD8452"]
    ax.pie(contagem, labels=contagem.index, autopct="%1.1f%%",
           colors=cores, startangle=90,
           wedgeprops=dict(edgecolor="white", linewidth=2))
    ax.set_title("Disponibilidade dos Livros")

    plt.tight_layout()
    path = os.path.join(PLOTS_DIR, "disponibilidade.png")
    plt.savefig(path, bbox_inches="tight")
    plt.close()
    print(f"  ✅ Salvo: {path}")


def plot_correlacao(df: pd.DataFrame):
    cols_numericas = ["preco", "rating", "estoque", "preco_normalizado"]
    corr = df[cols_numericas].corr()

    fig, ax = plt.subplots(figsize=(7, 5))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm",
                center=0, ax=ax, square=True,
                linewidths=0.5, cbar_kws={"shrink": 0.8})
    ax.set_title("Matriz de Correlação – Variáveis Numéricas")

    plt.tight_layout()
    path = os.path.join(PLOTS_DIR, "correlacao.png")
    plt.savefig(path, bbox_inches="tight")
    plt.close()
    print(f"  ✅ Salvo: {path}")


def plot_estoque_por_disponibilidade(df: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(8, 5))
    df_in = df[df["disponibilidade"] == "In stock"]
    sns.histplot(df_in["estoque"], bins=25, kde=True,
                 color="#55A868", ax=ax, alpha=0.75)
    ax.set_title("Distribuição do Estoque (livros disponíveis)")
    ax.set_xlabel("Quantidade em Estoque")
    ax.set_ylabel("Frequência")

    plt.tight_layout()
    path = os.path.join(PLOTS_DIR, "estoque_distribuicao.png")
    plt.savefig(path, bbox_inches="tight")
    plt.close()
    print(f"  ✅ Salvo: {path}")


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    os.makedirs(PLOTS_DIR, exist_ok=True)

    print("\n" + "="*60)
    print("ANÁLISE EXPLORATÓRIA DE DADOS (EDA)")
    print("="*60)

    df = carregar()

    # Garante tipo correto para rating_cat
    if "rating_cat" in df.columns:
        df["rating_cat"] = pd.Categorical(
            df["rating_cat"],
            categories=["Muito Ruim", "Ruim", "Regular", "Bom", "Excelente"],
            ordered=True,
        )

    secao_panorama_geral(df)
    secao_descritivas(df)

    print("\n📈 Gerando visualizações...")
    plot_distribuicao_precos(df)
    plot_top_generos(df)
    plot_preco_medio_por_genero(df)
    plot_distribuicao_rating(df)
    plot_disponibilidade(df)
    plot_correlacao(df)
    plot_estoque_por_disponibilidade(df)

    print(f"\n✅ Todos os gráficos salvos em: {PLOTS_DIR}")
    print("\n" + "="*60)
    print("ANÁLISE CONCLUÍDA")
    print("="*60)


if __name__ == "__main__":
    main()
