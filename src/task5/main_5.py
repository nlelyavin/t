import re
from collections import defaultdict

import pandas as pd
from bs4 import BeautifulSoup

from sklearn.feature_extraction.text import TfidfVectorizer


def extract_text(html) -> str:
    soup = BeautifulSoup(html, 'html.parser')
    # Извлекаем текст без HTML тегов
    text = soup.get_text()
    # Берём только кириллицу и слова длины > 2
    tokens = " ".join(re.findall(r'\b(?:[A-Z][a-z]+|[a-z]{3,})\b', text))

    return tokens


def main():
    data = defaultdict(list)
    with open('../task1/files/index.txt', 'r', encoding='utf-8') as file_with_indexes:
        i = 0
        while (line := file_with_indexes.readline()) and i < 100:
            i += 1
            file_index, file_link = line.split(', ')
            with open(f'../task1/result/{file_index}_file.html', 'r', encoding='utf-8') as file_html:
                text = extract_text(file_html)
            data['link'].append(file_link.replace('\n', ''))
            data['text'].append(text)
            print(line)

    df = pd.DataFrame(data=data)

    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(df['text'])
    return df, X, vectorizer


if __name__ == '__main__':
    main()
