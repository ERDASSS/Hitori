from Source.Helpers.generator import Generator
from Source.Helpers.solver import Solver, SolverTriangle


grid = [[4], [3, 3], [2, 1, 3]]
# print(Generator.generate_triangle_grid(4))
print(SolverTriangle.solve(grid))
