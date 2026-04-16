"""
etl.py - Pipeline ETL: Transformação e Carga
Disciplina: Mineração de Dados - Trabalho Prático Fase 1

Lê o CSV bruto (livros_raw.csv), aplica transformações e gera
o dataset final limpo e estruturado (livros_final.csv).
"""

import pandas as pd
import os
import logging

# ─── Configuração ─────────────────────────────────────────────────────────────
RAW_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "raw", "livros_raw.csv")
PROCESSED_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "processed")
PROCESSED_FILE = os.path.join(PROCESSED_DIR, "livros_final.csv")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
log = logging.getLogger(__name__)


# ─── Funções de Transformação ─────────────────────────────────────────────────

def carregar_dados(caminho: str) -> pd.DataFrame:
    """Carrega o CSV bruto."""
    df = pd.read_csv(caminho, encoding="utf-8")
    log.info(f"[EXTRAÇÃO] {len(df)} registros carregados de '{caminho}'")
    log.info(f"[EXTRAÇÃO] Colunas: {list(df.columns)}")
    return df


def relatorio_inicial(df: pd.DataFrame):
    """Imprime estatísticas do estado bruto."""
    log.info("\n" + "="*50)
    log.info("ESTADO INICIAL DOS DADOS (BRUTOS)")
    log.info("="*50)
    log.info(f"  Registros: {len(df)}")
    log.info(f"  Colunas  : {len(df.columns)}")
    log.info(f"\n  Nulos por coluna:\n{df.isnull().sum().to_string()}")
    log.info(f"\n  Duplicatas exatas: {df.duplicated().sum()}")
    log.info(f"\n  Tipos:\n{df.dtypes.to_string()}")


def tratar_tipos(df: pd.DataFrame) -> pd.DataFrame:
    """Garante os tipos corretos para cada coluna."""
    df["preco"] = pd.to_numeric(df["preco"], errors="coerce")
    df["rating"] = pd.to_numeric(df["rating"], errors="coerce")
    df["estoque"] = pd.to_numeric(df["estoque"], errors="coerce")
    df["genero"] = df["genero"].astype(str).str.strip().str.title()
    df["disponibilidade"] = df["disponibilidade"].astype(str).str.strip()
    df["titulo"] = df["titulo"].astype(str).str.strip()
    log.info("[TRANSFORMAÇÃO] Tipos de dados ajustados.")
    return df


def remover_duplicatas(df: pd.DataFrame) -> pd.DataFrame:
    """Remove linhas duplicadas com base em título + gênero."""
    antes = len(df)
    df = df.drop_duplicates(subset=["titulo", "genero"])
    depois = len(df)
    removidas = antes - depois
    log.info(f"[TRANSFORMAÇÃO] Duplicatas removidas: {removidas} "
             f"(critério: título + gênero)")
    return df


def tratar_nulos(df: pd.DataFrame) -> pd.DataFrame:
    """Trata valores nulos em cada coluna."""
    # Estoque -1 = não conseguiu coletar → trata como nulo
    df["estoque"] = df["estoque"].replace(-1, pd.NA)

    nulos_antes = df.isnull().sum().sum()

    # Preço: preenche com mediana do gênero
    df["preco"] = df.groupby("genero")["preco"].transform(
        lambda x: x.fillna(x.median())
    )

    # Rating: preenche com mediana global
    df["rating"] = df["rating"].fillna(df["rating"].median())

    # Estoque: preenche com 0 onde disponibilidade é "Out of stock",
    #           senão 1 (mínimo assumido)
    df["estoque"] = df.apply(
        lambda row: 0 if row["disponibilidade"] == "Out of stock"
        and pd.isna(row["estoque"])
        else (1 if pd.isna(row["estoque"]) else row["estoque"]),
        axis=1,
    )

    nulos_depois = df.isnull().sum().sum()
    log.info(f"[TRANSFORMAÇÃO] Nulos tratados: {nulos_antes} → {nulos_depois}")
    return df


