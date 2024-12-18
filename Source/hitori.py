from __future__ import annotations

from Source.Modes.Modes.classic import Classic
from Source.Modes.Modes.extended import Extended
from Source.States.States.solve import Solve
from Source.States.States.interactive import Interactive
from Source.Helpers.solver import Solver

import argparse
import logging
import curses

logging.basicConfig(
    filename="Source/debug.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


class HitoriCLI:
    @staticmethod
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

    @staticmethod
    def handle_mode_selection(screen) -> None | Classic | Extended:
        """Функция для обработки выбора версии игры."""
        mode_menu = ["Hitori Classic", "Hitori Extended", "Выход"]
        current_row = 0

        while True:
            HitoriCLI.print_menu(screen, mode_menu, current_row)
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

    @staticmethod
    def handle_main_menu(screen, mode: Classic | Extended):
        """Функция для обработки основного меню."""
        main_menu = ["Интерактивный режим", "Решить головоломку", "Назад"]
        current_row = 0

        while True:
            HitoriCLI.print_menu(screen, main_menu, current_row)
            key = screen.getch()

            if key == curses.KEY_UP and current_row > 0:
                current_row -= 1
            elif key == curses.KEY_DOWN and current_row < len(main_menu) - 1:
                current_row += 1
            elif key in (10, 13):  # Enter
                if current_row == 0:
                    if HitoriCLI.handle_interactive_mode(screen, mode):
                        continue  # Возвращаемся в меню
                elif current_row == 1:
                    # None, None - заглушки для width и height
                    if Solve.handle(screen, mode, None, None):
                        continue  # Возвращаемся в меню
                elif current_row == 2:
                    return  # Возвращаемся в меню выбора версии

    @staticmethod
    def handle_interactive_mode(screen, mode: Classic | Extended) -> bool:
        """Функция для обработки интерактивного режима."""
        screen.clear()
        size_data = mode.read_grid_info(screen)
        if size_data:
            width, height = size_data
            if Interactive.handle(screen, mode, height, width):
                return True
        return False

    @staticmethod
    def run(screen):
        curses.curs_set(0)

        while True:
            mode = HitoriCLI.handle_mode_selection(screen)
            if mode is None:
                break

            HitoriCLI.handle_main_menu(screen, mode)

    @staticmethod
    def print_solution_by_args(bord: list[list[int]], game_mode: Classic | Extended, show_all_solutions: bool):
        solutions = Solver.solve(bord, game_mode)

        if len(solutions) == 0:
            print("Решений для данного поля нету.")
            return

        def _show_solution(_solution: list[list[int | str]]):
            res = ""
            for row in _solution:
                res += " ".join(map(str, row)) + "\n"
            print(res)

        if show_all_solutions:
            current_solution_index = 1
            len_solutions = len(solutions)
            for solution in solutions:
                print(f"\nРешениe {current_solution_index} из {len_solutions}:\n")
                _show_solution(solution)
        else:
            print("\nОдно из решений:")
            _show_solution(solutions[0])
