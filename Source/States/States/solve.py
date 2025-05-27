from __future__ import annotations

import logging

from Source.Modes.Modes.triangle import Triangle
from Source.States.state import State
from Source.Helpers.reader import Reader
from Source.Helpers.display import Display
from Source.Helpers.solver import Solver, SolverTriangle
from Source.Modes.Modes.extended import Extended
from Source.Modes.Modes.classic import Classic


class Solve(State):
    @staticmethod
    def handle(screen, mode: Classic | Extended, height: int, width: int):
        Display.display_instructions(screen, mode)
        is_extended = mode.NAME == "Extended"
        grid = []
        while True:
            row_input = Reader.get_row_input(screen, len(grid))
            if is_extended and row_input == "":
                break

            try:
                row = Reader.validate_row(grid, row_input, mode)
                grid.append(row)
            except ValueError as e:
                screen.addstr(len(grid) + 2, 0, f"Ошибка ввода: {str(e)}")
                screen.refresh()
                screen.getch()
                return False  # Возвращаем False, чтобы указать, что режим завершился с ошибкой

            if len(grid) + 1 == len(row) + 1 and not is_extended:
                break

        try:
            mode.validate_grid(grid)
            solutions = Solver.solve(grid, mode)
        except Exception as e:
            screen.addstr(len(grid) + 3, 0, f"Ошибка решения: {str(e)}")
            screen.refresh()
            screen.getch()
            return False  # Возвращаем False, чтобы указать, что режим завершился с ошибкой

        if len(solutions) == 0:
            screen.clear()
            screen.addstr(0, 0, "Введенная головоломка:")
            for row_idx, row in enumerate(grid):
                screen.addstr(row_idx + 1, 0, " ".join(map(str, row)))

            screen.addstr(len(grid) + 2, 0, "Решений нет. Нажмите любую клавишу для выхода.")
            screen.refresh()
            screen.getch()
            return False  # Возвращаем False, чтобы указать, что режим завершился с ошибкой

        return Display.display_solutions(screen, grid, solutions, mode)

    @staticmethod
    def handle_triangle(screen):
        screen.clear()
        screen.addstr(0, 0, "Введите размер максимальной (нижней) стороны треугольника: ")
        screen.refresh()

        max_row_len = Reader.get_user_input(screen, 0, "Введите размер максимальной (нижней) стороны треугольника: ")
        if max_row_len is None:
            return None


        Display.display_instructions(screen, Triangle)
        grid = []
        while True:
            row_input = Reader.get_row_input_triangle(screen, len(grid), int(max_row_len))

            try:
                row = list(map(int, row_input.split()))
                Triangle.validate_row(row, len(grid) + 1)
                logging.debug(f"row {row}")
                grid.append(row)
            except ValueError as e:
                screen.addstr(len(grid) + 2, 0, f"Ошибка ввода: {str(e)}")
                screen.refresh()
                screen.getch()
                return False  # Возвращаем False, чтобы указать, что режим завершился с ошибкой

            if len(grid) + 1 == int(max_row_len) + 1:
                break

        try:
            Triangle.validate_grid(grid)
            solutions = SolverTriangle.solve(grid)
        except Exception as e:
            screen.addstr(len(grid) + 3, 0, f"Ошибка решения: {str(e)}")
            screen.refresh()
            screen.getch()
            return False  # Возвращаем False, чтобы указать, что режим завершился с ошибкой

        if len(solutions) == 0:
            screen.clear()
            screen.addstr(0, 0, "Введенная головоломка:")
            for row_idx, row in enumerate(grid):
                screen.addstr(row_idx + 1, len(grid[-1]) - row_idx + 1, " ".join(map(str, row)))

            screen.addstr(len(grid) + 2, 0, "Решений нет. Нажмите любую клавишу для выхода.")
            screen.refresh()
            screen.getch()
            return False  # Возвращаем False, чтобы указать, что режим завершился с ошибкой

        return Display.display_solutions(screen, grid, solutions, Triangle)
