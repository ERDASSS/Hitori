from __future__ import annotations

from Source.Modes.Modes.classic import Classic
from Source.Modes.Modes.extended import Extended
from Source.hitori import HitoriCLI

import argparse
import curses
import sys


def parse_board(board_str: str):
    """Parse the board string into a 2D list."""
    try:
        board = [[int(num) for num in row.split(",")] for row in board_str.split(";")]
        return board
    except ValueError:
        raise argparse.ArgumentTypeError(
            "Некорректный формат доски. Убедитесь, что строки разделены ';' и сами значения разделены ','")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Play or solve a Hitori puzzle.")
    parser.add_argument(
        "-s", "--solve",
        type=parse_board,
        help="Решить головоломку. Введите поле в следующем формате: '[a, b, ... ];[ ... ]; ... ;[ ... ]'.",
    )
    parser.add_argument(
        "-m", "--mode",
        choices=["Classic", "Extended"],
        help="Определить режим для решения головоломки (Classic или Extended).",
    )
    parser.add_argument('-a', '--all', action='store_true', help='Отображать все решения.')

    args = parser.parse_args()

    if args.solve:
        if not args.mode:
            print("Ошибка: режим (-m или --mode) обязателен для решения головоломки.", file=sys.stderr)
            sys.exit(1)
        board = args.solve
        mode = Classic() if args.mode == "Classic" else Extended()
        try:
            mode.validate_grid(board)
        except ValueError as e:
            print("Некорректные данные: ", e)
        HitoriCLI.print_solution_by_args(board, mode, args.all)
    else:
        curses.wrapper(HitoriCLI.run)
