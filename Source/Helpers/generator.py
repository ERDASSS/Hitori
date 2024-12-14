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
    def _generate_constrained_grid(width, height, max_value):
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
    def is_solvable(grid, is_extended):
        # TODO: Хуйня какая-то. Уже же есть solver. Нахуя ещё тут такой метод
        """
        Проверяет, решаема ли данная сетка.
        """
        try:
            solutions = Solver.solve(grid, is_extended)

            if len(solutions) == 1:
                x_count = sum(row.count("X") for row in solutions[0])
                if x_count == 0:
                    return False

            return len(solutions) > 0
        except Exception as e:
            logging.debug(f"Solver error: {e}")
            return False

    @staticmethod
    def generate_grid(width, height, is_extended):
        """
        Генерирует решаемую сетку для Hitori.
        """
        logging.debug(f"generate_hitori_grid {width}, {height}, {is_extended}")
        # TODO: RECHECK
        max_value = max(width, height)
        logging.debug(f"max_value {max_value}")

        attempts = 0
        while attempts < Generator.MAX_ATTEMPTS:
            grid = Generator._generate_constrained_grid(width, height, max_value)
            logging.debug(f"Attempt {attempts + 1}: {grid}")

            if Generator.is_solvable(grid, is_extended):
                print(f"Сгенерирована решаемая сетка за {attempts + 1} попыток.")
                return grid

            attempts += 1

        raise Exception("Не удалось сгенерировать решаемую сетку за отведенное число попыток.")
