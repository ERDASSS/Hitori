import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from Source.Helpers.reader import Reader
import unittest


class TestReader(unittest.TestCase):
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

    def test_parser_grid_for_args_wrong(self):
        with self.assertRaises(ValueError):
            Reader.parse_board_by_arg("1 2 3 4 5 6")  # Missing dimensions in space-separated format

        with self.assertRaises(ValueError):
            Reader.parse_board_by_arg("1 2 3 4 5 6 : 2x4")  # Mismatched elements and dimensions

        with self.assertRaises(ValueError):
            Reader.parse_board_by_arg("1,2;3,4,5")  # Irregular comma-separated format

        with self.assertRaises(ValueError):
            Reader.parse_board_by_arg("1 a 3 4 5 6 : 2x3")  # Non-integer input



if __name__ == '__main__':
    unittest.main()
