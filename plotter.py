#!/usr/bin/env python3

import argparse
import io
import sqlite3
import sys
import datetime as dt
import dateutil.parser
import pandas
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from scipy import interpolate
from scipy.ndimage.filters import gaussian_filter1d

# Plots scatter series data. On top of that it adds:
# 1. Filter to plot smooth data
# 2. Linear regression
def plotSeries(ax, name, dates, values):
    timestamps = [x.timestamp() for x in dates]
    x = np.array(timestamps).reshape((-1, 1))
    y = np.array(values)
    model = LinearRegression().fit(x, y)
    y_pred_0 = model.predict(np.array([timestamps[0]]).reshape((-1, 1)))[0]
    y_pred_1 = model.predict(np.array([timestamps[-1]]).reshape((-1, 1)))[0]
    ax.scatter(dates, values, label=name, marker='x')

    # Spline
    # interp = interpolate.interp1d(timestamps, values, 'quadratic')
    # new_timestamps = np.linspace (timestamps[0], timestamps[-1], num = 500, endpoint = True)
    # new_dates = [dt.datetime.fromtimestamp(ts) for ts in new_timestamps]
    # interp_weights = interp(new_timestamps)
    # ax.plot(new_dates, interp_weights, label=name, linewidth=2)

    # Gaussian filter for smooth data
    weight_smoothed = gaussian_filter1d(values, sigma=1)
    ax.plot(dates, weight_smoothed, label="Smooth {}".format(name), linewidth=2)

    ax.plot([dates[0], dates[-1]], [y_pred_0, y_pred_1], label='Prediction {}'.format(name), linestyle='--', linewidth=1)

# Supports two units: mmol/L (SI) and mg/dL.
# Tries to guess data unit and plots two axies.
def lipidPlot(df, name, value_column, mmolPerL_TO_mgPerdL, date_column = 0):
    dates=[dateutil.parser.parse(x) for x in df.iloc[:, date_column].values]
    values = df.iloc[:, value_column].values
    if len(values) == 0:
        return
    # Guess units
    if values[0] > 20:
        valuesMgPerDL = values
        valuesMmolPerL = [x / mmolPerL_TO_mgPerdL for x in values]
    else:
        valuesMmolPerL = values
        valuesMgPerDL = [x * mmolPerL_TO_mgPerdL for x in values]

    ax1 = plt.subplot()
    plotSeries(ax1, name, dates, valuesMmolPerL)
    ax1.set_ylabel('mmol/L')
    # second Unit axis
    ax2 = ax1.twinx()
    mn, mx = ax1.get_ylim()
    ax2.set_ylim(mn * mmolPerL_TO_mgPerdL, mx * mmolPerL_TO_mgPerdL)
    ax2.set_ylabel('mg/dL')

    ax1.legend()
    plt.show()

# Plot single simple plot
def singlePlot(df, name, label, value_column, date_column = 0):
    dates=[dateutil.parser.parse(x) for x in df.iloc[:, date_column].values]
    values = df.iloc[:, value_column].values
    if len(values) == 0:
        return

    ax1 = plt.subplot()
    plotSeries(ax1, name, dates, values)
    ax1.set_ylabel(label)
    ax1.legend()
    plt.show()

def bloodPressurePlot(df, sys_column, dia_column, date_column = 0):
    dates=[dateutil.parser.parse(x) for x in df.iloc[:, date_column].values]
    sys_values = df.iloc[:, sys_column].values
    dia_values = df.iloc[:, dia_column].values

    ax1 = plt.subplot()
    plotSeries(ax1, "BP SYS", dates, sys_values)
    plotSeries(ax1, "BP DIA", dates, dia_values)
    ax1.set_ylabel('mmHg')
    ax1.legend()
    plt.show()

parser = argparse.ArgumentParser(description='Health plotter')
parser.add_argument('csv_file', type=str, help='CSV file with data')
parser.add_argument('--ldl', type=int, help='Column in a csv file with LDL cholesterol')
parser.add_argument('--hdl', type=int, help='Column in a csv file with HDL cholesterol')
parser.add_argument('--chol', type=int, help='Column in a csv file with Total cholesterol')
parser.add_argument('--trig', type=int, help='Column in a csv file with Triglycerides')
parser.add_argument('--weight', type=int, help='Column in a csv file with Weight')
parser.add_argument('--bpm', type=int, help='Column in a csv file with BPM (heart rate)')
parser.add_argument('--bp', metavar="SYS,DIA", help='Columns in a csv file with systolic and diastolic blood pressures')
parser.add_argument('--verbose', action='store_true', help='Print head of read file')

args = parser.parse_args()

df = pandas.read_csv(args.csv_file)
if args.verbose:
    print(df.head())

if args.ldl:
    lipidPlot(df, "LDL", args.ldl, 38.66976)
if args.hdl:
    lipidPlot(df, "HDL", args.hdl, 38.66976)
if args.chol:
    lipidPlot(df, "CHOL", args.chol, 38.66976)
if args.trig:
    lipidPlot(df, "TRIG", args.trig, 88.57396)
if args.weight:
    singlePlot(df, "Weight", "kg", args.weight)
if args.bpm:
    singlePlot(df, "BPM", "1/min", args.bpm)
if args.bp:
    items = args.bp.split(',')
    if len(items) != 2:
        raise ValueError('Cannot parse blood pressure columns')
    bloodPressurePlot(df, int(items[0]), int(items[1]))
        
