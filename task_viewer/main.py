import sys
# ウィンドウAPI
from typing import Final
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
# グラフAPI
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
import pandas as pd
import numpy as np
import matplotlib.dates as mdates
# 自作プログラム
import readData, graph, myDate

# -----定数-----
HOUR_LENGTH: Final[float] = 1 / 24
HALFDAY_LENGTH: Final[float] = 1 / 2
DAY_LENGTH: Final[int] = 1
WEEK_LENGTH: Final[int] = 7
MONTH_LENGTH: Final[int] = 30
YEAR_LENGTH: Final[int] = 365
PASSWORD: Final[str] = 'OiC&0~ktz1%i4nUg1ZodLM+XUPf(f|E9ez_vys9p'
FILEPATH: Final[str] = '../data/applicationLog'

# -----初期設定-----
scroll_length = HOUR_LENGTH
span = HALFDAY_LENGTH
barset = '1h'

# -----ウィンドウ設定-----
root = tk.Tk()
root.title('Task Checker')
root.geometry("800x600")
root.minsize(width=800, height=600)

# -----パーツ設定-----
# タブ
nb = ttk.Notebook(root)
graphTab = tk.Frame(nb)
tableTab = tk.Frame(nb)
nb.add(graphTab, text='グラフ')
nb.add(tableTab, text='表')
# グラフ設定
frame = tk.Frame(graphTab, background='gray', height=50)

# グラフ設定：日時
dateFrame = tk.Frame(frame, background='white', height=50)
dateLabel = tk.Label(dateFrame, text='日時', font=12)


# グラフ設定：日時：共用関数
def baserestrict(i, S, lim):
    if int(i) >= int(lim) or not S.isdecimal():
        return False
    return True


# TODO: 公開するときには、例外(2020/13/32など)を入力できないようにしたい
def enterevent(entry):
    entry.focus_set()
    if 'select_range' in dir(entry):
        entry.select_range(0, len(entry.get()))


vcmd1 = (dateFrame.register(baserestrict), '%i', '%S', 4)
vcmd2 = (dateFrame.register(baserestrict), '%i', '%S', 2)

# グラフ設定：日時：from：年
year = tk.Entry(dateFrame, width=4, validatecommand=vcmd1, font=('', 15, 'bold'), validate='key')
year.bind('<Return>', lambda event: enterevent(month))
slashLabel = tk.Label(dateFrame, text='/', font=12)
# グラフ設定：日時：from：月
month = tk.Entry(dateFrame, width=2, validatecommand=vcmd2, font=('', 15, 'bold'), validate='key')
slashLabel2 = tk.Label(dateFrame, text='/', font=12)
month.bind('<Return>', lambda event: enterevent(day))
# グラフ設定：日時：from：日
day = tk.Entry(dateFrame, width=2, validatecommand=vcmd2, font=('', 15, 'bold'), validate='key')
minusLabel = tk.Label(dateFrame, text='-', font=12)
day.bind('<Return>', lambda event: enterevent(hour))
# グラフ設定：日時：from：時
hour = tk.Entry(dateFrame, width=2, validatecommand=vcmd2, font=('', 15, 'bold'), validate='key')
restLabel = tk.Label(dateFrame, text=':00:00', font=12)
hour.bind('<Return>', lambda event: enterevent(year2))

# グラフ設定：日時：～
tildeLabel = tk.Label(dateFrame, text='～', font=12)
# グラフ設定：日時：to：年
year2 = tk.Entry(dateFrame, width=4, validatecommand=vcmd1, font=('', 15, 'bold'), validate='key')
year2.bind('<Return>', lambda event: enterevent(month2))
slashLabel3 = tk.Label(dateFrame, text='/', font=12)
# グラフ設定：日時：to：月
month2 = tk.Entry(dateFrame, width=2, validatecommand=vcmd2, font=('', 15, 'bold'), validate='key')
slashLabel4 = tk.Label(dateFrame, text='/', font=12)
month2.bind('<Return>', lambda event: enterevent(day2))
# グラフ設定：日時：to：日
day2 = tk.Entry(dateFrame, width=2, validatecommand=vcmd2, font=('', 15, 'bold'), validate='key')
minusLabel2 = tk.Label(dateFrame, text='-', font=12)
day2.bind('<Return>', lambda event: enterevent(hour2))
# グラフ設定：日時：to：時
hour2 = tk.Entry(dateFrame, width=2, validatecommand=vcmd2, font=('', 15, 'bold'), validate='key')
restLabel2 = tk.Label(dateFrame, text=':00:00', font=12)
hour2.bind('<Return>', lambda event: enterevent(date_btn))


