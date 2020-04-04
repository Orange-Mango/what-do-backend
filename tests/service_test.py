
from datetime import datetime
import unittest
from  whatdo import service

class ServiceTEst(unittest.TestCase):
    def test_calculate_score(self):
        date = datetime(2020, 4, 4, 2)
        newer_date = datetime(2020, 4, 4, 4)

        score = service.calculate_score(date, newer_date, 0.5)
        self.assertEqual(score, 0.5)

    def test_calculate_score_zero_diff(self):
        date = datetime(2020, 4, 4, 4)
        newer_date = datetime(2020, 4, 4, 4)

        score = service.calculate_score(date, newer_date, 0.5)
        self.assertEqual(score, 1)

    def test_calculate_score_one_day(self):
        date = datetime(2020, 4, 3, 4)
        newer_date = datetime(2020, 4, 4, 4)

        score = service.calculate_score(date, newer_date, 1)
        self.assertEqual(score, 0.04)
