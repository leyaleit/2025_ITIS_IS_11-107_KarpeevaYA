import os
import nltk
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# Загружаем необходимые пакеты NLTK
nltk.download('stopwords')
nltk.download('punkt')
stop_words = set(stopwords.words('russian'))

# Шаг 1: Создание инвертированного индекса
def build_inverted_index(input_dir):
    inverted_index = {}

    for filename in os.listdir(input_dir):
        if filename.endswith('.txt'):
            with open(os.path.join(input_dir, filename), 'r', encoding='utf-8') as file:
                text = file.read()

            tokens = [token.lower() for token in word_tokenize(text) if token.isalpha() and token not in stop_words]

            for token in set(tokens):
                if token not in inverted_index:
                    inverted_index[token] = []
                inverted_index[token].append(filename)

    sorted_index = {k: sorted(v) for k, v in sorted(inverted_index.items())}

    with open('inverted_index.txt', 'w', encoding='utf-8') as f:
        for term, docs in sorted_index.items():
            f.write(f"{term}: {', '.join(docs)}\n")

    print("Инвертированный индекс сохранён в файл inverted_index.txt")
    return sorted_index

# Шаг 2: Реализация булевого поиска
def boolean_search(query, inverted_index):
    query = query.lower()
    query = re.sub(r'\bне\b', '!', query)
    query = re.sub(r'\bи\b', ' & ', query)
    query = re.sub(r'\bили\b', ' | ', query)

    tokens = query.split()
    if not tokens:
        return set()

    def get_docs(term):
        if term.startswith('!'):
            word = term[1:]
            all_docs = set()
            for doc_list in inverted_index.values():
                all_docs.update(doc_list)
            return all_docs - set(inverted_index.get(word, []))
        else:
            return set(inverted_index.get(term, []))

    try:
        result = get_docs(tokens[0])
        i = 1
        while i < len(tokens):
            operator = tokens[i]
            next_docs = get_docs(tokens[i + 1])
            if operator == '&':
                result = result & next_docs
            elif operator == '|':
                result = result | next_docs
            i += 2
        return result
    except Exception as e:
        print("Ошибка: Неверный формат булевого запроса.")
        return set()


# Основной блок
if __name__ == "__main__":
    input_dir = 'C:/Users/Yulia/Documents/Projects/IS_task1/pages'
    inverted_index = build_inverted_index(input_dir)

    while True:
        query = input("\nВведите булев запрос (например, word1 И word2 ИЛИ word3), или 'выход' для завершения: ")
        if query.strip().lower() == 'выход':
            print("Завершение программы.")
            break
        results = boolean_search(query, inverted_index)
        if results:
            print(f"Документы, удовлетворяющие запросу '{query}': {results}")
        else:
            print(f"Ни один документ не соответствует запросу '{query}'.")

