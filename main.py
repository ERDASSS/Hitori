import logging
from grid_generator import HitoriGenerator
from solver import HitoriSolver

logging.basicConfig(
    filename="debug.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


import curses

def display_grid(stdscr, grid, cursor_row=-1, cursor_col=-1):
    """
    Отображение сетки на экране с подсветкой курсора.
    """
    stdscr.clear()
    for row_idx, row in enumerate(grid):
        for col_idx, cell in enumerate(row):
            # Подсветка ячейки под курсором
            if row_idx == cursor_row and col_idx == cursor_col:
                stdscr.attron(curses.A_REVERSE)

            # Отображение содержимого ячейки (с учетом символа "X")
            if cell == "X":
                stdscr.addstr(row_idx, col_idx * 2, str(cell), curses.A_BOLD | curses.A_REVERSE if row_idx == cursor_row and col_idx == cursor_col else curses.A_BOLD)
            else:
                stdscr.addstr(row_idx, col_idx * 2, str(cell))

            # Выключение подсветки
            if row_idx == cursor_row and col_idx == cursor_col:
                stdscr.attroff(curses.A_REVERSE)
    stdscr.refresh()


def toggle_cell(grid, original_grid, row, col):
    """
    Закрашивает или снимает закраску с ячейки.
    """
    if grid[row][col] == "X":
        grid[row][col] = original_grid[row][col]
    else:
        grid[row][col] = "X"

def interactive_mode(stdscr, is_extended, height, width):
    try:
        if is_extended:
            grid = HitoriGenerator.generate_hitori_grid(width, height, is_extended)
        else:
            grid = HitoriGenerator.generate_hitori_grid(width, width, is_extended)
    except Exception as e:
        stdscr.addstr(1, 0, f"Ошибка генерации сетки: {str(e)}")
        stdscr.refresh()
        stdscr.getch()
        return False

    original_grid = [row[:] for row in grid]
    cursor_row, cursor_col = 0, 0

    while True:
        display_grid(stdscr, grid, cursor_row, cursor_col)
        stdscr.addstr(
            len(grid) + 1,
            0,
            "Используйте стрелки для перемещения, пробел для закрашивания/отмены, q для выхода в меню.",
        )
        stdscr.refresh()

        key = stdscr.getch()
        if key == curses.KEY_UP and cursor_row > 0:
            cursor_row -= 1
        elif key == curses.KEY_DOWN and cursor_row < len(grid) - 1:
            cursor_row += 1
        elif key == curses.KEY_LEFT and cursor_col > 0:
            cursor_col -= 1
        elif key == curses.KEY_RIGHT and cursor_col < len(grid[0]) - 1:
            cursor_col += 1
        elif key == ord(" "):
            toggle_cell(grid, original_grid, cursor_row, cursor_col)
        elif key in (ord("q"), ord("Q"), ord("й"), ord("Й")):
            return True

        if HitoriSolver.is_valid(grid, is_extended) and HitoriSolver.is_connected(grid, is_extended):
            display_grid(stdscr, grid, cursor_row, cursor_col)
            stdscr.addstr(len(grid) + 2, 0, "Поздравляем! Вы решили головоломку!")
            stdscr.refresh()
            stdscr.getch()
            return True

def solve_mode(stdscr, is_extended):
    stdscr.clear()
    if is_extended:
        stdscr.addstr(0, 0, "Введите головоломку строка за строкой, разделяя числа пробелами. Для завершения введите пустую строку:")
    else:
        stdscr.addstr(0, 0, "Введите головоломку строка за строкой, разделяя числа пробелами:")
    stdscr.refresh()

    grid = []
    while True:
        stdscr.addstr(len(grid) + 1, 0, f"Строка {len(grid) + 1}: ")
        stdscr.refresh()

        row_input = ""
        cursor_pos = len(f"Строка {len(grid) + 1}: ")
        while True:
            key = stdscr.getch()
            if key in (10, 13):  # Enter
                break
            elif key in (8, 127, curses.KEY_BACKSPACE):  # Backspace
                if cursor_pos > len(f"Строка {len(grid) + 1}: "):
                    row_input = row_input[:-1]
                    cursor_pos -= 1
                    stdscr.addstr(len(grid) + 1, cursor_pos, " ")
                    stdscr.refresh()
            elif 48 <= key <= 57 or key == ord(" "):  # Цифры и пробелы
                row_input += chr(key)
                cursor_pos += 1
            stdscr.addstr(len(grid) + 1, len(f"Строка {len(grid) + 1}: "), row_input)
            stdscr.refresh()

        row = list(map(int, row_input.split()))
        logging.debug(f"num_count {len(row)}")
        if is_extended and row_input == "":
            break

        try:
            # row = list(map(int, row_input.split()))
            if grid and len(row) != len(grid[0]):
                raise ValueError("Все строки должны быть одной длины.")
            for num in row:
                if num > len(row) and not is_extended:
                    raise ValueError("Числа не должны превышать размер квадрата")
                if not is_extended and num <= 0:
                    raise ValueError("Числа должны быть больше 0")

            grid.append(row)
        except ValueError as e:
            stdscr.addstr(len(grid) + 2, 0, f"Ошибка ввода: {str(e)}")
            stdscr.refresh()
            stdscr.getch()
            return False  # Возвращаем False, чтобы указать, что режим завершился с ошибкой

        if len(grid) + 1 == len(row) + 1 and not is_extended:
            break

    if is_extended:
        max_width = len(grid[0])
        max_height = len(grid)
        # max_allowed = int(max(max_width, max_height) * 1.5)
        max_allowed = max(max_width, max_height)
        for row in grid:
            for num in row:
                if num > max_allowed:
                    stdscr.addstr(len(grid) + 3, 0,
                                  f"Число {num} превышает финальное допустимое значение {max_allowed}.")
                    stdscr.refresh()
                    stdscr.getch()
                    return False

    try:
        solutions = HitoriSolver.solve(grid, is_extended)
    except Exception as e:
        stdscr.addstr(len(grid) + 3, 0, f"Ошибка решения: {str(e)}")
        stdscr.refresh()
        stdscr.getch()
        return False  # Возвращаем False, чтобы указать, что режим завершился с ошибкой

    if len(solutions) == 0:
        stdscr.clear()
        stdscr.addstr(0, 0, "Введенная головоломка:")
        for row_idx, row in enumerate(grid):
            stdscr.addstr(row_idx + 1, 0, " ".join(map(str, row)))

        stdscr.addstr(len(grid) + 2, 0, "Решений нет. Нажмите любую клавишу для выхода.")
        stdscr.refresh()
        stdscr.getch()
        return False  # Возвращаем False, чтобы указать, что режим завершился с ошибкой

    solution_index = 0
    while True:
        solution = solutions[solution_index]

        # Очищаем экран от предыдущего решения
        stdscr.clear()
        stdscr.addstr(0, 0, "Введенная головоломка:")
        for row_idx, row in enumerate(grid):
            stdscr.addstr(row_idx + 1, 0, " ".join(map(str, row)))

        stdscr.addstr(len(grid) + 2, 0, f"Решение {solution_index + 1} из {len(solutions)}:")

        for row_idx, row in enumerate(solution):
            stdscr.addstr(len(grid) + 3 + row_idx, 0, " ".join(map(str, row)))

        stdscr.addstr(len(grid) + 3 + len(solution), 0, "Нажмите стрелки для навигации, q для выхода в меню.")
        stdscr.refresh()

        key = stdscr.getch()
        if key in (ord("q"), ord("Q"), ord("й"), ord("Й")):
            return True  # Возвращаем True, чтобы указать, что пользователь вышел в меню
        elif key == curses.KEY_LEFT:  # Стрелка вверх
            solution_index = max(0, solution_index - 1)
        elif key == curses.KEY_RIGHT:  # Стрелка вниз
            solution_index = min(len(solutions) - 1, solution_index + 1)

def main(stdscr):
    curses.curs_set(0)

    # Первое меню: выбор версии игры
    mode_menu = ["Hitori Classic", "Hitori Extended", "Выход"]
    # Основное меню
    main_menu = ["Интерактивный режим", "Решить головоломку", "Выход"]
    current_row = 0
    is_extended = False

    def print_menu(menu):
        """Функция для отображения меню."""
        stdscr.clear()
        for idx, item in enumerate(menu):
            if idx == current_row:
                stdscr.attron(curses.A_REVERSE)
                stdscr.addstr(idx, 0, item)
                stdscr.attroff(curses.A_REVERSE)
            else:
                stdscr.addstr(idx, 0, item)
        stdscr.refresh()

    # Меню выбора версии
    while True:
        print_menu(mode_menu)
        key = stdscr.getch()

        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(mode_menu) - 1:
            current_row += 1
        elif key in (10, 13):  # Enter
            if current_row == 0:
                is_extended = False
                break
            elif current_row == 1:
                is_extended = True
                break
            elif current_row == 2:
                return  # Выход из программы

    # Переход к основному меню
    current_row = 0  # Сброс текущей строки для основного меню
    while True:
        print_menu(main_menu)
        key = stdscr.getch()

        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(main_menu) - 1:
            current_row += 1
        elif key in (10, 13):  # Enter
            if current_row == 0:
                stdscr.clear()
                if is_extended:
                    stdscr.addstr(0, 0, "Введите ширину поля: ")
                    stdscr.refresh()

                    width_input = ""
                    while True:
                        key = stdscr.getch()
                        if key in (10, 13):  # Enter
                            break
                        elif key in (8, 127, curses.KEY_BACKSPACE):  # Backspace
                            if width_input:
                                width_input = width_input[:-1]
                                stdscr.addstr(0, len("Введите ширину поля: ") + len(width_input), " ")
                                stdscr.refresh()
                        elif 48 <= key <= 57:  # Цифры
                            width_input += chr(key)
                            stdscr.addstr(0, len("Введите ширину поля: "), width_input)
                            stdscr.refresh()

                    stdscr.addstr(1, 0, "Введите высоту поля: ")
                    stdscr.refresh()

                    height_input = ""
                    while True:
                        key = stdscr.getch()
                        if key in (10, 13):  # Enter
                            break
                        elif key in (8, 127, curses.KEY_BACKSPACE):  # Backspace
                            if height_input:
                                height_input = height_input[:-1]
                                stdscr.addstr(1, len("Введите высоту поля: ") + len(height_input), " ")
                                stdscr.refresh()
                        elif 48 <= key <= 57:  # Цифры
                            height_input += chr(key)
                            stdscr.addstr(1, len("Введите высоту поля: "), height_input)
                            stdscr.refresh()

                    try:
                        width = int(width_input)
                        height = int(height_input)
                        if width < 3 or height < 3 or width * height > 25 or height >= 10 or width >= 10:
                            raise ValueError("Ширина и высота должны быть > 2 и < 10 и площадь не должна превышать 25")
                    except ValueError as e:
                        stdscr.addstr(2, 0, f"Ошибка: {str(e)}")
                        stdscr.refresh()
                        stdscr.getch()
                        continue

                    if interactive_mode(stdscr, is_extended, height, width):
                        continue  # Возвращаемся в меню
                else:
                    stdscr.addstr(0, 0, "Введите размер поля [3;5]: ")
                    stdscr.refresh()

                    size_input = ""
                    while True:
                        key = stdscr.getch()
                        if key in (10, 13):  # Enter
                            break
                        elif key in (8, 127, curses.KEY_BACKSPACE):  # Backspace
                            if size_input:
                                size_input = size_input[:-1]
                                stdscr.addstr(0, len("Введите размер поля [3;5]: ") + len(size_input), " ")
                                stdscr.refresh()
                        elif 48 <= key <= 57:  # Цифры
                            size_input += chr(key)
                            stdscr.addstr(0, len("Введите размер поля [3;5]: "), size_input)
                            stdscr.refresh()

                    try:
                        size = int(size_input)
                        if size < 3 or size > 5:
                            raise ValueError("Размер поля должен быть в пределах [3;5]")
                    except ValueError as e:
                        stdscr.addstr(1, 0, f"Ошибка: {str(e)}")
                        stdscr.refresh()
                        stdscr.getch()
                        continue

                    if interactive_mode(stdscr, is_extended, size, size):
                        continue

            elif current_row == 1:
                if solve_mode(stdscr, is_extended):
                    continue  # Возвращаемся в меню
            elif current_row == 2:
                break  # Выход из программы

if __name__ == "__main__":
    curses.wrapper(main)