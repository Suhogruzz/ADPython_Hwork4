import itertools


# Итератор возвращающий плоское представление списка списков
class FlatIterator:
    def __init__(self, _list):
        self._list = _list

    def __iter__(self):
        self.list_iter = iter(self._list)
        self.new_list = []
        self.cursor = -1
        return self

    def __next__(self):
        self.cursor += 1
        if len(self.new_list) == self.cursor:
            self.new_list = None
            self.cursor = 0
            while not self.new_list:
                self.new_list = next(self.list_iter)
        return self.new_list[self.cursor]


# Итератор для списков с любым уровнем вложенности
class FlatIteratorAny:
    def __init__(self, _list):
        self._list = _list

    def __iter__(self):
        self.temporary_list = []
        self.iterable = iter(self._list)
        return self

    def __next__(self):
        while True:
            try:
                self.current = next(self.iterable)
            except StopIteration:
                if not self.temporary_list:
                    raise StopIteration
                else:
                    self.iterable = self.temporary_list.pop()
                    continue
            if type(self.current) == list:
                self.temporary_list.append(self.iterable)
                self.iterable = iter(self.current)
            else:
                return self.current


# Итератор с помощью itertools
def flatiterator_itertools(_list):
    flatened_list = list(itertools.chain(*_list))
    print(flatened_list)


if __name__ == '__main__':
    nested_list = [
        ['a', 'b', 'c'],
        ['d', 'e', 'f', 'h', False],
        [1, 2, None],
    ]
    flat_list = [item for item in FlatIterator(nested_list)]
    print(flat_list)

    nested_list_any = [[
        ['a', 'b', 'c'],
        ['d', [['e'], 'f', 'h'], False],
        [1, 2, None],
        [[[['ttt']]]]
    ]]
    flat_list_any = [item for item in FlatIteratorAny(nested_list_any)]
    print(flat_list_any)

    nested_list_itertools = [
        ['a', 'b', 'c'],
        ['d', 'e', 'f', 'h', False],
        [1, 2, None],
    ]
    flatiterator_itertools(nested_list_itertools)