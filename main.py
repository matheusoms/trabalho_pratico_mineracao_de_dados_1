"""
main.py - Executa o pipeline completo: Scraping → ETL → Análise
Disciplina: Mineração de Dados - Trabalho Prático Fase 1

Uso:
    python main.py                 # Roda tudo do zero
    python main.py --skip-scraping # Pula o scraping (usa CSV já existente)
"""

import sys
import os

# Adiciona src/ ao path
SRC_DIR = os.path.join(os.path.dirname(__file__), "src")
sys.path.insert(0, SRC_DIR)

RAW_FILE = os.path.join(os.path.dirname(__file__), "data", "raw", "livros_raw.csv")


def main():
    skip_scraping = "--skip-scraping" in sys.argv

    print("\n" + "█" * 60)
    print("  MINERAÇÃO DE DADOS — FASE 1")
    print("  Coleta, ETL e Análise Exploratória — books.toscrape.com")
    print("█" * 60)

    # ── ETAPA 1: Scraping ─────────────────────────────────────────────────────
    if skip_scraping:
        print("\n⏭️  Scraping ignorado (--skip-scraping). Usando CSV existente.")
    else:
        if os.path.exists(RAW_FILE):
            resposta = input(
                f"\n⚠️  '{RAW_FILE}' já existe. Refazer o scraping? [s/N]: "
            ).strip().lower()
            if resposta != "s":
                print("   Usando dados existentes.")
                skip_scraping = True

        if not skip_scraping:
            print("\n🌐 ETAPA 1 — WEB SCRAPING")
            from scraper import main as scraping_main
            scraping_main()

    # ── ETAPA 2: ETL ──────────────────────────────────────────────────────────
    print("\n🔄 ETAPA 2 — PIPELINE ETL")
    from etl import main as etl_main
    etl_main()

    # ── ETAPA 3: Análise ──────────────────────────────────────────────────────
    print("\n📊 ETAPA 3 — ANÁLISE EXPLORATÓRIA")
    from analise import main as analise_main
    analise_main()

    print("\n" + "█" * 60)
    print("  ✅ PIPELINE COMPLETO EXECUTADO COM SUCESSO")
    print(f"  › Dados brutos : data/raw/livros_raw.csv")
    print(f"  › Dados finais : data/processed/livros_final.csv")
    print(f"  › Gráficos     : data/plots/")
    print("█" * 60 + "\n")


if __name__ == "__main__":
    main()
