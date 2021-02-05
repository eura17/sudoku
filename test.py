import numpy as np

from sudoku import Sudoku

s = 0

with open('p096_sudoku.txt', 'r') as f:
    sudoku = []
    for line in f:
        if 'Grid' in line:
            if len(sudoku) == 9:
                sudoku = Sudoku(np.array(sudoku, dtype=int))
                sudoku.solve()
                print(sudoku)
                ul3 = sudoku.cells[0, 0].value * 100 + sudoku.cells[0, 1].value * 10 + sudoku.cells[0, 2].value
                s += ul3
            sudoku = []
        else:
            line = list(map(int, list(line.strip())))
            sudoku.append(line)
    sudoku = Sudoku(np.array(sudoku, dtype=int))
    sudoku.solve()
    print(sudoku)
    ul3 = sudoku.cells[0, 0].value * 100 + sudoku.cells[0, 1].value * 10 + \
        sudoku.cells[0, 2].value
    s += ul3

print(s)
