import logging
import curses
from interactive_mode import InteractiveMode
from solve_mode import SolveMode

logging.basicConfig(
    filename="debug.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def print_menu(stdscr, menu, current_row):
    """Функция для отображения меню."""
    stdscr.clear()
    for idx, item in enumerate(menu):
        if idx == current_row:
            stdscr.attron(curses.A_REVERSE)
            stdscr.addstr(idx, 0, item)
            stdscr.attroff(curses.A_REVERSE)
        else:
            stdscr.addstr(idx, 0, item)
    stdscr.refresh()

def handle_mode_selection(stdscr):
    """Функция для обработки выбора версии игры."""
    mode_menu = ["Hitori Classic", "Hitori Extended", "Выход"]
    current_row = 0
    is_extended = False

    while True:
        print_menu(stdscr, mode_menu, current_row)
        key = stdscr.getch()

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

def handle_main_menu(stdscr, is_extended):
    """Функция для обработки основного меню."""
    main_menu = ["Интерактивный режим", "Решить головоломку", "Назад"]
    current_row = 0

    while True:
        print_menu(stdscr, main_menu, current_row)
        key = stdscr.getch()

        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(main_menu) - 1:
            current_row += 1
        elif key in (10, 13):  # Enter
            if current_row == 0:
                if handle_interactive_mode(stdscr, is_extended):
                    continue  # Возвращаемся в меню
            elif current_row == 1:
                if SolveMode.solve_mode(stdscr, is_extended):
                    continue  # Возвращаемся в меню
            elif current_row == 2:
                return  # Возвращаемся в меню выбора версии

def handle_interactive_mode(stdscr, is_extended):
    """Функция для обработки интерактивного режима."""
    stdscr.clear()
    if is_extended:
        stdscr.addstr(0, 0, "Введите ширину поля: ")
        stdscr.refresh()

        width_input = get_user_input(stdscr, 0, "Введите ширину поля: ")
        if width_input is None:
            return False

        stdscr.addstr(1, 0, "Введите высоту поля: ")
        stdscr.refresh()

        height_input = get_user_input(stdscr, 1, "Введите высоту поля: ")
        if height_input is None:
            return False

        try:
            width = int(width_input)
            height = int(height_input)
            if width < 3 or height < 3 or width * height > 25 or height >= 10 or width >= 10:
                raise ValueError("Ширина и высота должны быть > 2 и < 10 и площадь не должна превышать 25")
        except ValueError as e:
            stdscr.addstr(2, 0, f"Ошибка: {str(e)}")
            stdscr.refresh()
            stdscr.getch()
            return False

        if InteractiveMode.do_interactive_mode(stdscr, is_extended, height, width):
            return True
    else:
        stdscr.addstr(0, 0, "Введите размер поля [3;5]: ")
        stdscr.refresh()

        size_input = get_user_input(stdscr, 0, "Введите размер поля [3;5]: ")
        if size_input is None:
            return False

        try:
            size = int(size_input)
            if size < 3 or size > 5:
                raise ValueError("Размер поля должен быть в пределах [3;5]")
        except ValueError as e:
            stdscr.addstr(1, 0, f"Ошибка: {str(e)}")
            stdscr.refresh()
            stdscr.getch()
            return False

        if InteractiveMode.do_interactive_mode(stdscr, is_extended, size, size):
            return True

def get_user_input(stdscr, row, prompt):
    """Функция для получения ввода пользователя."""
    stdscr.addstr(row, 0, prompt)
    stdscr.refresh()

    user_input = ""
    while True:
        key = stdscr.getch()
        if key in (10, 13):  # Enter
            break
        elif key in (8, 127, curses.KEY_BACKSPACE):  # Backspace
            if user_input:
                user_input = user_input[:-1]
                stdscr.addstr(row, len(prompt) + len(user_input), " ")
                stdscr.refresh()
        elif 48 <= key <= 57:  # Цифры
            user_input += chr(key)
            stdscr.addstr(row, len(prompt), user_input)
            stdscr.refresh()

    return user_input

def main(stdscr):
    curses.curs_set(0)

    while True:
        is_extended = handle_mode_selection(stdscr)
        if is_extended is None:
            break

        handle_main_menu(stdscr, is_extended)

if __name__ == "__main__":
    curses.wrapper(main)