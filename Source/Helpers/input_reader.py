import curses
import logging


class InputReader:
    @staticmethod
    def get_row_input(screen, row_number: int) -> str:
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
    def validate_row(grid: list[list[int]], row: str, mode) -> list[int]:
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
    def get_user_input(screen, row: int, prompt: str) -> str:
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
