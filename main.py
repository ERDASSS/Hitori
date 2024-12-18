from __future__ import annotations

from Source.Modes.Modes.classic import Classic
from Source.Modes.Modes.extended import Extended
from Source.hitori import HitoriCLI
from Source.Helpers.reader import Reader

import argparse
import curses
import sys

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Play or solve a Hitori puzzle.")
    parser.add_argument(
        "-s", "--solve",
        type=Reader.parse_board_by_arg,
        help="Решить головоломку. Введите поле в следующем формате: '[a, b, ... ];[ ... ]; ... ;[ ... ]'.",
    )
    parser.add_argument(
        "-f", "--file",
        type=Reader.parse_board_from_file,
        help="Solve a puzzle from a file. Provide the path to a text file containing the board.",
    )
    parser.add_argument(
        "-m", "--mode",
        choices=["Classic", "Extended"],
        help="Определить режим для решения головоломки (Classic или Extended).",
    )
    parser.add_argument('-a', '--all', action='store_true', help='Отображать все решения.')
    try:
        args = parser.parse_args()
    except ValueError as e:
        print("Некорректный формат доски. Убедитесь, что данные введены в одном из верных форматов.")
        sys.exit(1)
    except Exception as e:
        print(e)
        sys.exit(1)

    if args.solve or args.file:
        if not args.mode:
            print("Ошибка: режим (-m или --mode) обязателен для решения головоломки.", file=sys.stderr)
            sys.exit(1)
        board = args.solve if args.solve else args.file
        mode = Classic() if args.mode == "Classic" else Extended()
        try:
            mode.validate_grid(board)
        except ValueError as e:
            print("Некорректные данные: ", e)
            print("Пожалуйста, проверте соответсвие вводимх данных одному из форматов и введёный режим игры")
            sys.exit(1)
        HitoriCLI.print_solution_by_args(board, mode, args.all)
    else:
        curses.wrapper(HitoriCLI.run)
