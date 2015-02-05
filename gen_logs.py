import uuid
import numpy as np
import math
from datetime import datetime, timedelta


def main():
    """
    This saves lines of log in the csv file.
    :return: a csv file
    """
    gen_logs = make_multiple_cid_logs(1000, '2015-01-01', '2015-02-28', 2, .1)
    with open('./fake_logs.csv', 'w') as f:
        for gen_cid in gen_logs:
            for line in gen_cid:
                f.write(','.join(line) + '\n')


def make_multiple_cid_logs(cnt, start_date, end_date, beta, increment=0):
    """
    This makes lines of log for multiple id.
    :param cnt: int, the number of ids
    :param start_date: str, the start date of time window
    :param end_date: str, the end date of time window
    :param beta: float, the parameter for exponential distribution in the 'time_lapse' function
    :param increment: float, the parameter for normal distribution in the 'time_increment' function
    :return: generator having generator of lines of log for single ids
    """
    list_id = gen_id(cnt)
    start_date, end_date = time_window(start_date, end_date)
    for cid in list_id:
        yield make_single_cid_logs(cid, start_date, end_date, beta, increment)


def gen_id(cnt_id):
    """
    This generates the number of ids.
    :param cnt_id: int, the number of ids.
    :return: generator having ids.
    """
    while cnt_id > 0:
        yield str(uuid.uuid4())
        cnt_id -= 1


def time_window(start_date, end_date):
    """
    This convert date strings into datetime objects.
    :param start_date:
    :param end_date:
    :return:
    """
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')
    return start_date, end_date


def make_single_cid_logs(cid, start_date, end_date, beta, increment=0):
    """
    This makes lines of log for one id.
    :param cid:
    :param start_date:
    :param end_date:
    :param beta: float > 0, the parameter for exponential distribution in the 'time_lapse' function.
    :param increment: float, the parameter for normal distribution in the 'time_increment' function.
    :return:
    """
    start_date += timedelta(days=time_lapse(0.1))
    while start_date < end_date:
        yield cid, start_date.strftime('%Y-%m-%d %H:%M:%S.%f'), str(beta)
        start_date += timedelta(days=time_lapse(beta))
        beta = max(1, beta + time_increment(increment))


def time_lapse(beta):
    """
    This makes time lapse which means interval time between the last log and the next log.
    Time lapse is sampled from exponential distribution with beta.
    The value of beta means the mean of time before the next Poisson-typed event occurs.
    :param beta: float > 0
    :return: float > 0
    """
    return float(np.random.exponential(beta, 1))


def time_increment(increment):
    """
    This makes the increment of beta for exponential distribution.
    If this value is plus, the time lapse is getting longer, and vice versa.
    :param increment: float
    :return: float
    """
    if increment == 0:
        return 0
    else:
        return math.copysign(1, increment) * abs(float(np.random.normal(0, abs(increment), 1)))

if __name__ == '__main__':
    main()
