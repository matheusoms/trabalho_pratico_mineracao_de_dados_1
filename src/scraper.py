"""
scraper.py - Web Scraping de Livros (books.toscrape.com)
Disciplina: Mineração de Dados - Trabalho Prático Fase 1
Site-alvo: http://books.toscrape.com (site de prática, sem restrições éticas)
"""

import requests
from bs4 import BeautifulSoup
import csv
import time
import os
import logging

# ─── Configuração ────────────────────────────────────────────────────────────
BASE_URL = "http://books.toscrape.com/catalogue/"
START_URL = "http://books.toscrape.com/catalogue/page-1.html"
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "raw")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "livros_raw.csv")

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}

# Mapeamento de rating por extenso → numérico
RATING_MAP = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5,
}

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
log = logging.getLogger(__name__)


# ─── Funções Auxiliares ───────────────────────────────────────────────────────

def get_soup(url: str) -> BeautifulSoup | None:
    """Faz a requisição HTTP e retorna um objeto BeautifulSoup."""
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        return BeautifulSoup(response.text, "lxml")
    except requests.RequestException as e:
        log.error(f"Erro ao acessar {url}: {e}")
        return None


def get_genero_from_url(url: str) -> str:
    """Extrai o gênero a partir da URL da categoria."""
    # URL de categoria: .../catalogue/category/books/mystery_3/...
    parts = url.split("/")
    for part in parts:
        if part and part not in ("catalogue", "category", "books", ""):
            # Remove o sufixo numérico: "mystery_3" → "mystery"
            genero = "_".join(part.split("_")[:-1]) if "_" in part else part
            return genero.replace("-", " ").title()
    return "Desconhecido"


def parse_livro(article, genero: str, url_livro: str) -> dict:
    """Extrai os campos de um elemento <article class='product_pod'>."""
    titulo = article.h3.a["title"]

    preco_raw = article.find("p", class_="price_color").text.strip()
    preco = float(preco_raw.replace("£", "").replace("Â", "").strip())

    rating_class = article.find("p", class_="star-rating")["class"][1]
    rating = RATING_MAP.get(rating_class, 0)

    disponibilidade_raw = article.find("p", class_="instock availability")
    disponibilidade = disponibilidade_raw.text.strip() if disponibilidade_raw else "Unknown"
    disponibilidade_bool = "In stock" if "In stock" in disponibilidade else "Out of stock"

    return {
        "titulo": titulo,
        "preco": preco,
        "rating": rating,
        "genero": genero,
        "disponibilidade": disponibilidade_bool,
        "url": url_livro,
    }


def get_estoque(url_livro: str) -> int:
    """Acessa a página individual do livro para obter a quantidade em estoque."""
    soup = get_soup(BASE_URL + url_livro)
    if soup is None:
        return -1
    table = soup.find("table", class_="table-striped")
    if table:
        rows = table.find_all("tr")
        for row in rows:
            th = row.find("th")
            td = row.find("td")
            if th and td and "availability" in th.text.lower():
                texto = td.text.strip()
                # Extrai número: "In stock (22 available)" → 22
                numeros = [s for s in texto.split() if s.isdigit()]
                return int(numeros[0]) if numeros else (1 if "In stock" in texto else 0)
    return -1


# ─── Coleta por Categoria ─────────────────────────────────────────────────────

def get_categorias() -> list[tuple[str, str]]:
    """Retorna lista de (nome_genero, url_categoria)."""
    soup = get_soup("http://books.toscrape.com/")
    if soup is None:
        return []
    sidebar = soup.find("ul", class_="nav-list")
    categorias = []
    for li in sidebar.find_all("li")[1:]:  # Ignora "Books" (geral)
        a = li.find("a")
        nome = a.text.strip()
        url = "http://books.toscrape.com/" + a["href"]
        categorias.append((nome, url))
    return categorias


def scrape_categoria(nome_genero: str, url_categoria: str, registros: list, max_por_categoria: int = 25):
    """Raspa todos os livros de uma categoria (paginação incluída)."""
    url_atual = url_categoria
    coletados = 0

    while url_atual and coletados < max_por_categoria:
        soup = get_soup(url_atual)
        if soup is None:
            break

        articles = soup.find_all("article", class_="product_pod")
        for article in articles:
            if coletados >= max_por_categoria:
                break

            url_relativa = article.h3.a["href"].replace("../", "")
            livro = parse_livro(article, nome_genero, url_relativa)

            # Busca estoque na página individual (com delay)
            time.sleep(0.2)
            livro["estoque"] = get_estoque(url_relativa)

            registros.append(livro)
            coletados += 1

        # Paginação
        next_btn = soup.find("li", class_="next")
        if next_btn:
            next_href = next_btn.find("a")["href"]
            # Constrói URL da próxima página
            base_cat = url_atual.rsplit("/", 1)[0] + "/"
            url_atual = base_cat + next_href
        else:
            break

        time.sleep(0.3)  # Delay respeitoso entre páginas

    log.info(f"  └─ {nome_genero}: {coletados} livros coletados")


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    log.info("=" * 60)
    log.info("INÍCIO DA COLETA - books.toscrape.com")
    log.info("=" * 60)

    categorias = get_categorias()
    log.info(f"Categorias encontradas: {len(categorias)}")

    registros = []

    for nome_genero, url_cat in categorias:
        log.info(f"Coletando categoria: {nome_genero}")
        scrape_categoria(nome_genero, url_cat, registros, max_por_categoria=25)

        if len(registros) >= 1100:
            log.info("Limite de 1100 registros atingido. Encerrando coleta.")
            break

    log.info(f"\nTotal coletado: {len(registros)} livros")

    # Salva CSV bruto
    campos = ["titulo", "preco", "rating", "genero", "disponibilidade", "estoque", "url"]
    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=campos)
        writer.writeheader()
        writer.writerows(registros)

    log.info(f"Dados brutos salvos em: {OUTPUT_FILE}")
    log.info("=" * 60)
    log.info("COLETA CONCLUÍDA")
    log.info("=" * 60)


if __name__ == "__main__":
    main()
