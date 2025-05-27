from __future__ import annotations

import curses

from Source.Modes.Modes.classic import Classic
from Source.Modes.Modes.extended import Extended
from Source.Modes.Modes.triangle import Triangle


class Display:
    @staticmethod
    def display_grid(screen, grid: list[list[int | str]], cursor_row=-1, cursor_col=-1):
        """
        Отображение сетки на экране с подсветкой курсора.
        """
        screen.clear()
        for row_idx, row in enumerate(grid):
            for col_idx, cell in enumerate(row):
                # Подсветка ячейки под курсором
                if row_idx == cursor_row and col_idx == cursor_col:
                    screen.attron(curses.A_REVERSE)

                # Отображение содержимого ячейки (с учетом символа "X")
                if cell == "X":
                    if row_idx == cursor_row and col_idx == cursor_col:
                        attr_for_chars = curses.A_BOLD | curses.A_REVERSE
                    else:
                        attr_for_chars = curses.A_BOLD
                    screen.addstr(row_idx, col_idx * 2, str(cell), attr_for_chars)
                else:
                    screen.addstr(row_idx, col_idx * 2, str(cell))

                # Выключение подсветки
                if row_idx == cursor_row and col_idx == cursor_col:
                    screen.attroff(curses.A_REVERSE)
        screen.refresh()

    @staticmethod
    def display_grid_triangle(screen, grid: list[list[int | str]], cursor_row=-1, cursor_col=-1):
        """
		Отображение сетки на экране с подсветкой курсора в форме треугольника.
		"""
        screen.clear()
        max_width = max(len(row) for row in grid)  # Определяем максимальную ширину строки для выравнивания

        for row_idx, row in enumerate(grid):
            row_offset = (max_width - len(row))  # Определяем отступ для выравнивания строк треугольника
            for col_idx, cell in enumerate(row):
                # Подсветка ячейки под курсором
                if row_idx == cursor_row and col_idx == cursor_col:
                    screen.attron(curses.A_REVERSE)

                # Вычисляем позицию символа с учётом отступов
                x_position = row_offset + col_idx * 2

                # Отображение содержимого ячейки (с учетом символа "X")
                if cell == "X":
                    if row_idx == cursor_row and col_idx == cursor_col:
                        attr_for_chars = curses.A_BOLD | curses.A_REVERSE
                    else:
                        attr_for_chars = curses.A_BOLD
                    screen.addstr(row_idx, x_position, str(cell), attr_for_chars)
                else:
                    screen.addstr(row_idx, x_position, str(cell))

                # Выключение подсветки
                if row_idx == cursor_row and col_idx == cursor_col:
                    screen.attroff(curses.A_REVERSE)
        screen.refresh()


    @staticmethod
    def toggle_cell(grid: list[list[int | str]], original_grid: list[list[int]], row: int, col: int):
        """
        Закрашивает или снимает закраску с ячейки.
        """
        if grid[row][col] == "X":
            grid[row][col] = original_grid[row][col]
        else:
            grid[row][col] = "X"

    @staticmethod
    def display_solutions(screen, grid: list[list[int | str]], solutions: list[list[list[int]]], mode: Classic | Extended | Triangle):
        """
        Отображает решения головоломки.
        """
        solution_index = 0
        while True:
            solution = solutions[solution_index]

            # Очищаем экран от предыдущего решения
            screen.clear()
            screen.addstr(0, 0, "Введенная головоломка:")
            if mode.NAME == "Triangle":
                for row_idx, row in enumerate(grid):
                    screen.addstr(row_idx + 1, len(grid[-1]) - row_idx + 1, " ".join(map(str, row)))

                screen.addstr(len(grid) + 2, 0, f"Решение {solution_index + 1} из {len(solutions)}:")

                for row_idx, row in enumerate(solution):
                    screen.addstr(len(grid) + 3 + row_idx, len(grid[-1]) - row_idx + 1, " ".join(map(str, row)))
            else:
                for row_idx, row in enumerate(grid):
                    screen.addstr(row_idx + 1, 0, " ".join(map(str, row)))

                screen.addstr(len(grid) + 2, 0, f"Решение {solution_index + 1} из {len(solutions)}:")

                for row_idx, row in enumerate(solution):
                    screen.addstr(len(grid) + 3 + row_idx, 0, " ".join(map(str, row)))

            screen.addstr(len(grid) + 3 + len(solution), 0, "Нажмите стрелки для навигации, q для выхода в меню.")
            screen.refresh()

            key = screen.getch()
            if key in (ord("q"), ord("Q"), ord("й"), ord("Й")):
                return True  # Возвращаем True, чтобы указать, что пользователь вышел в меню
            elif key == curses.KEY_LEFT:  # Стрелка влево
                solution_index = max(0, solution_index - 1)
            elif key == curses.KEY_RIGHT:  # Стрелка вправо
                solution_index = min(len(solutions) - 1, solution_index + 1)

    @staticmethod
    def display_instructions(screen, mode):
        """
        Отображает инструкции для ввода головоломки.
        """
        screen.clear()
        mode.display_input_info(screen)
        screen.refresh()