# グラフ設定：日時：ボタン
def move():
    d = year.get(), month.get(), day.get(), hour.get(), \
        year2.get(), month2.get(), day2.get(), hour2.get()
    flag = True
    for i in d:
        if not i.isdecimal():
            flag = False

    if flag is True:
        # TODO: datetimeに変換して比較する。graph.absolutemoveなどは、strftime関数で年月日を渡す
        d = list(map(int, d))
        if 1970 <= d[0] <= 2500 and 1970 <= d[4] <= 2500:
            if 1 <= d[1] <= 12 and 1 <= d[5] <= 12:
                if 1 <= d[2] <= myDate.lastdate(d[0], d[1]) and \
                        1 <= d[6] <= myDate.lastdate(d[4], d[5]):
                    if 0 <= d[3] <= 23 and 0 <= d[7] <= 23:
                        if d[0] < d[4] or \
                                (d[0] == d[4] and d[1] < d[5]) or \
                                (d[0] == d[4] and d[1] == d[5] and d[2] < d[6]) or \
                                (d[0] == d[4] and d[1] == d[5] and d[2] == d[6] and d[3] < d[7]):
                            # print(year.get() + '/' + month.get() + '/' + day.get() + '-' + hour.get() + ':00:00')
                            d = list(map(str, d))
                            graph.absoluteMove(d[0] + '-' + d[1] + '-' + d[2] + ' ' + d[3])
                            graph.absoluteRange(myDate.datetimeToFloat(d[4]+'-'+d[5]+'-'+d[6]+' '+d[7]) -
                                                myDate.datetimeToFloat(d[0]+'-'+d[1]+'-'+d[2]+' '+d[3]))
                            graph.rewrite()
                            return
                    messagebox.showerror('エラー', '範囲が正しくありません。')
                    return
    messagebox.showerror('エラー', '日付が正しくありません。')


date_btn = tk.Button(master=dateFrame, text='MOVE', command=move)
date_btn.bind('<Return>', lambda event: move())

# グラフ設定：棒グラフ
barFrame = tk.Frame(frame, background='white', height=50)
barLabel = tk.Label(barFrame, text='棒グラフ', font=12)

# 一本の棒グラフで表す期間を変更する関数
# def getBarSpan():
#     if 「棒グラフ」のコンボボックスが変更されたら:
#         barset = barFormat.get()
#         reformedList = readData.reform(graphDataList, barset)
#         graph.reset()
#         graph.init(y_label=labelList(barset), locator=locatorList(barset))
#         ~~~
#             ax.barでグラフを追加
#         ~~~
#         graph.rewrite()
#         span = spanList(barset)
# TODO: 上記のプログラムを実装する。
#   また、barset毎にグラフ1本の横幅とspan(barset=1h:1/24, 3h:1/8, 1d:1...)を変更する
def getBarSpan():
    # print(barFormat.get())
    global barset, scroll_length, span
    if barset != barFormat.get():
        barset = barFormat.get()
        reformedList = readData.reform(graphDataList, barset)
        print(reformedList)
        # graph.relativeMove(span / 2)
        # if barset == '1h':
        #     scroll_length = HOUR_LENGTH
        #     span = HALFDAY_LENGTH
        # elif barset == '3h':
        #     scroll_length = HOUR_LENGTH
        #     span = DAY_LENGTH
        # elif barset == '6h':
        #     scroll_length = HALFDAY_LENGTH
        #     span = DAY_LENGTH
        # elif barset == '12h':
        #     scroll_length = HALFDAY_LENGTH
        #     span = WEEK_LENGTH
        # elif barset == '1d':
        #     scroll_length = DAY_LENGTH
        #     span = WEEK_LENGTH
        # elif barset == '1w':
        #     scroll_length = WEEK_LENGTH
        #     span = MONTH_LENGTH
        # elif barset == '1m':
        #     scroll_length = MONTH_LENGTH
        #     span = YEAR_LENGTH
        # print(barset)
        # graph.absoluteRange(span)
        # graph.relativeMove(-span / 2)

    return True


