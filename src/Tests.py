import unittest

import Data

PRECISION = 5

class TestOddsConverter(unittest.TestCase):
    def test_american_positive(self):
        actual = Data.Odds("+175", "American").percent
        expected = 0.363636
        self.assertEqual(round(actual, PRECISION), round(expected, PRECISION))


    def test_american_negative(self):
        actual = Data.Odds("-225", fmt="American").percent
        expected = 0.692307
        self.assertEqual(round(actual, PRECISION), round(expected, PRECISION))

if __name__ == "__main__":
    unittest.main()
