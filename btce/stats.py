#!/usr/bin/env python3

import datetime
import decimal
import json
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas
from scipy import stats


QUANTIZE_VALUE = decimal.Decimal('0.0001')


def get_round_coeff(round):
    up_amount, down_amount = map(decimal.Decimal, round['amounts'])
    if round['end_price'] > round['start_price']:
        return (down_amount / up_amount).quantize(QUANTIZE_VALUE)
    return (up_amount / down_amount).quantize(QUANTIZE_VALUE)


# Общая статистика
if sys.argv[2] == '0':
    rounds = tuple(map(json.loads, open(sys.argv[1])))
    dataframe = pandas.DataFrame({
        'coeff': list(map(get_round_coeff, rounds))
    })
    dataframe = dataframe.astype(float)
    print('До отсечения: среднее: %s, медиана: %s' % (dataframe.mean().coeff, dataframe.median().coeff))
    # Отсекаем аномалии:
    dataframe = dataframe[(np.abs(stats.zscore(dataframe)) < 3).all(axis=1)]
    print('Среднее: %s. медиана: %s' % (dataframe.mean().coeff, dataframe.median().coeff))
    dataframe[['coeff']].plot.hist(bins=100)
    plt.show()

# Угадывает ли большинство
if sys.argv[2] == '1':
    def is_guess_correct(cols):
        if cols.start_price > cols.end_price and cols.down_bets > cols.up_bets:
            return True
        if cols.start_price < cols.end_price and cols.up_bets > cols.down_bets:
            return True
        return False
    dataframe = pandas.read_csv(sys.argv[1])
    dataframe['is_guess_correct'] = dataframe[['start_price', 'end_price', 'down_bets', 'up_bets']].apply(is_guess_correct, axis=1)
    print('Большинство угадывает: %s' % (len(dataframe[dataframe.is_guess_correct]) / len(dataframe)))
    # Группировка по дням:
    def get_date_from_datetime(cols):
        return str(datetime.datetime.strptime(cols.start_time, '%Y-%m-%dT%H:%M:%SZ').date())
    dataframe['start_day'] = dataframe[['start_time']].apply(get_date_from_datetime, axis=1)
    grouped = dataframe.groupby('start_day')
    grouped = grouped.aggregate({'is_guess_correct': lambda values: sum(filter(lambda value: value, values)) / len(values)})
    grouped.plot()
    plt.show()
    # Группировка по часам:
    def get_hour_of_day_from_datetime(cols):
        return datetime.datetime.strptime(cols.start_time, '%Y-%m-%dT%H:%M:%SZ').time().hour
    dataframe['hour'] = dataframe[['start_time']].apply(get_hour_of_day_from_datetime, axis=1)
    grouped = dataframe.groupby('hour')
    grouped = grouped.aggregate({'is_guess_correct': lambda values: sum(filter(lambda value: value, values)) / len(values)})
    grouped.plot()
    plt.show()
