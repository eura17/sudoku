from collections import Counter
from itertools import combinations
from functools import reduce

import numpy as np

from field import Field
from cell import Cell


class Sudoku(Field):
    def __init__(self, field: np.array):
        sqr_size = int(np.sqrt(len(field)))
        super().__init__(sqr_size)
        for i in range(self.cells.shape[0]):
            for j in range(self.cells.shape[1]):
                self.cells[i, j] = Cell(field[i, j], sqr_size)
        self.__backups = []

    __is_filled = staticmethod(np.vectorize(lambda x: x.value != 0))

    def __count_filled(self):
        return np.sum(self.__is_filled(self.cells))

    def __is_solved(self):
        return self.__count_filled() == self.sqr_size ** 4 and \
               self.__is_correct()

    @staticmethod
    def __is_item_correct(item):
        is_correct = True
        values = Counter()
        for cell in item:
            is_correct *= cell.is_correct()
            values[cell.value] += 1
        values[0] = 1
        return bool(is_correct) and values.most_common()[0][1] == 1

    def __is_correct(self):
        is_correct = True
        for row in self.cells:
            is_correct *= self.__is_item_correct(row)
        for column in self.cells.T:
            is_correct *= self.__is_item_correct(column)
        for i in range(self.sqr_size):
            for j in range(self.sqr_size):
                rows = slice(i * self.sqr_size, (i + 1) * self.sqr_size)
                columns = slice(j * self.sqr_size, (j + 1) * self.sqr_size)
                sqr = self.cells[rows, columns]
                is_correct *= self.__is_item_correct(sqr.flatten())
        return bool(is_correct)

    __get_values = staticmethod(np.vectorize(lambda x: x.value))

    def __backup(self):
        self.__backups.append(self.__get_values(self.cells))

    def __restore(self):
        backup = self.__backups[0]
        for i in range(self.cells.shape[0]):
            for j in range(self.cells.shape[1]):
                self.cells[i, j] = Cell(backup[i, j], self.sqr_size)
        self.__backups = []

    @staticmethod
    def __exclude_straightforwardly(item):
        unique = set([cell.value for cell in item])
        for cell in item:
            cell.del_possible_value(unique)

    def straightforward_solver(self):
        for row in self.cells:
            self.__exclude_straightforwardly(row)
        for column in self.cells.T:
            self.__exclude_straightforwardly(column)
        for i in range(self.sqr_size):
            for j in range(self.sqr_size):
                rows = slice(i * self.sqr_size, (i + 1) * self.sqr_size)
                columns = slice(j * self.sqr_size, (j + 1) * self.sqr_size)
                sqr = self.cells[rows, columns]
                self.__exclude_straightforwardly(sqr.flatten())

    @staticmethod
    def __exclude_indirectly(item):
        def filter_blank_cells(cells):
            return np.array(list(filter(lambda x: x.value == 0, cells)))

        blank_cells = filter_blank_cells(item)
        for n in range(2, blank_cells.shape[0]):
            for comb in combinations(blank_cells, n):
                comb = filter_blank_cells(comb)
                comb_pv = reduce(lambda pv, x: pv | x.possible_values,
                                 comb, set())
                if len(comb) == len(comb_pv):
                    for cell in blank_cells:
                        if cell not in comb:
                            cell.del_possible_value(comb_pv)

    def indirect_solver(self):
        for row in self.cells:
            self.__exclude_indirectly(row)
        for column in self.cells.T:
            self.__exclude_indirectly(column)
        for i in range(self.sqr_size):
            for j in range(self.sqr_size):
                rows = slice(i * self.sqr_size, (i + 1) * self.sqr_size)
                columns = slice(j * self.sqr_size, (j + 1) * self.sqr_size)
                sqr = self.cells[rows, columns]
                self.__exclude_indirectly(sqr.flatten())

    def __guess(self):
        blank_items = []
        for row in self.cells:
            if not np.all(self.__is_filled(row)):
                blank_items.append(row)
        for column in self.cells.T:
            if not np.all(self.__is_filled(column)):
                blank_items.append(column)
        for i in range(self.sqr_size):
            for j in range(self.sqr_size):
                rows = slice(i * self.sqr_size, (i + 1) * self.sqr_size)
                columns = slice(j * self.sqr_size, (j + 1) * self.sqr_size)
                sqr = self.cells[rows, columns].flatten()
                if not np.all(self.__is_filled(sqr)):
                    blank_items.append(sqr)
        blank_items.sort(key=lambda x: np.sum(self.__is_filled(x)))
        item = blank_items[-1]
        possible = set(np.arange(1, self.sqr_size**2+1))
        unfilled = set(self.__get_values(item))
        to_fill = list(possible - unfilled)
        np.random.shuffle(to_fill)
        for cell in item:
            if cell.value == 0:
                cell.del_possible_value(possible - {to_fill.pop()})

    def guess_and_test(self):
        self.__backup()
        self.__guess()

    def solve(self):
        while not self.__is_solved():
            if not self.__is_correct():
                try:
                    self.__restore()
                except IndexError:
                    return False
            filled = self.__count_filled()
            self.straightforward_solver()
            if filled == self.__count_filled():
                self.indirect_solver()
                if filled == self.__count_filled():
                    self.guess_and_test()


if __name__ == '__main__':
    sudoku = np.array(
        [[7, 0, 8, 0, 0, 0, 3, 0, 0],
         [0, 0, 0, 2, 0, 1, 0, 0, 0],
         [5, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 4, 0, 0, 0, 0, 0, 2, 6],
         [3, 0, 0, 0, 8, 0, 0, 0, 0],
         [0, 0, 0, 1, 0, 0, 0, 9, 0],
         [0, 9, 0, 6, 0, 0, 0, 0, 4],
         [0, 0, 0, 0, 7, 0, 5, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0]]
    )
    s = Sudoku(sudoku)
    s.solve()
    print(s)
