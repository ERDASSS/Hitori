from itertools import product
import logging

logging.basicConfig(
	filename="debug.log",
	level=logging.DEBUG,
	format="%(asctime)s - %(levelname)s - %(message)s"
)

class HitoriSolver:
	@staticmethod
	def is_valid(grid, is_extended):
		"""
		Проверяет, является ли текущая сетка допустимой по правилам Hitori.
		"""
		if is_extended:
			width = len(grid[0])
			height = len(grid)
		else:
			width = height = len(grid)

		# Проверка на дубли в строках и столбцах
		for i in range(height):
			row_values = {}
			for j in range(width):
				# Проверка строки
				if grid[i][j] != "X":
					if grid[i][j] in row_values:
						return False
					row_values[grid[i][j]] = True

		for j in range(width):
			col_values = {}
			for i in range(height):
				# Проверка столбца
				if grid[i][j] != "X":
					if grid[i][j] in col_values:
						return False
					col_values[grid[i][j]] = True

		return HitoriSolver.check_neighbours(grid, is_extended)

	@staticmethod
	def check_neighbours(grid, is_extended):
		"""
		Проверяет, что никакие две закрашенные клетки не являются соседними.
		"""
		if is_extended:
			width = len(grid[0])
			height = len(grid)
		else:
			width = height = len(grid)

		neighbours = [(-1, 0), (1, 0), (0, -1), (0, 1)]
		if is_extended:
			neighbours.extend([(-1, -1), (1, 1), (-1, 1), (1, -1)])

		for i, j in product(range(height), range(width)):
			if grid[i][j] == "X":
				for di, dj in neighbours:
					ni, nj = i + di, j + dj
					if 0 <= ni < height and 0 <= nj < width and grid[ni][nj] == "X":
						return False

		return True

	@staticmethod
	def is_connected(grid, is_extended):
		"""
		Проверяет, связаны ли все не закрашенные клетки в единую область.
		"""
		if is_extended:
			width = len(grid[0])
			height = len(grid)
		else:
			width = height = len(grid)

		visited = [[False for _ in range(width)] for _ in range(height)]

		# Найти стартовую не закрашенную клетку
		start = None
		for i, j in product(range(height), range(width)):
			if grid[i][j] != "X":
				start = (i, j)
				break

		if not start:
			return False  # Если все клетки закрашены, это недопустимо

		# BFS для проверки связности
		queue = [start]
		visited[start[0]][start[1]] = True
		count = 0

		while queue:
			x, y = queue.pop(0)
			count += 1

			for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
				nx, ny = x + dx, y + dy
				if 0 <= nx < height and 0 <= ny < width and not visited[nx][ny] and grid[nx][ny] != "X":
					visited[nx][ny] = True
					queue.append((nx, ny))

		# Убедиться, что все не закрашенные клетки посещены
		total_unshaded = sum(1 for i, j in product(range(height), range(width)) if grid[i][j] != "X")
		return count == total_unshaded

	@staticmethod
	def solve(grid, is_extended):
		"""
		Решает головоломку Hitori. Возвращает список состояний сетки.
		"""
		if is_extended:
			width = len(grid[0])
			height = len(grid)
		else:
			width = height = len(grid)

		def backtrack(grid, candidates):
			if not candidates:
				# Проверяем, является ли решение допустимым
				if HitoriSolver.is_valid(grid, is_extended) and HitoriSolver.is_connected(grid, is_extended):
					return [[row[:] for row in grid]]
				return []

			row, col = candidates.pop()
			solutions = []

			# Пробуем оставить клетку как есть
			solutions.extend(backtrack([row[:] for row in grid], candidates[:]))

			# Пробуем закрасить клетку
			grid[row][col] = "X"
			if HitoriSolver.check_neighbours(grid, is_extended) and HitoriSolver.is_connected(grid, is_extended):
				solutions.extend(backtrack([row[:] for row in grid], candidates[:]))

			# Отменяем изменения
			grid[row][col] = original_grid[row][col]
			candidates.append((row, col))

			return solutions

		# Формируем список кандидатов для закраски (ячейки с дубликатами в строках или столбцах)
		candidates = []
		for i in range(height):
			row_counts = {}
			for j in range(width):
				# Анализ строки
				if grid[i][j] not in row_counts:
					row_counts[grid[i][j]] = []
				row_counts[grid[i][j]].append((i, j))

			for positions in row_counts.values():
				if len(positions) > 1:
					candidates.extend(positions)

		for j in range(width):
			col_counts = {}
			for i in range(height):
				# Анализ столбца
				if grid[i][j] not in col_counts:
					col_counts[grid[i][j]] = []
				col_counts[grid[i][j]].append((i, j))

			for positions in col_counts.values():
				if len(positions) > 1:
					candidates.extend(positions)

		original_grid = [row[:] for row in grid]
		return backtrack(grid, list(set(candidates)))


