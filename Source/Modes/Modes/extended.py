from __future__ import annotations

from Source.Modes.mode import Mode
from Source.Helpers.input_reader import InputReader


class Extended(Mode):
    NAME = "Extended"

    @staticmethod
    def read_grid_info(screen) -> None | tuple[int, int]:
        screen.addstr(0, 0, "Введите ширину поля: ")
        screen.refresh()

        width_input = InputReader.get_user_input(screen, 0, "Введите ширину поля: ")
        if width_input is None:
            return None

        screen.addstr(1, 0, "Введите высоту поля: ")
        screen.refresh()

        height_input = InputReader.get_user_input(screen, 1, "Введите высоту поля: ")
        if height_input is None:
            return None

        try:
            width = int(width_input)
            height = int(height_input)
            if width < 3 or height < 3 or width * height > 25 or height >= 10 or width >= 10:
                raise ValueError("Ширина и высота должны быть > 2 и < 10 и площадь не должна превышать 25")
        except ValueError as e:
            screen.addstr(2, 0, f"Ошибка: {str(e)}")
            screen.refresh()
            screen.getch()
            return None

        return width, height
        # if InteractiveMode.do_interactive_mode(screen, is_extended, height, width):
        #     return True

    @staticmethod
    def display_input_info(screen):
        screen.addstr(0, 0, "Введите головоломку строка за строкой, разделяя числа пробелами."
                            " Для завершения введите пустую строку:")