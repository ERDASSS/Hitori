from Source.Helpers.generator import Generator
from Source.Helpers.solver import Solver
import unittest


class TestHitoriGenerator(unittest.TestCase):
    def test_is_solvable(self):
        self.assertTrue(Generator.is_solvable([[1, 1], [1, 2]], False))
        self.assertFalse(Generator.is_solvable([[1, 2], [1, 2]], False))

    def test_is_valid(self):
        self.assertFalse(Solver.is_valid([['X', 1], ['X', 2]], False))
        self.assertFalse(Solver.is_valid([['X', 1], [1, 1]], False))
        # self.assertFalse(HitoriSolver.is_valid([['X', 1], [1, 'X']], False))
        self.assertTrue(Solver.is_valid([['X', 1], [1, 2]], False))

    def test_is_valid_extended(self):
        self.assertFalse(Solver.is_valid([['X', 1], ['X', 2], [2, 1]], True))
        self.assertFalse(Solver.is_valid([['X', 1], [1, 2], [2, 1]], True))
        self.assertFalse(Solver.is_valid([['X', 1], [1, 'X'], [2, 1]], True))
        self.assertTrue(Solver.is_valid([['X', 1], [1, 2], ['X', 3]], True))

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
                [4, 5, 2, 1, 5]], False))

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
                [4, 2, 3, 3]], False))

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
            ], True
            ))


if __name__ == '__main__':
    unittest.main()
