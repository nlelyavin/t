import re
from collections import defaultdict
from os import listdir
from typing import List, Set, Dict

import nltk
from bs4 import BeautifulSoup
from nltk import WordNetLemmatizer
from nltk.corpus import wordnet


def extract_tokens(html) -> Set[str]:
    soup = BeautifulSoup(html, 'html.parser')
    # Извлекаем текст без HTML тегов
    text = soup.get_text()
    # Берём только кириллицу и слова длины > 2
    tokens = set(re.findall(r'\b(?:[A-Z][a-z]+|[a-z]{3,})\b', text))

    return tokens


def grouping_by_lemmas(tokens: set[str]) -> Dict[str, List[str]]:
    # Создание лемматизатора
    lemmatizer = WordNetLemmatizer()

    lemma_tokens = defaultdict(list)

    # Лемматизация токенов
    for token in tokens:
        tag = nltk.pos_tag([token])[0][1][0].upper()
        tag_dict = {"J": wordnet.ADJ, "N": wordnet.NOUN, "V": wordnet.VERB, "R": wordnet.ADV}
        wordnet_tag = tag_dict.get(tag, wordnet.NOUN)

        lemmatized_token = lemmatizer.lemmatize(token, wordnet_tag)
        lemma_tokens[lemmatized_token].append(token)

    return dict(lemma_tokens)


def main():
    nltk.download('wordnet')
    nltk.download('punkt')
    nltk.download('averaged_perceptron_tagger')
    files = sorted(listdir('../task1/result'), key=lambda x: int(x.split('_')[0]))

    tokens = set()
    for i, file in enumerate(files):
        with open(f'../task1/result/{file}', mode='r', encoding="utf-8") as f:
            new_tokens = extract_tokens(f.read())
            tokens = tokens.union(new_tokens)

    tokens = {token.lower() for token in tokens}
    lemma_tokens = grouping_by_lemmas(tokens)

    with open('result/tokens.txt', mode='a', encoding="utf-8") as f:
        for token in tokens:
            f.write(f'{token}\n')

    with open('result/lemmatized_tokens.txt', mode='a', encoding="utf-8") as f:
        for key, values in lemma_tokens.items():
            f.write(f'{key} {" ".join(values)}\n')


if __name__ == '__main__':
    main()
