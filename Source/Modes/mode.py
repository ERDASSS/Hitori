from __future__ import annotations


class Mode:
    NAME = "Mode"

    @staticmethod
    def read_grid_info(screen) -> None | tuple[int, int]:
        ...

    @staticmethod
    def display_input_info(screen):
        ...