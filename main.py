from Source.interactive_mode import InteractiveMode
from Source.Helpers.input_reader import InputReader
import logging
import curses

logging.basicConfig(
    filename="Source/debug.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def print_menu(screen, menu, current_row):
    """Функция для отображения меню."""
    screen.clear()
    for idx, item in enumerate(menu):
        if idx == current_row:
            screen.attron(curses.A_REVERSE)
            screen.addstr(idx, 0, item)
            screen.attroff(curses.A_REVERSE)
        else:
            screen.addstr(idx, 0, item)
    screen.refresh()


def handle_mode_selection(screen):
    """Функция для обработки выбора версии игры."""
    mode_menu = ["Hitori Classic", "Hitori Extended", "Выход"]
    current_row = 0

    while True:
        print_menu(screen, mode_menu, current_row)
        key = screen.getch()

        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(mode_menu) - 1:
            current_row += 1
        elif key in (10, 13):  # Enter
            if current_row == 0:
                is_extended = False
                break
            elif current_row == 1:
                is_extended = True
                break
            elif current_row == 2:
                return None  # Выход из программы

    return is_extended


def handle_main_menu(screen, is_extended):
    """Функция для обработки основного меню."""
    main_menu = ["Интерактивный режим", "Решить головоломку", "Назад"]
    current_row = 0

    while True:
        print_menu(screen, main_menu, current_row)
        key = screen.getch()

        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(main_menu) - 1:
            current_row += 1
        elif key in (10, 13):  # Enter
            if current_row == 0:
                if handle_interactive_mode(screen, is_extended):
                    continue  # Возвращаемся в меню
            elif current_row == 1:
                if InputReader.solve_mode(screen, is_extended):
                    continue  # Возвращаемся в меню
            elif current_row == 2:
                return  # Возвращаемся в меню выбора версии


def handle_interactive_mode(screen, is_extended):
    """Функция для обработки интерактивного режима."""
    screen.clear()
    if is_extended:
        screen.addstr(0, 0, "Введите ширину поля: ")
        screen.refresh()

        width_input = get_user_input(screen, 0, "Введите ширину поля: ")
        if width_input is None:
            return False

        screen.addstr(1, 0, "Введите высоту поля: ")
        screen.refresh()

        height_input = get_user_input(screen, 1, "Введите высоту поля: ")
        if height_input is None:
            return False

        try:
            width = int(width_input)
            height = int(height_input)
            if width < 3 or height < 3 or width * height > 25 or height >= 10 or width >= 10:
                raise ValueError("Ширина и высота должны быть > 2 и < 10 и площадь не должна превышать 25")
        except ValueError as e:
            screen.addstr(2, 0, f"Ошибка: {str(e)}")
            screen.refresh()
            screen.getch()
            return False

        if InteractiveMode.do_interactive_mode(screen, is_extended, height, width):
            return True
    else:
        # TODO: A че больше нельзя?
        screen.addstr(0, 0, "Введите размер поля [3;5]: ")
        screen.refresh()

        size_input = get_user_input(screen, 0, "Введите размер поля [3;5]: ")
        if size_input is None:
            return False

        try:
            size = int(size_input)
            if size < 3 or size > 5:
                raise ValueError("Размер поля должен быть в пределах [3;5]")
        except ValueError as e:
            screen.addstr(1, 0, f"Ошибка: {str(e)}")
            screen.refresh()
            screen.getch()
            return False

        if InteractiveMode.do_interactive_mode(screen, is_extended, size, size):
            return True


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


def main(screen):
    curses.curs_set(0)

    while True:
        is_extended = handle_mode_selection(screen)
        if is_extended is None:
            break

        handle_main_menu(screen, is_extended)


if __name__ == "__main__":
    curses.wrapper(main)
