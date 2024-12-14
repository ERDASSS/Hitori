from __future__ import annotations

from Source.Modes.Modes.classic import Classic
from Source.Modes.Modes.extended import Extended
from Source.States.States.solve import Solve
from Source.States.States.interactive import Interactive

import logging
import curses

logging.basicConfig(
    filename="Source/debug.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def print_menu(screen, menu: list[str], current_row: int):
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


def handle_mode_selection(screen) -> None | Classic | Extended:
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
                mode = Classic()
                break
            elif current_row == 1:
                mode = Extended()
                break
            elif current_row == 2:
                return None  # Выход из программы

    return mode


def handle_main_menu(screen, mode: Classic | Extended):
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
                if handle_interactive_mode(screen, mode):
                    continue  # Возвращаемся в меню
            elif current_row == 1:
                # None, None - заглушки для width и height
                if Solve.handle(screen, mode, None, None):
                    continue  # Возвращаемся в меню
            elif current_row == 2:
                return  # Возвращаемся в меню выбора версии


def handle_interactive_mode(screen, mode: Classic | Extended) -> bool:
    """Функция для обработки интерактивного режима."""
    screen.clear()
    size_data = mode.read_grid_info(screen)
    if size_data:
        width, height = size_data
        if Interactive.handle(screen, mode, height, width):
            return True
    return False


def main(screen):
    curses.curs_set(0)

    while True:
        mode = handle_mode_selection(screen)
        if mode is None:
            break

        handle_main_menu(screen, mode)


if __name__ == "__main__":
    curses.wrapper(main)
