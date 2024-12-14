from __future__ import annotations

from Source.Modes.mode import Mode
from Source.Helpers.input_reader import InputReader


class Classic(Mode):
    NAME = "Classic"
    @staticmethod
    def read_grid_info(screen) -> None | tuple[int, int]:
        # TODO: A че больше нельзя?
        screen.addstr(0, 0, "Введите размер поля [3;5]: ")
        screen.refresh()

        size_input = InputReader.get_user_input(screen, 0, "Введите размер поля [3;5]: ")
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
        # if InteractiveMode.do_interactive_mode(screen, is_extended, size, size):
        #     return True

    @staticmethod
    def display_input_info(screen):
        screen.addstr(0, 0, "Введите головоломку строка за строкой, разделяя числа пробелами:")
