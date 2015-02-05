import unittest
import statistics
from gen_logs import *


class MyTestCase(unittest.TestCase):
    def test_make_id(self):
        test_cnt = 100
        actual = list(gen_id(test_cnt))
        self.assertEqual(test_cnt, len(set(actual)))

    def test_time_window(self):
        test_start_date = '2014-01-01'
        test_end_date = '2014-01-10'
        actual = time_window(test_start_date, test_end_date)
        actual_start_date = actual[0].strftime('%Y-%m-%d')
        actual_end_date = actual[1].strftime('%Y-%m-%d')
        self.assertEqual(test_start_date, actual_start_date)
        self.assertEqual(test_end_date, actual_end_date)

    def test_time_lapse(self):
        test_beta = 2
        actual = [time_lapse(test_beta) for _ in range(10000)]
        actual_mean = statistics.mean(actual)
        actual_variance = statistics.variance(actual)
        self.assertAlmostEqual(test_beta, actual_mean, 0)
        self.assertAlmostEqual(test_beta ** 2, actual_variance, 0)

    def test_make_log(self):
        test_id = next(gen_id(1))
        test_start_date = '2015-01-01'
        test_end_date = '2015-01-31'
        test_start_date, test_end_date = time_window(test_start_date, test_end_date)
        test_beta = 2
        actual = list(make_single_cid_logs(test_id, test_start_date, test_end_date, test_beta))
        self.assertLessEqual(test_start_date, datetime.strptime(actual[0][1], '%Y-%m-%d %H:%M:%S.%f'))
        self.assertGreaterEqual(test_end_date, datetime.strptime(actual[-1][1], '%Y-%m-%d %H:%M:%S.%f'))



if __name__ == '__main__':
    unittest.main()
