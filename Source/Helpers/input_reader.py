from Source.Helpers.solver import Solver
from Source.display import Display
import curses
import logging


class InputReader:
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
    def _validate_row(grid, row, mode):
        """
        Проверяет корректность введенной строки.
        """
        row = list(map(int, row.split()))
        logging.debug(f"num_count {len(row)}")

        if grid and len(row) != len(grid[0]):
            raise ValueError("Все строки должны быть одной длины.")

        mode.validate_row(row)

        return row

    @staticmethod
    def get_user_input(screen, row, prompt):
        """Функция для получения ввода пользователя."""
        screen.addstr(row, 0, prompt)
        screen.refresh()

        user_input = ""
        while True:
            key = screen.getch()
            if key in (10, 13):  # Enter
                break
            elif key in (8, 127, curses.KEY_BACKSPACE):  # Backspace
                if user_input:
                    user_input = user_input[:-1]
                    screen.addstr(row, len(prompt) + len(user_input), " ")
                    screen.refresh()
            elif 48 <= key <= 57:  # Цифры
                user_input += chr(key)
                screen.addstr(row, len(prompt), user_input)
                screen.refresh()

        return user_input

    @staticmethod
    def solve_mode(screen, mode):
        Display.display_instructions(screen, mode)
        is_extended = mode.NAME == "Extended"
        grid = []
        while True:
            row_input = InputReader.get_row_input(screen, len(grid))
            if is_extended and row_input == "":
                break

            try:
                row = InputReader._validate_row(grid, row_input, mode)
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
