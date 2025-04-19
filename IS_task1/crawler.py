import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, unquote
import os
import sys

visited = set()
to_visit = []
max_docs = 100  # Ограничение на количество скачиваемых страниц
min_words = 1000  # Минимальное количество слов на странице
base_output_dir = "pages"
index_file = "index.txt"
doc_count = 0

def clean_text(soup):
    # Убираем все ненужные элементы
    for tag in soup(["script", "style", "header", "footer", "nav", "aside"]):
        tag.decompose()
    return soup.get_text(separator=" ", strip=True)

def save_page(content, url, doc_id):
    global index_file
    filename = os.path.join(base_output_dir, f"{doc_id}.txt")
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)

    with open(index_file, "a", encoding="utf-8") as f:
        f.write(f"{doc_id}\t{url}\n")

def crawl(url):
    global doc_count
    if url in visited or doc_count >= max_docs:
        return
    print(f"Скачиваю: {url}")
    visited.add(url)

    try:
        resp = requests.get(url)
        soup = BeautifulSoup(resp.text, "html.parser")
        text = clean_text(soup)

        if len(text.split()) < min_words:
            return

        doc_count += 1
        save_page(text, url, doc_count)

        # Добавляем новые ссылки
        for link in soup.find_all("a", href=True):
            href = link['href']
            full_url = urljoin(url, href)
            parsed = urlparse(full_url)

            if parsed.scheme.startswith("http") and "ru.wikipedia.org" in parsed.netloc:
                decoded_url = unquote(full_url)

                # исключаем повторяющиеся статьи на одну тему
                if "Искусственный_интеллект" not in decoded_url:
                    to_visit.append(decoded_url)

    except Exception as e:
        print(f"Ошибка при обработке {url}: {e}")

def main(start_urls):
    global to_visit
    os.makedirs(base_output_dir, exist_ok=True)

    # Чистим старые данные
    if os.path.exists(index_file):
        os.remove(index_file)

    to_visit.extend(start_urls)

    while to_visit and doc_count < max_docs:
        url = to_visit.pop(0)
        crawl(url)

    print(f"Готово! Скачано {doc_count} страниц.")

if __name__ == "__main__":
    start_urls = [
        'https://ru.wikipedia.org/wiki/Искусственный_интеллект',
    ]
    main(start_urls)