vcmd3 = (dateFrame.register(getBarSpan))
barFormat = ttk.Combobox(barFrame, state='readonly', width=5, font=12, validatecommand=vcmd3, validate='focusin')
barFormat["values"] = ("1h", "3h", "6h", "12h", "1d", "1w", "1m")
barFormat.current(0)
perLabel = tk.Label(barFrame, text='毎', font=12)

# グラフ設定：横幅
widthFrame = tk.Frame(frame, background='white', height=50)
widthLabel = tk.Label(widthFrame, text='グラフの幅', font=12)
widthFormat = ttk.Combobox(widthFrame, state='readonly', width=5, font=12)
widthFormat["values"] = ("12h", "day", "week", "month", "year")
widthFormat.current(0)


def changeRange(sp):
    graph.relativeRange(sp)
    graph.rewrite()

# TODO:矢印は画像に差し替える
narrow_btn = tk.Button(master=widthFrame, text='→←', command=lambda: changeRange(-span))
wide_btn = tk.Button(master=widthFrame, text='←→', command=lambda: changeRange(span))


# グラフ設定：移動ボタン
# TODO:矢印は画像に差し替える
def locate(sclen):
    graph.relativeMove(sclen)
    graph.rewrite()


left_btn = tk.Button(master=graphTab, text='←', command=lambda: locate(-scroll_length))
right_btn = tk.Button(master=graphTab, text='→', command=lambda: locate(scroll_length))

# グラフ
graph = graph.Graph()
graphDataList = readData.parseData(FILEPATH, PASSWORD)

for wl in graphDataList:  # graphDataListをグラフに描画
    # print(wl[0])
    x = pd.DatetimeIndex([wl[0] + ':00:00'])
    base = 0
    for w in wl[1].getworklist():
        # print(w[1].getdata()[0].total_seconds()/60)
        time = w[1].getdata()[0].total_seconds() / 60
        graph.getax().bar(x, time, bottom=base, align='edge', width=0.03)  # データの描画
        base += time

graph.absoluteRange(span)  # TODO: spanとは別の変数を使用する？(spanは本来ボタンクリックで変化する幅の変数)
graph.absoluteMove(graphDataList[-1][0])
graph.relativeMove(-(span / 2))
reformedlist = readData.reform(graphDataList[6:8], '6h')

for wl in reformedlist:
    print(wl[0])
    for w in wl[1].getworklist():
        print('  ', w[0], w[1].getdata())

for wl in graphDataList:
    print(wl[0])
    for w in wl[1].getworklist():
        print('  ', w[0], w[1].getdata())

# -----レイアウト生成-----
# タブ
nb.pack(fill='both', expand=1)
# グラフ設定
frame.pack(fill=tk.BOTH, padx=20)
# 日時
dateFrame.pack(side='left', expand=True)
dateLabel.pack(side='left')
year.pack(side='left')
slashLabel.pack(side='left')
month.pack(side='left')
slashLabel2.pack(side='left')
day.pack(side='left')
minusLabel.pack(side='left')
hour.pack(side='left')
restLabel.pack(side='left')
tildeLabel.pack(side='left')
year2.pack(side='left')
slashLabel3.pack(side='left')
month2.pack(side='left')
slashLabel4.pack(side='left')
day2.pack(side='left')
minusLabel2.pack(side='left')
hour2.pack(side='left')
restLabel2.pack(side='left')
date_btn.pack(side='left')
# 棒グラフ
barFrame.pack(side='left', expand=True)
barLabel.pack(side='left')
barFormat.pack(side='left')
perLabel.pack(side='left')
# 幅
widthFrame.pack(side='left', expand=True)
widthLabel.pack(side='left')
widthFormat.pack(side='left')
narrow_btn.pack(side='left')
wide_btn.pack(side='left')

# 移動ボタン(左)
left_btn.pack(fill='x', padx=20, side='left')
# グラフ
graph.pack(graphTab)
# 移動ボタン(右)
right_btn.pack(fill='x', padx=20, side='right')

# 実行
root.mainloop()
