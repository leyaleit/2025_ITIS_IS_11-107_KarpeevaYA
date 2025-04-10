import os
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import pymorphy2

# Загружаем необходимые ресурсы
nltk.download('punkt')
nltk.download('stopwords')

# Загружаем стоп-слова
stop_words = set(stopwords.words('russian'))

# Морфологический анализатор
morph = pymorphy2.MorphAnalyzer()

def process_text(text):
    """Обработка текста: токенизация, лемматизация, удаление стоп-слов и пунктуации."""
    words = word_tokenize(text, language="russian")
    lemmas = []
    for word in words:
        word = word.lower()
        if word.isalpha() and word not in stop_words:
            lemma = morph.parse(word)[0].normal_form
            lemmas.append(lemma)
    return ' '.join(lemmas)

def process_files(input_dir='C:/Users/Yulia/Documents/Projects/IS_task1/pages',
                  output_dir='C:/Users/Yulia/Documents/Projects/IS_task2/lemmatized'):
    """Обработка всех текстовых файлов в указанной папке."""
    os.makedirs(output_dir, exist_ok=True)

    for filename in os.listdir(input_dir):
        if filename.endswith('.txt'):
            with open(os.path.join(input_dir, filename), 'r', encoding='utf-8') as file:
                text = file.read()
            processed_text = process_text(text)
            with open(os.path.join(output_dir, filename), 'w', encoding='utf-8') as output_file:
                output_file.write(processed_text)

if __name__ == "__main__":
    process_files()

