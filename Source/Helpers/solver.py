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
