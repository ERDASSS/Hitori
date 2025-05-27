from __future__ import annotations


class Mode:
    NAME = "Mode"

    @staticmethod
    def read_grid_info(screen) -> None | tuple[int, int]:
        ...

    @staticmethod
    def display_input_info(screen):
        ...

    @staticmethod
    def validate_row(row: list[int], max_len = None):
        ...

    @staticmethod
    def validate_grid(grid: list[list[int]]):
        ...

    @staticmethod
    def get_neighbours() -> list:
        ...