def tratar_outliers(df: pd.DataFrame) -> pd.DataFrame:
    """Identifica e documenta outliers em variáveis numéricas."""
    for col in ["preco", "estoque"]:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        limite_sup = Q3 + 1.5 * IQR
        limite_inf = Q1 - 1.5 * IQR
        outliers = df[(df[col] < limite_inf) | (df[col] > limite_sup)]
        log.info(
            f"[TRANSFORMAÇÃO] Outliers em '{col}': {len(outliers)} registros "
            f"(IQR: [{limite_inf:.2f}, {limite_sup:.2f}]) — mantidos para análise"
        )
    return df


def converter_rating_categorico(df: pd.DataFrame) -> pd.DataFrame:
    """Cria coluna de rating categórico para enriquecer o dataset."""
    bins = [0, 1, 2, 3, 4, 5]
    labels = ["Muito Ruim", "Ruim", "Regular", "Bom", "Excelente"]
    df["rating_cat"] = pd.cut(
        df["rating"],
        bins=bins,
        labels=labels,
        include_lowest=True,
    )
    log.info("[TRANSFORMAÇÃO] Coluna 'rating_cat' criada (discretização de rating).")
    return df


def normalizar_preco(df: pd.DataFrame) -> pd.DataFrame:
    """Cria coluna de preço normalizado (Min-Max) para uso futuro."""
    preco_min = df["preco"].min()
    preco_max = df["preco"].max()
    df["preco_normalizado"] = (df["preco"] - preco_min) / (preco_max - preco_min)
    log.info("[TRANSFORMAÇÃO] Coluna 'preco_normalizado' criada (Min-Max Scaling).")
    return df


def remover_url(df: pd.DataFrame) -> pd.DataFrame:
    """Remove coluna de URL do dataset final (não relevante para análise)."""
    if "url" in df.columns:
        df = df.drop(columns=["url"])
        log.info("[TRANSFORMAÇÃO] Coluna 'url' removida do dataset final.")
    return df


def salvar_dados(df: pd.DataFrame, caminho: str):
    """Salva o dataset tratado."""
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    df.to_csv(caminho, index=False, encoding="utf-8")
    log.info(f"[CARGA] Dataset final salvo: '{caminho}'")


def relatorio_final(df: pd.DataFrame):
    """Imprime estatísticas do estado final."""
    log.info("\n" + "="*50)
    log.info("ESTADO FINAL DOS DADOS (PROCESSADOS)")
    log.info("="*50)
    log.info(f"  Registros  : {len(df)}")
    log.info(f"  Colunas    : {len(df.columns)} → {list(df.columns)}")
    log.info(f"\n  Nulos por coluna:\n{df.isnull().sum().to_string()}")
    log.info(f"\n  Estatísticas numéricas:\n{df[['preco','rating','estoque']].describe().to_string()}")
    log.info(f"\n  Valores únicos em 'genero': {df['genero'].nunique()}")
    log.info(f"\n  Distribuição de 'disponibilidade':\n{df['disponibilidade'].value_counts().to_string()}")


# ─── Pipeline Principal ───────────────────────────────────────────────────────

def main():
    log.info("=" * 60)
    log.info("INÍCIO DO PIPELINE ETL")
    log.info("=" * 60)

    # 1. Extração
    df = carregar_dados(RAW_FILE)
    relatorio_inicial(df)

    registros_antes = len(df)

    # 2. Transformações
    df = tratar_tipos(df)
    df = remover_duplicatas(df)
    df = tratar_nulos(df)
    df = tratar_outliers(df)
    df = converter_rating_categorico(df)
    df = normalizar_preco(df)
    df = remover_url(df)

    registros_depois = len(df)
    log.info(f"\n[RESUMO] Registros: {registros_antes} → {registros_depois} "
             f"(removidos: {registros_antes - registros_depois})")

    # 3. Carga
    salvar_dados(df, PROCESSED_FILE)
    relatorio_final(df)

    log.info("\n" + "=" * 60)
    log.info("PIPELINE ETL CONCLUÍDO COM SUCESSO")
    log.info("=" * 60)


if __name__ == "__main__":
    main()
