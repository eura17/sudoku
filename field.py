import numpy as np

from cell import Cell


class Field:
    def __init__(self, sqr_size: int = 3):
        self.sqr_size = sqr_size
        self.cells = np.ndarray(shape=(sqr_size ** 2, sqr_size ** 2),
                                dtype=Cell)

    def __repr__(self):
        return f'Field({self.sqr_size})'

    def __str__(self):
        vboard = ' | '
        hboard = f'{"-" * (self.sqr_size * 2)}+' \
                 f'{"-" * (self.sqr_size * 2 + 1)}+' \
                 f'{"-" * (self.sqr_size * 2)}\n'
        field = ''
        for row in range(self.sqr_size ** 2):
            for j in range(self.sqr_size):
                columns = slice(j * self.sqr_size, (j + 1) * self.sqr_size)
                field += ' '.join(map(str, self.cells[row, columns]))
                if (j + 1) != self.sqr_size:
                    field += vboard
            field += '\n'
            if (row + 1) % self.sqr_size == 0 and \
                    (row + 1) != self.sqr_size ** 2:
                field += hboard
        return field


if __name__ == '__main__':
    a = [1, 2, 3]
    print(a)
    np.random.shuffle(a)
    print(a)