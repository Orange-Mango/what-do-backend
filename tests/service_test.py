from  whatdo import service
from datetime import datetime
import unittest

class ServiceTEst(unittest.TestCase):
    def testCalculateScore(self):
        date = datetime(2020,4,4,2)
        newerDate = datetime(2020,4,4,4)

        score = service.calculate_score(date,newerDate, 0.5)
        self.assertEqual(score,0.5)

    def testCalculateScoreZeroDiff(self):
        date = datetime(2020,4,4,4)
        newerDate = datetime(2020,4,4,4)

        score = service.calculate_score(date,newerDate, 0.5)
        self.assertEqual(score,1)

    def testCalculateScoreOneDay(self):
        date = datetime(2020,4,3,4)
        newerDate = datetime(2020,4,4,4)

        score = service.calculate_score(date,newerDate, 1)
        self.assertEqual(score,0.04)
