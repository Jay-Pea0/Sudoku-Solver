from z3 import *
from itertools import combinations


def exactly_one(literals):
    c = []
    for pair in combinations(literals, 2):
        a, b = pair[0],pair[1]
        c +=[Or(Not(a), Not(b))]
    c += [Or(literals)]
    return And(c)


def solve(grid):
    lits = []
    for i in range(9):
        lits +=[[]]
        for j in range(9):
            lits[i] += [[]]
            for digit in range(9):
                lits[i][j] += [Bool("x_%i_%i_%i" % (i, j, digit))]


    s = Solver()

    for i in range(9):
        for j in range(9):
            s.add(exactly_one(lits[i][j]))

    for i in range(9):
        for x in range(9):
            row = []
            for j in range(9):
                row += [lits[i][j][x]]
            s.add(exactly_one(row))

    for j in range(9):
        for x in range(9):
            s.add(exactly_one([lits[i][j][x] for i in range(9)]))

    for i in range(3):
        for j in range(3):
            for k in range(9):
                grid_cells = []
                for x in range(3):
                    for y in range(3):
                        grid_cells +=[lits[3 * i + x][3 * j + y][k]]
                s.add(exactly_one(grid_cells))

    for i in range(9):
        for j in range(9):
            if grid[i][j] > 0:
                s.add(lits[i][j][grid[i][j] - 1])

    if str(s.check()) == 'sat':
        print_solution(s.model(), lits)
    else:
        print("unsat")


def print_solution(model, lits):
    lines = []
    for i in range(9):
        lines += [[]]
        for j in range(9):
            digit = 0
            for x in range(9):
                if model.evaluate(lits[i][j][x]):
                    digit = x + 1
            lines[i] += [digit]

    for line in lines:
        print(" ".join([str(x) for x in line]))



if __name__ == '__main__':
    filename = sys.argv[1]
    grid = []
    with open(filename, 'r') as input_f:
        for line in input_f.readlines():
            grid.append([int(x) for x in line.split(" ")])

        solve(grid)

    
                
