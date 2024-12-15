from __future__ import annotations

from Source.Modes.Modes.classic import Classic
from Source.Modes.Modes.extended import Extended
from Source.Helpers.solver import Solver
import random
import logging

logging.basicConfig(
    filename="debug.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


class Generator:
    MAX_ATTEMPTS = 1000

    @staticmethod
    def _generate_constrained_grid(width: int, height: int, max_value: int) -> list[list[int]]:
        """
        Генерирует сетку с добавлением ограничений, чтобы уменьшить вероятность нерешаемости.
        """
        grid = [[0] * width for _ in range(height)]
        for i in range(height):
            for j in range(width):
                # Выбираем случайное число с учетом ограничений (ряд и колонка)
                possible_values = set(range(1, max_value + 1))
                if i > 0:
                    possible_values.discard(grid[i - 1][j])
                if j > 0:
                    possible_values.discard(grid[i][j - 1])

                grid[i][j] = random.choice(list(possible_values))

        return grid

    @staticmethod
    def generate_grid(width: int, height: int, mode: Classic | Extended) -> list[list[int]]:
        """
        Генерирует решаемую сетку для Hitori.
        """
        logging.debug(f"generate_hitori_grid {width}, {height}, {mode.NAME}")
        max_value = max(width, height)
        logging.debug(f"max_value {max_value}")

        attempts = 0
        while attempts < Generator.MAX_ATTEMPTS:
            grid = Generator._generate_constrained_grid(width, height, max_value)
            logging.debug(f"Attempt {attempts + 1}: {grid}")

            if Solver.is_solvable(grid, mode):
                print(f"Сгенерирована решаемая сетка за {attempts + 1} попыток.")
                return grid

            attempts += 1

        raise Exception("Не удалось сгенерировать решаемую сетку за отведенное число попыток.")
