import asyncio
import concurrent.futures
import re
import time
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from os import listdir
from pprint import pprint
from typing import List, Dict, Set

from bs4 import BeautifulSoup

from bool_search import BoolSearcher


def extract_tokens(html):
    soup = BeautifulSoup(html, 'html.parser')
    # Извлекаем текст без HTML тегов
    text = soup.get_text()
    # Берём только кириллицу и слова длины > 2
    tokens = re.findall(r'\b(?:[A-Z][a-z]+|[a-z]{3,})\b', text)
    unique_tokens = set(tokens)

    return tokens, unique_tokens


def check_file(
        file: str,
        lem_tokens: Dict[str, List[str]],
        file_number: int,
        result_lemmas: dict[str, set[tuple[int]]],
        result_tokens: dict[str, set[tuple[int]]],
):
    file_tokens = extract_tokens(file)
    tokens: list[str] = file_tokens[0]
    unique_tokens: set[str] = file_tokens[1]

    for key, values in lem_tokens.items():
        tokens_in_file = set(values).intersection(unique_tokens)
        for token in tokens_in_file:
            # Сколько раз слово встречается в файле
            percentage_word_in_file = round(tokens.count(token) / len(tokens), 6)
            amount_word_in_file = (file_number, percentage_word_in_file)
            result_lemmas[key].add(amount_word_in_file)
            result_tokens[token].add(amount_word_in_file)


async def main():
    lem_tokens: Dict[str, List[str]] = defaultdict(list)

    with open('../task2/result/lemmatized_tokens.txt', mode='r', encoding="utf-8") as f:
        line = f.readline()
        while line:
            key, values = line.split(' ', 1)
            values = values.replace('\n', '').split(' ')
            lem_tokens[key] += values
            line = f.readline()

    files = sorted(listdir('../task1/result'), key=lambda x: int(x.split('_')[0]))
    d_files = {}
    for i, file in enumerate(files):
        with open(f'../task1/result/{file}', mode='r', encoding="utf-8") as f:
            file = f.read()
            d_files[i] = file

    result_lemmas: Dict[str, set[tuple[int]]] = defaultdict(set)
    result_tokens: Dict[str, set[tuple[int]]] = defaultdict(set)

    for i in d_files:
        print(i)
        check_file(d_files[i], lem_tokens, i, result_lemmas=result_lemmas, result_tokens=result_tokens)

    with open('result/inverted_index_lemmas.txt', 'a', encoding='utf-8') as file:
        for lemma in result_lemmas:
            line = f'{lemma} - {result_lemmas[lemma]}\n'
            file.write(line)

    with open('result/inverted_index_tokens.txt', 'a', encoding='utf-8') as file:
        for token in result_tokens:
            line = f'{token} - {result_tokens[token]}\n'
            file.write(line)

    # Пример использования:
    query = "посетителей OR редактировать"
    searcher = BoolSearcher(example=query, index=result_lemmas)
    print(searcher.bool_search())


if __name__ == '__main__':
    asyncio.run(main())
