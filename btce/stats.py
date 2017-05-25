#!/usr/bin/env python3

import datetime
import decimal
import os.path
import sys

import matplotlib.pyplot as plt
import pandas


OUTPUT_DIRECTORY = 'data'
QUANTIZE_VALUE = decimal.Decimal('0.0001')


def get_round_coeff(cols):
    return cols.down_amount / cols.up_amount if cols.end_price > cols.start_price else cols.up_amount / cols.down_amount


def is_guess_correct(cols):
    return (cols.start_price > cols.end_price and cols.down_bets > cols.up_bets) or (cols.start_price < cols.end_price and cols.down_bets < cols.up_bets)


def get_winrate(values):
    return sum(map(int, values)) / len(values)


def get_datetime(start_time):
    return datetime.datetime.strptime(start_time, '%Y-%m-%dT%H:%M:%SZ')


def get_date_from_datetime(start_time):
    return str(start_time.date())


def get_day_of_week_from_datetime(start_time):
    return start_time.weekday()


def get_hour_of_day_from_datetime(start_time):
    return start_time.hour


dataframe = pandas.read_csv(sys.argv[1])
dataframe['start_time'] = dataframe['start_time'].apply(get_datetime)

# Общая статистика:
dataframe['coeff'] = dataframe[['start_price', 'end_price', 'down_amount', 'up_amount']].apply(get_round_coeff, axis=1)
print('Среднее: %s. медиана: %s' % (dataframe['coeff'].mean(), dataframe['coeff'].median()))
axes = dataframe['coeff'].plot.hist(bins=1000)
axes.set_xlim((0, 8))
plt.savefig(os.path.join(OUTPUT_DIRECTORY, 'figure1.png'))

# Смотрим на большинство:
dataframe['is_guess_correct'] = dataframe[['start_price', 'end_price', 'down_bets', 'up_bets']].apply(is_guess_correct, axis=1)
print('Большинство угадывает: %s' % (len(dataframe[dataframe.is_guess_correct]) / len(dataframe)))

# Группировка по дням:
dataframe['start_day'] = dataframe['start_time'].apply(get_date_from_datetime)
grouped = dataframe.groupby('start_day')
grouped = grouped.aggregate({'is_guess_correct': get_winrate})
grouped.plot()
plt.savefig(os.path.join(OUTPUT_DIRECTORY, 'figure2.png'))

# Группировка по дням недели:
dataframe['start_week_day'] = dataframe['start_time'].apply(get_day_of_week_from_datetime)
grouped = dataframe.groupby('start_week_day')
grouped = grouped.aggregate({'is_guess_correct': get_winrate})
grouped.plot()
plt.savefig(os.path.join(OUTPUT_DIRECTORY, 'figure3.png'))

# Группировка по часам:
dataframe['hour'] = dataframe['start_time'].apply(get_hour_of_day_from_datetime)
grouped = dataframe.groupby('hour')
grouped = grouped.aggregate({'is_guess_correct': get_winrate})
grouped.plot()
plt.savefig(os.path.join(OUTPUT_DIRECTORY, 'figure4.png'))
