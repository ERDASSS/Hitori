from Source.Helpers.solver import Solver

grid = [
    [3, 3, 2, 4, 5],
    [3, 1, 4, 5, 2],
    [5, 2, 4, 3, 4],
    [5, 4, 3, 5, 5],
    [4, 5, 2, 1, 5]
]
grid_solved = [
    ['X', 3, 'X', 4, 'X'],
    [3, 1, 4, 5, 2],
    [5, 2, 'X', 3, 4],
    ['X', 4, 3, 'X', 5],
    [4, 5, 2, 1, 'X']
]

grid_super_easy = [
    [3, 3, 2, 2],
    [2, 4, 1, 3],
    [1, 1, 4, 4],
    [4, 2, 3, 3]
]

grid_extended = [
    [4, 2, 3],
    [1, 4, 2],
    [2, 3, 4],
    [1, 4, 2]
]

grid_solved_1 = [
    [1, 2, 3],
    [2, 3, 1],
    [3, 1, 2]
]

solution = Solver.solve(grid_extended, True)
print(solution)
