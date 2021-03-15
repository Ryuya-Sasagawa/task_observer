# ウィンドウAPI
from typing import Final
import tkinter as tk
from tkinter import ttk
# グラフAPI
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
import pandas as pd
import numpy as np
import matplotlib.dates as mdates
from typing import Final

import myDate

class Graph:
    BLANK_HOUR: Final[float] = 0.01
    def __init__(self):
        self.fig = plt.Figure()
        self.ax = self.fig.add_subplot(111)
        self.init()
        self.blank = self.BLANK_HOUR

    def init(self):
        self.ax.set_ylabel("minutes")
        self.ax.grid(axis='y', c='gainsboro', zorder=9)
        # days = mdates.HourLocator(byhour=range(0, 24, 1), tz=None)
        # daysFmt = mdates.DateFormatter('%d/%H')
        # days = mdates.DayLocator(bymonthday=None, interval=1, tz=None)
        # daysFmt = mdates.DateFormatter("%Y-%m-%d")
        days = mdates.MonthLocator(interval=1, tz=None)
        daysFmt = mdates.DateFormatter("%Y-%m")
        self.ax.xaxis.set_major_locator(days)
        self.ax.xaxis.set_major_formatter(daysFmt)

    def reset(self):
        self.ax.clear()
    def getax(self):
        return self.ax
    def getfig(self):
        return self.fig

    def relativeMove(self, dig):
        if self.ax.get_xlim()[0] + dig >= 0:
            self.ax.set_xlim(self.ax.get_xlim()[0] + dig, self.ax.get_xlim()[1] + dig)

    def absoluteMove(self, date):
        loc = myDate.datetimeToFloat(date)
        span = self.ax.get_xlim()[1] - self.ax.get_xlim()[0]
        if loc >= 0:
            self.ax.set_xlim(loc - self.blank, loc+span - self.blank)

    def relativeRange(self, span):
        if self.ax.get_xlim()[0] < self.ax.get_xlim()[1] + span:
            self.ax.set_xlim(self.ax.get_xlim()[0], self.ax.get_xlim()[1] + span)

    def absoluteRange(self, span):
        if span > 0:
            self.ax.set_xlim(self.ax.get_xlim()[0], self.ax.get_xlim()[0] + span)
