import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from Source.Modes.Modes.classic import Classic
from Source.Modes.Modes.extended import Extended
from Source.hitori import HitoriCLI
import unittest

from unittest.mock import patch
import io

# Чтобы не ругался редактор
Classic = Classic()
Extended = Extended()


class TestHitoriCLI(unittest.TestCase):
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


if __name__ == '__main__':
    unittest.main()
