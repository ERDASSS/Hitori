from Source.Helpers.solver import Solver
from Source.Modes.Modes.classic import Classic
from Source.Modes.Modes.extended import Extended
from Source.hitori import HitoriCLI
from Source.Helpers.reader import Reader
import unittest

from unittest.mock import patch
import io

# Чтобы не ругался редактор
Classic = Classic()
Extended = Extended()


class TestHitoriGenerator(unittest.TestCase):
    def test_is_solvable(self):
        self.assertTrue(Solver.is_solvable([[1, 1], [1, 2]], Classic))
        self.assertFalse(Solver.is_solvable([[1, 2], [1, 2]], Classic))

    def test_is_valid(self):
        self.assertFalse(Solver.grid_is_valid([['X', 1], ['X', 2]], Classic))
        self.assertFalse(Solver.grid_is_valid([['X', 1], [1, 1]], Classic))
        self.assertTrue(Solver.grid_is_valid([['X', 1], [1, 2]], Classic))

    def test_is_valid_extended(self):
        self.assertFalse(Solver.grid_is_valid([['X', 1], ['X', 2], [2, 1]], Extended))
        self.assertFalse(Solver.grid_is_valid([['X', 1], [1, 2], [2, 1]], Extended))
        self.assertFalse(Solver.grid_is_valid([['X', 1], [1, 'X'], [2, 1]], Extended))
        self.assertTrue(Solver.grid_is_valid([['X', 1], [1, 2], ['X', 3]], Extended))

    def test_solve(self):
        self.assertEqual([
            [['X', 3, 'X', 4, 'X'],
             [3, 1, 4, 5, 2],
             [5, 2, 'X', 3, 4],
             ['X', 4, 3, 'X', 5],
             [4, 5, 2, 1, 'X']]],
            Solver.solve([
                [3, 3, 2, 4, 5],
                [3, 1, 4, 5, 2],
                [5, 2, 4, 3, 4],
                [5, 4, 3, 5, 5],
                [4, 5, 2, 1, 5]], Classic))

        self.assertEqual([
            [[3, 'X', 2, 'X'],
             [2, 4, 1, 3],
             ['X', 1, 'X', 4],
             [4, 2, 3, 'X']],
            [['X', 3, 2, 'X'],
             [2, 4, 1, 3],
             ['X', 1, 'X', 4],
             [4, 2, 3, 'X']],
            [['X', 3, 'X', 2],
             [2, 4, 1, 3],
             ['X', 1, 'X', 4],
             [4, 2, 3, 'X']]],
            Solver.solve([
                [3, 3, 2, 2],
                [2, 4, 1, 3],
                [1, 1, 4, 4],
                [4, 2, 3, 3]], Classic))

    def test_solve_extended(self):
        self.assertEqual(
            [[[4, 2, 3],
              ['X', 4, 'X'],
              [2, 3, 4],
              [1, 'X', 2]],
             [[4, 2, 3],
              [1, 'X', 2],
              [2, 3, 4],
              ['X', 4, 'X']]],
            Solver.solve([
                [4, 2, 3],
                [1, 4, 2],
                [2, 3, 4],
                [1, 4, 2]
            ], Extended
            ))

    def test_check_neighbours_classic(self):
        grid_false = [[1, 'X'], [2, 'X']]
        grid_true = [[1, 'X'], [2, 1]]
        self.assertFalse(Solver.check_neighbours(grid_false, Classic))
        self.assertTrue(Solver.check_neighbours(grid_true, Classic))

    def test_check_neighbours_extended(self):
        grid_false = [[1, 'X'], [2, 'X'], [3, 1]]
        grid_true = [[1, 'X'], [2, 1], [3, 2]]
        self.assertFalse(Solver.check_neighbours(grid_false, Classic))
        self.assertTrue(Solver.check_neighbours(grid_true, Classic))

    def test_is_connected(self):
        grid_false = [[1, 'X'], ['X', 2]]
        grid_true = [[1, 'X'], [2, 1]]
        grid_true_extended = [[1, 'X'], [2, 1], [3, 2]]
        grid_false_extended = [[1, 'X'], ['X', 2], [3, 1]]
        self.assertFalse(Solver.is_connected(grid_false))
        self.assertTrue(Solver.is_connected(grid_true))
        self.assertFalse(Solver.is_connected(grid_false_extended))
        self.assertTrue(Solver.is_connected(grid_true_extended))

    def test_solver_output_classic_3x3(self):
        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            HitoriCLI.print_solution_by_args([[4, 5, 5], [3, 5, 1], [4, 1, 1]], Classic, False)
            output = mock_stdout.getvalue()
            assert "4 X 5" in output
            assert "3 5 1" in output
            assert "X 1 X" in output

    def test_solver_output_classic_4x4_all(self):
        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            HitoriCLI.print_solution_by_args([[2, 1, 4, 3], [2, 4, 3, 1], [4, 4, 1, 2], [1, 2, 3, 1]], Classic, True)
            output = mock_stdout.getvalue()
            # Первое
            assert "X 1 4 3" in output
            assert "2 4 X 1" in output
            assert "4 X 1 2" in output
            assert "1 2 3 X" in output

            # Второе
            assert "X 1 4 3" in output
            assert "2 4 X 1" in output
            assert "4 X 1 2" in output
            assert "X 2 3 X" in output

            # Последнее
            assert "2 1 4 3" in output
            assert "X 4 X 1" in output
            assert "4 X 1 2" in output
            assert "1 2 3 X" in output

    def test_solver_output_extended_3x4_all(self):
        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            HitoriCLI.print_solution_by_args([
                [4, 2, 3],
                [1, 4, 2],
                [2, 3, 4],
                [1, 4, 2]
            ], Extended, True)
            output = mock_stdout.getvalue()
            # Первое
            assert "4 2 3" in output
            assert "X 4 X" in output
            assert "2 3 4" in output
            assert "1 X 2" in output

            # Последнее
            assert "4 2 3" in output
            assert "1 X 2" in output
            assert "2 3 4" in output
            assert "X 4 X" in output

    def test_parser_grid_for_args_spaces(self):
        grid_str = "4 2 3 1 4 2 2 3 4 1 4 2:3x4"
        grid = Reader.parse_board_by_arg(grid_str)
        expected_grid = [
            [4, 2, 3],
            [1, 4, 2],
            [2, 3, 4],
            [1, 4, 2]
        ]
        self.assertEqual(grid, expected_grid)

        grid_str = "2 1 4 3 2 4 3 1 4 4 1 2 1 2 3 1"
        grid = Reader.parse_board_by_arg(grid_str)
        expected_grid = [
            [2, 1, 4, 3],
            [2, 4, 3, 1],
            [4, 4, 1, 2],
            [1, 2, 3, 1]
        ]
        self.assertEqual(grid, expected_grid)

        grid_str = "2 1 4 3"
        grid = Reader.parse_board_by_arg(grid_str)
        expected_grid = [
            [2, 1],
            [4, 3],
        ]
        self.assertEqual(grid, expected_grid)

    def test_parser_grid_for_args_semicolons(self):
        grid_str = "4,5,5;3,5,1;4,1,1"
        grid = Reader.parse_board_by_arg(grid_str)
        expected_grid = [
            [4, 5, 5],
            [3, 5, 1],
            [4, 1, 1]
        ]
        self.assertEqual(grid, expected_grid)

        grid_str = "4,2,3;1,4,2;2,3,4;1,4,2"
        grid = Reader.parse_board_by_arg(grid_str)
        expected_grid = [
            [4, 2, 3],
            [1, 4, 2],
            [2, 3, 4],
            [1, 4, 2]
        ]
        self.assertEqual(grid, expected_grid)


if __name__ == '__main__':
    unittest.main()
