import os
import nltk
import math
import pandas as pd
from collections import Counter
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# Загружаем необходимые пакеты NLTK
nltk.download('stopwords')
nltk.download('punkt')

stop_words = set(stopwords.words('russian'))

# Шаг 1: Сбор лемматизированных данных
def get_documents(input_dir):
    documents = []
    filenames = []
    
    for filename in os.listdir(input_dir):
        if filename.endswith('.txt'):
            with open(os.path.join(input_dir, filename), 'r', encoding='utf-8') as file:
                text = file.read()

            tokens = [token.lower() for token in word_tokenize(text) if token.isalpha() and token not in stop_words]
            documents.append(tokens)
            filenames.append(filename)

    return documents, filenames

# Шаг 2: Подсчёт TF
def compute_tf(documents):
    tf_list = []
    for doc in documents:
        tf_doc = Counter(doc)
        doc_len = len(doc)
        tf_list.append({word: count / doc_len for word, count in tf_doc.items()})
    return tf_list

# Шаг 3: Подсчёт IDF
def compute_idf(documents):
    N = len(documents)
    idf_dict = {}
    all_terms = set(term for doc in documents for term in doc)
    for term in all_terms:
        term_in_docs = sum(1 for doc in documents if term in doc)
        idf_dict[term] = math.log(N / (1 + term_in_docs))
    return idf_dict

# Шаг 4: Подсчёт TF-IDF
def compute_tfidf(tf_list, idf_dict):
    tfidf_list = []
    for tf_doc in tf_list:
        tfidf_doc = {term: tf * idf_dict.get(term, 0) for term, tf in tf_doc.items()}
        tfidf_list.append(tfidf_doc)
    return tfidf_list

# Шаг 5: Сохранение результатов в CSV
def save_to_csv(tf_list, idf_dict, tfidf_list, filenames):
    # Создаём таблицу для TF
    tf_df = pd.DataFrame(tf_list).fillna(0)
    tf_df['Document'] = filenames
    tf_df.to_csv('tf_table.csv', index=False, float_format='%.5f')

    # Создаём таблицу для IDF
    idf_df = pd.DataFrame(list(idf_dict.items()), columns=['Term', 'IDF'])
    idf_df.to_csv('idf_table.csv', index=False, float_format='%.5f')

    # Создаём таблицу для TF-IDF
    tfidf_df = pd.DataFrame(tfidf_list).fillna(0)
    tfidf_df['Document'] = filenames
    tfidf_df.to_csv('tfidf_table.csv', index=False, float_format='%.5f')

    print("Результаты сохранены в файлы: tf_table.csv, idf_table.csv, tfidf_table.csv")

# Основной блок
if __name__ == "__main__":
    input_dir = 'C:/Users/Yulia/Documents/Projects/IS_task2/lemmatized'  # Путь к вашим данным

    # Сбор документов
    documents, filenames = get_documents(input_dir)
    
    # Подсчёт TF
    print("Подсчёт TF...")
    tf_list = compute_tf(documents)
    
    # Подсчёт IDF
    print("Подсчёт IDF...")
    idf_dict = compute_idf(documents)
    
    # Подсчёт TF-IDF
    print("Подсчёт TF-IDF...")
    tfidf_list = compute_tfidf(tf_list, idf_dict)
    
    # Сохранение результатов в файлы CSV
    print("Сохранение результатов...")
    save_to_csv(tf_list, idf_dict, tfidf_list, filenames)




