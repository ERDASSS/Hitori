from Source.Helpers.generator import Generator
from Source.Helpers.solver import Solver, SolverTriangle


grid = [['X'], [1, 3], [5, 2, 4], [2, 'X', 3, 1], [4, 1, 2, 5, 'X']]
# print(Generator.generate_triangle_grid(5))
print(SolverTriangle.grid_is_valid(grid))


