from Source.Helpers.generator import Generator
from Source.Helpers.solver import Solver, SolverTriangle


grid = [[2], [1, 'X'], ['X', 1, 3]]
# print(Generator.generate_triangle_grid(5))
print(SolverTriangle.grid_is_valid(grid))


