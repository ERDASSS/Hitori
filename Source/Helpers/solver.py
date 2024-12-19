from __future__ import annotations

from Source.Modes.Modes.classic import Classic
from Source.Modes.Modes.extended import Extended
from itertools import product
import logging

logging.basicConfig(
    filename="debug.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class Solver:
    @staticmethod
    def grid_is_valid(grid: list[list[int | str]], mode: Classic | Extended) -> bool:
        """
        Проверяет, является ли текущая сетка допустимой по правилам Hitori.
        """
        width = len(grid[0])
        height = len(grid)

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

        return Solver.check_neighbours(grid, mode)

    @staticmethod
    def check_neighbours(grid: list[list[int | str]], mode: Classic | Extended) -> bool:
        """
        Проверяет, что никакие две закрашенные клетки не являются соседними.
        """
        width = len(grid[0])
        height = len(grid)

        neighbours = mode.get_neighbours()

        for i, j in product(range(height), range(width)):
            if grid[i][j] == "X":
                for di, dj in neighbours:
                    ni, nj = i + di, j + dj
                    if 0 <= ni < height and 0 <= nj < width and grid[ni][nj] == "X":
                        return False
        return True

    @staticmethod
    def is_connected(grid: list[list[int | str]]) -> bool:
        """
        Проверяет, связаны ли все не закрашенные клетки в единую область.
        """
        width = len(grid[0])
        height = len(grid)

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
    def is_solvable(grid: list[list[int]], mode: Classic | Extended) -> bool:
        """
        Проверяет, решаема ли данная сетка.
        """
        try:
            solutions = Solver.solve(grid, mode)

            if len(solutions) == 1:
                x_count = sum(row.count("X") for row in solutions[0])
                if x_count == 0:
                    return False

            return len(solutions) > 0
        except Exception as e:
            logging.debug(f"Solver error: {e}")
            return False

    @staticmethod
    def solve(grid: list[list[int | str]], mode: Classic | Extended) -> list[list[list[int]]]:
        """
        Решает головоломку Hitori. Возвращает список состояний сетки.
        """
        width = len(grid[0])
        height = len(grid)

        def backtrack(grid: list[list[int | str]], candidates: list[tuple[int, int]]) -> list[list[list[int]]]:
            if not candidates:
                # Проверяем, является ли решение допустимым
                if Solver.grid_is_valid(grid, mode) and Solver.is_connected(grid):
                    return [[row[:] for row in grid]]
                return []

            row, col = candidates.pop()
            solutions = []

            # Пробуем оставить клетку как есть
            solutions.extend(backtrack([row[:] for row in grid], candidates[:]))

            # Пробуем закрасить клетку
            grid[row][col] = "X"
            if Solver.check_neighbours(grid, mode) and Solver.is_connected(grid):
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


class SolverTriangle:
    @staticmethod
    def get_neighbors(grid, i, j):
        neighbors = []
        if j > i:
            raise ValueError
        # Up-right
        if i > 0 and j < len(grid[i - 1]):
            neighbors.append((i - 1, j))
        # Up-left
        if i > 0 and j - 1 >= 0:
            neighbors.append((i - 1, j - 1))
        # Down-left
        if i + 1 < len(grid) and j < len(grid[i + 1]):
            neighbors.append((i + 1, j))
        # Down-right
        if i + 1 < len(grid) and j + 1 < len(grid[i + 1]):
            neighbors.append((i + 1, j + 1))
        # Left
        if j > 0:
            neighbors.append((i, j - 1))
        # Right
        if j < len(grid[i]) - 1:
            neighbors.append((i, j + 1))

        return neighbors

    @staticmethod
    def check_neighbours(grid: list[list[int | str]]) -> bool:
        """
        Checks that no two "X" cells are adjacent in the triangular grid.
        """
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                if grid[i][j] == "X":
                    neighbors = SolverTriangle.get_neighbors(grid, i, j)
                    for ni, nj in neighbors:
                        if grid[ni][nj] == "X":
                            return False
        return True

    @staticmethod
    def is_connected(grid: list[list[int | str]]) -> bool:
        """
        Checks if all non-"X" cells in the triangular grid form a single connected region.
        """
        height = len(grid)
        visited = [[False] * len(row) for row in grid]

        # Find the starting cell that is not "X"
        start = None
        for i in range(height):
            for j in range(len(grid[i])):
                if grid[i][j] != "X":
                    start = (i, j)
                    break
            if start:
                break

        if not start:
            return False  # No non-"X" cells

        # BFS to check connectivity
        queue = [start]
        visited[start[0]][start[1]] = True
        count = 1
        total_non_X = sum(1 for row in grid for cell in row if cell != "X")

        while queue:
            x, y = queue.pop(0)
            neighbors = SolverTriangle.get_neighbors(grid, x, y)
            for nx, ny in neighbors:
                if not visited[nx][ny] and grid[nx][ny] != "X":
                    visited[nx][ny] = True
                    queue.append((nx, ny))
                    count += 1

        return count == total_non_X

    @staticmethod
    def grid_is_valid(grid: list[list[int | str]]) -> bool:
        """
        Checks if the current grid is valid according to Hitori rules for a triangular grid.
        """
        for current_row in range(0, len(grid)):
            col_counts_slash = {}
            col_counts_backslash = {}
            current_j_slash = 0
            current_j_backslash = current_row

            for i in range(current_row, len(grid)):
                value = grid[i][current_j_slash]
                col_counts_slash.setdefault(value, []).append((i, current_j_slash))
                current_j_slash += 1

            for i in range(current_row, len(grid)):
                value = grid[i][current_j_backslash]
                col_counts_backslash.setdefault(value, []).append((i, current_j_backslash))

            for positions in col_counts_slash.values():
                if len(positions) > 1:
                    return False

            for positions in col_counts_backslash.values():
                if len(positions) > 1:
                    return False

        # Check for duplicates in horizontal rows
        for row in grid:
            seen = {}
            for value in row:
                if value != "X":
                    if value in seen:
                        return False
                    seen[value] = True

        return SolverTriangle.check_neighbours(grid) and SolverTriangle.is_connected(grid)

    @staticmethod
    def solve(grid: list[list[int | str]]) -> list[list[list[int]]]:
        """
		Решает треугольное поле Hitori. Возвращает список состояний сетки.
		"""

        def backtrack(grid: list[list[int | str]], candidates: list[tuple[int, int]]) -> list[list[list[int]]]:
            if not candidates:
                # Проверяем, является ли решение допустимым
                if SolverTriangle.grid_is_valid(grid) and SolverTriangle.is_connected(grid):
                    return [[row[:] for row in grid]]
                return []

            row, col = candidates.pop()
            solutions = []

            # Пробуем оставить клетку как есть
            solutions.extend(backtrack([row[:] for row in grid], candidates[:]))

            # Пробуем закрасить клетку
            grid[row][col] = "X"
            if SolverTriangle.check_neighbours(grid) and SolverTriangle.is_connected(grid):
                solutions.extend(backtrack([row[:] for row in grid], candidates[:]))

            # Отменяем изменения
            grid[row][col] = original_grid[row][col]
            candidates.append((row, col))

            return solutions

        # Формируем список кандидатов для закраски (ячейки с дубликатами в строках или "треугольных" колонках)
        candidates = set()
        for i, row in enumerate(grid):
            row_counts = {}
            for j, value_begin in enumerate(row):
                # Анализ строки
                if value_begin not in row_counts:
                    row_counts[value_begin] = []
                row_counts[value_begin].append((i, j))

            for positions in row_counts.values():
                if len(positions) > 1:
                    candidates.update(positions)


        for current_row in range(0, len(grid)):
            col_counts_slash = {}
            col_counts_backslash = {}
            current_j_slash = 0
            current_j_backslash = current_row

            for i in range(current_row, len(grid)):
                value = grid[i][current_j_slash]
                col_counts_slash.setdefault(value, []).append((i, current_j_slash))
                current_j_slash += 1

            for i in range(current_row, len(grid)):
                value = grid[i][current_j_backslash]
                col_counts_backslash.setdefault(value, []).append((i, current_j_backslash))

            for positions in col_counts_slash.values():
                if len(positions) > 1:
                    candidates.update(positions)

            for positions in col_counts_backslash.values():
                if len(positions) > 1:
                    candidates.update(positions)


        original_grid = [row[:] for row in grid]
        return backtrack(grid, list(set(candidates)))
