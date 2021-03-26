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
    def __init__(self, onclick):
        self.fig = plt.Figure()
        self.ax = self.fig.add_subplot(111)
        self.init()
        self.blank = 0
        self.barwidth = 0
        self.onclick = onclick

    def init(self, ylabel='minutes', ylim=62, barset='1h'):
        self.ax.set_ylabel(ylabel)
        self.ax.set_ylim(0, ylim)
        self.ax.grid(axis='y', c='gainsboro', zorder=9)
        barsetDict = {'1h': 1, '3h': 2, '6h': 3, '12h': 4, '1d': 5, '1w': 6, '1m': 7}
        self._locator(barsetDict[barset])
        self.annot = self.ax.annotate("", xy=(0, 0), xytext=(20, 20), textcoords="offset points",
                                      bbox=dict(boxstyle="round", fc="w"), arrowprops=dict(arrowstyle="->"),
                                      fontname="MS Gothic")
        self.annot.set_visible(False)

    def _locator(self, type):
        if type == 1:
            major = mdates.HourLocator(byhour=range(0, 24, 3), tz=None)
            majorFmt = mdates.DateFormatter('%m/%d\n%H:00')
            minor = mdates.HourLocator(byhour=range(0, 24, 1), tz=None)
        elif type == 2:
            major = mdates.HourLocator(byhour=range(0, 24, 6), tz=None)
            majorFmt = mdates.DateFormatter('%m/%d\n%H:00')
            minor = mdates.HourLocator(byhour=range(0, 24, 3), tz=None)
        elif type == 3:
            major = mdates.HourLocator(byhour=range(0, 24, 12), tz=None)
            majorFmt = mdates.DateFormatter('%m/%d\n%H:00')
            minor = mdates.HourLocator(byhour=range(0, 24, 6), tz=None)
        elif type == 4:
            major = mdates.DayLocator(interval=1, tz=None)
            majorFmt = mdates.DateFormatter('%Y\n%m/%d')
            minor = mdates.HourLocator(byhour=range(0, 24, 12), tz=None)
        elif type == 5:
            major = mdates.DayLocator(interval=1, tz=None)
            majorFmt = mdates.DateFormatter('%Y\n%m/%d')
            minor = mdates.DayLocator(interval=1, tz=None)
        elif type == 6:
            major = mdates.WeekdayLocator(byweekday=mdates.SUNDAY, tz=None)
            majorFmt = mdates.DateFormatter('%Y\n%m/%d')
            minor = mdates.WeekdayLocator(byweekday=mdates.SUNDAY, tz=None)
        elif type == 7:
            major = mdates.MonthLocator(interval=1, tz=None)
            majorFmt = mdates.DateFormatter('%Y/%m')
            minor = mdates.MonthLocator(interval=1, tz=None)
        self.ax.xaxis.set_major_locator(major)
        self.ax.xaxis.set_major_formatter(majorFmt)
        self.ax.xaxis.set_minor_locator(minor)

    def annotation(self, text, x, y):
        # print(text, x, y)
        self.annot.set_text(text)
        self.annot.xy = (x,y)
        self.annot.set_visible(True)

    def hideannot(self):
        self.annot.set_visible(False)

    def plotbar(self, x, worklist, width, per='min'):
        self.barwidth = width
        perDict = {'sec':1, 'min':60, 'hour':3600}
        base = 0
        for w in worklist[1].getworklist():
            # print(w[1].getdata()[0].total_seconds()/60)
            time = w[1].getdata()[0].total_seconds() / perDict[per]
            self.ax.bar(x, time, bottom=base, align='edge', width=width)  # データの描画
            base += time

    def reset(self):
        self.ax.clear()
    def getax(self):
        return self.ax
    def getfig(self):
        return self.fig

    def relativeMove(self, dig):
        if self.ax.get_xlim()[0] + dig >= 0:
            self.ax.set_xlim(self.ax.get_xlim()[0] + dig, self.ax.get_xlim()[1] + dig)

    def absoluteMove(self, date, blank=-1):
        loc = myDate.datetimeToFloat(date)
        span = self.ax.get_xlim()[1] - self.ax.get_xlim()[0]
        if loc >= 0:
            if blank >= 0:
                self.blank = blank
            self.ax.set_xlim(loc - self.blank, loc+span - self.blank)

    # TODO: 描画範囲を広げた時、目盛りのラベルが重ならないようにする。且つ最大限詳細までラベルを表示する
    def relativeRange(self, span):
        if self.ax.get_xlim()[0] + self.barwidth + self.blank < self.ax.get_xlim()[1] + span:
            self.ax.set_xlim(self.ax.get_xlim()[0], self.ax.get_xlim()[1] + span)
            return True
        return False

    def absoluteRange(self, span):
        if span > 0:
            self.ax.set_xlim(self.ax.get_xlim()[0], self.ax.get_xlim()[0] + span)

    def pack(self, master):
        self.canvas = FigureCanvasTkAgg(self.fig, master=master)
        self.canvas.mpl_connect("motion_notify_event", self.onclick)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side='left', fill=tk.BOTH, expand=1)

    def rewrite(self):
        self.canvas.mpl_connect("motion_notify_event", self.onclick)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side='left', fill=tk.BOTH, expand=1)
