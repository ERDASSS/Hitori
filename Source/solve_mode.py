import curses
import logging
from Source.solver import HitoriSolver
from Source.display import Display


class SolveMode:

    @staticmethod
    def get_row_input(screen, row_number):
        """
        Получает ввод строки от пользователя.
        """
        screen.addstr(row_number + 1, 0, f"Строка {row_number + 1}: ")
        screen.refresh()

        row_input = ""
        cursor_pos = len(f"Строка {row_number + 1}: ")
        while True:
            key = screen.getch()
            if key in (10, 13):  # Enter
                break
            elif key in (8, 127, curses.KEY_BACKSPACE):  # Backspace
                if cursor_pos > len(f"Строка {row_number + 1}: "):
                    row_input = row_input[:-1]
                    cursor_pos -= 1
                    screen.addstr(row_number + 1, cursor_pos, " ")
                    screen.refresh()
            elif 48 <= key <= 57 or key == ord(" "):  # Цифры и пробелы
                row_input += chr(key)
                cursor_pos += 1
            screen.addstr(row_number + 1, len(f"Строка {row_number + 1}: "), row_input)
            screen.refresh()

        return row_input

    @staticmethod
    def validate_row(grid, row, is_extended):
        """
        Проверяет корректность введенной строки.
        """
        row = list(map(int, row.split()))
        logging.debug(f"num_count {len(row)}")

        if grid and len(row) != len(grid[0]):
            raise ValueError("Все строки должны быть одной длины.")
        for num in row:
            if num > len(row) and not is_extended:
                raise ValueError("Числа не должны превышать размер квадрата")
            if not is_extended and num <= 0:
                raise ValueError("Числа должны быть больше 0")

        return row

    @staticmethod
    def validate_grid(grid, is_extended):
        """
        Проверяет корректность всей сетки.
        """
        if is_extended:
            max_width = len(grid[0])
            max_height = len(grid)
            max_allowed = max(max_width, max_height)
            for row in grid:
                for num in row:
                    if num > max_allowed:
                        raise ValueError(f"Число {num} превышает финальное допустимое значение {max_allowed}.")

    @staticmethod
    def solve_mode(screen, is_extended):
        Display.display_instructions(screen, is_extended)

        grid = []
        while True:
            row_input = SolveMode.get_row_input(screen, len(grid))
            if is_extended and row_input == "":
                break

            try:
                row = SolveMode.validate_row(grid, row_input, is_extended)
                grid.append(row)
            except ValueError as e:
                screen.addstr(len(grid) + 2, 0, f"Ошибка ввода: {str(e)}")
                screen.refresh()
                screen.getch()
                return False  # Возвращаем False, чтобы указать, что режим завершился с ошибкой

            if len(grid) + 1 == len(row) + 1 and not is_extended:
                break

        try:
            SolveMode.validate_grid(grid, is_extended)
            solutions = HitoriSolver.solve(grid, is_extended)
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
