import ast
from collections import defaultdict
from typing import Union, Dict

from const import Operators


class BoolSearcher:
    def __init__(self, example: str, index: dict[str, set[tuple[int]]]):
        self.example = self._replace_elem_to_set(example=example.strip().split(), index=index)
        print(self.example)
        self._in_bracket: bool = False

    def bool_search(self, ) -> set:
        if not self.example:
            return set()

        # result = set()
        while len(self.example) > 1:
            elem_1 = self._handle_elem(self.example.pop(0))
            if self._in_bracket and elem_1 == Operators.CLOSE:
                return self.example.pop(0)

            operand = self._handle_elem(elem=self.example.pop(0))
            if self._in_bracket and operand == Operators.CLOSE:
                return elem_1

            elem_2 = self._handle_elem(elem=self.example.pop(0))

            self.example.insert(0, self._execute_operand(elem_1=elem_1, elem_2=elem_2, operand=operand))

        return self.example.pop(0)

    def _handle_elem(self, elem: Union[set, str]):
        if elem == Operators.OPEN:
            self._in_bracket = True
            elem_2 = self.bool_search()
            return elem_2

        return elem

    @staticmethod
    def _execute_operand(elem_1, elem_2, operand):
        if operand == Operators.AND:
            return elem_1.intersection(elem_2)
        elif operand == Operators.OR:
            return elem_1.union(elem_2)
        elif operand == Operators.NOT:
            return elem_1.difference(elem_2)

    @staticmethod
    def _replace_elem_to_set(
            example: list[Union[str, set]],
            index: dict[str, set[tuple[int]]]
    ) -> list[Union[str, set]]:
        """Заменяем элементы в выражение на их местонахождения в индексе (set)

        A AND B -> {1, 2} AND {1}
        """

        for i in range(len(example)):
            elem = example[i]
            if elem not in Operators.reserved_operators():
                where_elem = index.get(elem, set())
                example[i] = {place_elem[0] for place_elem in where_elem}

        return example


def main():
    result_lemmas: Dict[str, set[tuple[int]]] = defaultdict(set)

    with open('../task3/result/inverted_index_lemmas.txt') as file:
        while line := file.readline():
            lemma, inverted_index = line.split(' - ')
            result_lemmas[lemma] = ast.literal_eval(inverted_index)

    # Пример использования:
    query = "youth OR lucky AND extract"
    searcher = BoolSearcher(example=query, index=result_lemmas)
    print(searcher.bool_search())


if __name__ == '__main__':
    main()