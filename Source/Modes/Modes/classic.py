from __future__ import annotations

from Source.Modes.mode import Mode
from Source.Helpers.reader import Reader


class Classic(Mode):
    NAME = "Classic"

    @staticmethod
    def read_grid_info(screen) -> None | tuple[int, int]:
        screen.addstr(0, 0, "Введите размер поля [3;5]: ")
        screen.refresh()

        size_input = Reader.get_user_input(screen, 0, "Введите размер поля [3;5]: ")
        if size_input is None:
            return None

        try:
            size = int(size_input)
            if size < 3 or size > 5:
                raise ValueError("Размер поля должен быть в пределах [3;5]")
        except ValueError as e:
            screen.addstr(1, 0, f"Ошибка: {str(e)}")
            screen.refresh()
            screen.getch()
            return None

        return size, size

    @staticmethod
    def display_input_info(screen):
        screen.addstr(0, 0, "Введите головоломку строка за строкой, разделяя числа пробелами:")

    @staticmethod
    def validate_row(row: list[int], max_len = None):
        for num in row:
            if num > len(row):
                raise ValueError("Числа не должны превышать размер квадрата")
            if num <= 0:
                raise ValueError("Числа должны быть больше 0")

    @staticmethod
    def get_neighbours() -> list:
        return [(-1, 0), (1, 0), (0, -1), (0, 1)]
