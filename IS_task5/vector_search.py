import pandas as pd
import numpy as np
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from sklearn.metrics.pairwise import cosine_similarity

# Загрузка необходимых ресурсов
nltk.download('punkt')
nltk.download('stopwords')

# Загрузка таблицы TF-IDF
tfidf_df = pd.read_csv('C:/Users/Yulia/Documents/Projects/IS_task4/tfidf_table.csv')
stop_words = set(stopwords.words('russian'))

# Отделяем имена документов от векторов
doc_names = tfidf_df['Document']
tfidf_df = tfidf_df.drop(columns=['Document'])

# Функция обработки поискового запроса
def preprocess_query(query):
    tokens = word_tokenize(query.lower())
    tokens = [word for word in tokens if word.isalpha() and word not in stop_words]
    return tokens

# Построение вектора запроса
def build_query_vector(query_tokens, tfidf_columns):
    vector = np.zeros(len(tfidf_columns))
    term_counts = {term: query_tokens.count(term) for term in query_tokens}
    for i, term in enumerate(tfidf_columns):
        tf = term_counts.get(term, 0)
        vector[i] = tf
    return vector

# Основной поиск
def search(query, tfidf_df, doc_names):
    tokens = preprocess_query(query)
    if not tokens:
        print("Запрос не содержит значимых слов.")
        return

    query_vector = build_query_vector(tokens, tfidf_df.columns)
    doc_matrix = tfidf_df.to_numpy()

    # Нормализация
    query_vector = query_vector.reshape(1, -1)
    similarities = cosine_similarity(doc_matrix, query_vector).flatten()

    # Вывод результатов
    results = list(zip(doc_names, similarities))
    results.sort(key=lambda x: x[1], reverse=True)

    print("\nРезультаты поиска:")
    for doc, score in results:
        if score > 0:
            print(f"{doc}: релевантность = {score:.5f}")
        else:
            break

# --- Запуск ---
if __name__ == "__main__":
    while True:
        query = input("\nВведите поисковый запрос (или 'выход' для завершения): ")
        if query.lower() in ['выход', 'exit', 'quit']:
            break
        search(query, tfidf_df, doc_names)


