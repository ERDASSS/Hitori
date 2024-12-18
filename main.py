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
            numbers = list(map(int, parts[0].split()))
            width = height = int(len(numbers) ** 0.5)
            board = [[numbers[i * width + j] for j in range(width)] for i in range(height)]

        return board
    except Exception as e:
        print("Некорректный формат доски. Убедитесь, что данные введены в одном из верных форматов.")
        sys.exit(1)


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
