from Source.Helpers.generator import Generator
from Source.Helpers.display import Display
from Source.Helpers.solver import Solver
from Source.States.state import State
import curses


class Interactive(State):
    @staticmethod
    def handle(screen, mode, height, width):
        try:
            grid = Generator.generate_grid(height, width, mode)
        except Exception as e:
            screen.addstr(1, 0, f"Ошибка генерации сетки: {str(e)}")
            screen.refresh()
            screen.getch()
            return False

        original_grid = [row[:] for row in grid]
        cursor_row, cursor_col = 0, 0

        while True:
            Display.display_grid(screen, grid, cursor_row, cursor_col)
            screen.addstr(len(grid) + 1, 0, "Используйте стрелки для перемещения, "
                                            "пробел для закрашивания/отмены, q для выхода в меню.", )
            screen.refresh()

            key = screen.getch()
            if key == curses.KEY_UP and cursor_row > 0:
                cursor_row -= 1
            elif key == curses.KEY_DOWN and cursor_row < len(grid) - 1:
                cursor_row += 1
            elif key == curses.KEY_LEFT and cursor_col > 0:
                cursor_col -= 1
            elif key == curses.KEY_RIGHT and cursor_col < len(grid[0]) - 1:
                cursor_col += 1
            elif key == ord(" "):
                Display.toggle_cell(grid, original_grid, cursor_row, cursor_col)
            elif key in (ord("q"), ord("Q"), ord("й"), ord("Й")):
                return True

            if Solver.grid_is_valid(grid, mode) and Solver.is_connected(grid):
                Display.display_grid(screen, grid, cursor_row, cursor_col)
                screen.addstr(len(grid) + 2, 0, "Поздравляем! Вы решили головоломку!")
                screen.refresh()
                screen.getch()
                return True
