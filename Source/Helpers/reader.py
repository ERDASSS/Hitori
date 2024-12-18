import curses
import logging


class Reader:
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

    @staticmethod
    def parse_board_by_arg(board_str: str):
        """Parse the board string into a 2D list."""
        try:
            parts = board_str.rsplit(":", 1)
            if ":" in board_str:
                # Space-separated format with explicit dimensions
                numbers_str, dimensions = parts[0].strip(), parts[1].strip()
                width, height = map(int, dimensions.lower().split("x"))
                numbers = list(map(int, numbers_str.split()))

                if len(numbers) != width * height:
                    raise ValueError("Number of elements does not match the specified dimensions.")

                board = [numbers[i * width:(i + 1) * width] for i in range(height)]
            elif "," in board_str:
                board = [[int(num) for num in row.split(",")] for row in board_str.split(";")]
            else:
                numbers_str = parts[0].strip()
                numbers = list(map(int, numbers_str.split()))
                width = height = int(len(numbers) ** 0.5)

                if len(numbers) != width * height:
                    raise ValueError("Number of elements does not match the specified dimensions.")

                board = [numbers[i * width:(i + 1) * width] for i in range(height)]

            len_row = len(board[0])
            for row in board:
                if len_row != len(row):
                    raise ValueError("Number of elements does not match the specified dimensions.")

            return board
        except Exception as e:
            raise ValueError()

    @staticmethod
    def parse_board_from_file(file_path: str):
        """Parse the board from a file."""
        try:
            with open(file_path, "r") as f:
                board_str = f.read().strip()

                # New logic: Check for space-separated and newline-separated format
                if "\n" in board_str and not (", " in board_str or ": " in board_str):
                    board = [[int(num) for num in line.split()] for line in board_str.splitlines()]
                else:
                    # Fall back to parsing using existing logic
                    return Reader.parse_board_by_arg(board_str)

                len_row = len(board[0])
                for row in board:
                    if len_row != len(row):
                        raise ValueError("Rows are not of consistent length in the file.")

                return board
        except FileNotFoundError:
            raise ValueError(f"File not found: {file_path}")
        except PermissionError:
            raise ValueError(f"Permission denied: {file_path}")
        except IsADirectoryError:
            raise ValueError(f"Expected a file but found a directory: {file_path}")
        except ValueError as e:
            raise ValueError(f"Error parsing board from file: {e}")
        except Exception as e:
            raise ValueError(f"An unexpected error occurred while reading the file: {e}")