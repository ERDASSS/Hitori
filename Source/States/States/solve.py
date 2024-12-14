from __future__ import annotations

from Source.States.state import State
from Source.Helpers.input_reader import InputReader
from Source.display import Display
from Source.Helpers.solver import Solver
from Source.Modes.Modes.extended import Extended
from Source.Modes.Modes.classic import Classic


class Solve(State):
    @staticmethod
    def handle(screen, mode: Classic | Extended, height: int, width: int):
        Display.display_instructions(screen, mode)
        is_extended = mode.NAME == "Extended"
        grid = []
        while True:
            row_input = InputReader.get_row_input(screen, len(grid))
            if is_extended and row_input == "":
                break

            try:
                row = InputReader.validate_row(grid, row_input, mode)
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

        return Display.display_solutions(screen, grid, solutions)
