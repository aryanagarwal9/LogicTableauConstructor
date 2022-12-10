import os
import unittest
from parameterized import parameterized
from tableau import *


class TestTail(unittest.TestCase):
    @parameterized.expand([
        ['-(p>(q>p))', 0],
        ['(-(p>q)^q)', 0],
        ['(---pv(q^-q))', 1],
        ['(p>p)', 1],
        ['-(p>p)', 0],
        ['((pvq)^', -1],
        ['(p-q)', -1],
        ['((pvq)^(-pv-q))', 1],
        ['(q^-(pv-p))', 0],
        ['p', 1],
        ['((pvq)^((p>-p)^(-p>p)))', 0],
        ['-----------q', 1]
        ])
    def test_sat(self, line, result):
        parsed = parse(line)
        if parsed:
            tableau = [theory(line)]
            self.assertEqual(sat(tableau), result)
        else:
            self.assertEqual(-1, result)


if __name__ == '__main__':
    unittest.main()
