import curses


class Display:
    @staticmethod
    def display_grid(screen, grid, cursor_row=-1, cursor_col=-1):
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
    def toggle_cell(grid, original_grid, row, col):
        """
        Закрашивает или снимает закраску с ячейки.
        """
        if grid[row][col] == "X":
            grid[row][col] = original_grid[row][col]
        else:
            grid[row][col] = "X"

    @staticmethod
    def display_solutions(screen, grid, solutions):
        """
        Отображает решения головоломки.
        """
        solution_index = 0
        while True:
            solution = solutions[solution_index]

            # Очищаем экран от предыдущего решения
            screen.clear()
            screen.addstr(0, 0, "Введенная головоломка:")
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
    def display_instructions(stdscr, is_extended):
        """
        Отображает инструкции для ввода головоломки.
        """
        stdscr.clear()
        if is_extended:
            stdscr.addstr(0, 0, "Введите головоломку строка за строкой, разделяя числа пробелами."
                                " Для завершения введите пустую строку:")
        else:
            stdscr.addstr(0, 0, "Введите головоломку строка за строкой, разделяя числа пробелами:")
        stdscr.refresh()
