import ast
import math
from collections import defaultdict

DOC_NUMBERS = 100


def parse_inverted_index(filename: str) -> dict[str, set[tuple]]:
    inverted_index = {}

    with open(filename, mode='r', encoding="utf-8") as file:
        while line := file.readline():
            lemma, file_numbers = line.split(' - ')
            files_entry = ast.literal_eval(file_numbers)
            files_entry_dct = defaultdict(int)
            for file_entry in files_entry:
                files_entry_dct[file_entry[0]] += file_entry[1]

            files_entry = {tuple([file_entry, files_entry_dct[file_entry]]) for file_entry in files_entry_dct}

            inverted_index[lemma] = files_entry

    return inverted_index


def calculate_tf_idf(entry_number: int, all_token_entry: int) -> (float, float):
    """

    :param entry_number: Сколько раз токен повторяется в файле поделенный на кол-во слов в документе
    :param all_token_entry: Общее кол-во файлов, где был токен
    :return:
    """
    idf = round(math.log10(DOC_NUMBERS / all_token_entry), 6)
    return idf, round(idf * entry_number, 6)


def get_tf_idf(inverted_index: dict[str, set[tuple]]) -> dict[str, list[tuple[int, float, float]]]:
    """"""

    tf_idf: dict[str, list[tuple[int, float, float]]] = defaultdict(list)

    for token, files_entry in inverted_index.items():
        for file_entry in files_entry:
            token_idf, token_tf_idf = calculate_tf_idf(entry_number=file_entry[1], all_token_entry=len(files_entry))
            tf_idf[token].append((file_entry[0], token_idf, token_tf_idf))

    return tf_idf


def save_to_file(filename, tf_idf_result):
    with open(filename, 'a', encoding='utf-8') as file:
        for token, tf_idf_by_doc in tf_idf_result.items():
            line = token
            for tf_idf in tf_idf_by_doc:
                line += f' file_{tf_idf[0]} {tf_idf[1]} {tf_idf[2]}'
            line += '\n'
            file.write(line)


def main():
    inverted_index_lemmas = parse_inverted_index('../task3/result/inverted_index_lemmas.txt')
    inverted_index_tokens = parse_inverted_index('../task3/result/inverted_index_tokens.txt')

    tf_idf_tokens = get_tf_idf(inverted_index_tokens)
    tf_idf_lemmas = get_tf_idf(inverted_index_lemmas)

    save_to_file(filename='result/tdf_idf_tokens.txt', tf_idf_result=tf_idf_tokens)
    save_to_file(filename='result/tdf_idf_lemmas.txt', tf_idf_result=tf_idf_lemmas)


if __name__ == '__main__':
    main()
