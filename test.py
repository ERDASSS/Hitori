from unittest.util import sorted_list_difference

from solver import HitoriSolver

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

grid_easy = [
	[1, 1, 1],
	[2, 3, 4],
	[5, 6, 7]
]

grid_super_easy = [
	[1, 1, 2],
	[2, 3, 1],
	[3, 1, 2]
]

grid_extended = [
	[1, 2, 3],
	[4, 5, 6],
	[2, 4, 1],
	[4, 6, 5]
]



solution = HitoriSolver.solve(grid_extended, True)
print(solution)