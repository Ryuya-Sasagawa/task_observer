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
FILEPATH: Final[str] = '../task_checker2/data/applicationLog'

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
# グラフ設定：日時：フレーム＆見出し
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


# グラフ設定：日時：年
vcmd1 = (dateFrame.register(baserestrict), '%i', '%S', 4)
year = tk.Entry(dateFrame, width=4, validatecommand=vcmd1, font=('', 15, 'bold'), validate='key')
year.bind('<Return>', lambda event: enterevent(month))
slashLabel = tk.Label(dateFrame, text='/', font=12)
# グラフ設定：日時：共用(月、日、時)
vcmd2 = (dateFrame.register(baserestrict), '%i', '%S', 2)
# グラフ設定：日時：月
month = tk.Entry(dateFrame, width=2, validatecommand=vcmd2, font=('', 15, 'bold'), validate='key')
slashLabel2 = tk.Label(dateFrame, text='/', font=12)
month.bind('<Return>', lambda event: enterevent(day))
# グラフ設定：日時：日
day = tk.Entry(dateFrame, width=2, validatecommand=vcmd2, font=('', 15, 'bold'), validate='key')
minusLabel = tk.Label(dateFrame, text='-', font=12)
day.bind('<Return>', lambda event: enterevent(hour))
# グラフ設定：日時：時
hour = tk.Entry(dateFrame, width=2, validatecommand=vcmd2, font=('', 15, 'bold'), validate='key')
restLabel = tk.Label(dateFrame, text=':00:00', font=12)
hour.bind('<Return>', lambda event: enterevent(date_btn))


# グラフ設定：日時：ボタン
def move():
    if year.get().isdecimal() and month.get().isdecimal() and \
            day.get().isdecimal() and hour.get().isdecimal():
        if int(year.get()) >= 1970 and int(year.get()) <= 2500:
            if int(month.get()) >= 1 and int(month.get()) <= 12:
                if int(day.get()) >= 1 and int(day.get()) <= myDate.lastdate(int(year.get()), int(month.get())):
                    if int(hour.get()) >= 0 and int(hour.get()) <= 23:
                        # print(year.get() + '/' + month.get() + '/' + day.get() + '-' + hour.get() + ':00:00')
                        graph.absoluteMove(year.get() + '-' + month.get() + '-' + day.get() + ' ' + hour.get())
                        canvas.draw()
                        canvas.get_tk_widget().pack(side='left', fill=tk.BOTH, expand=1)
                        return
    messagebox.showerror('エラー', '日付が正しくありません。')


date_btn = tk.Button(master=dateFrame, text='MOVE', command=move)
date_btn.bind('<Return>', lambda event: move())

# グラフ設定：棒グラフ
barFrame = tk.Frame(frame, background='white', height=50)
barLabel = tk.Label(barFrame, text='棒グラフ', font=12)


def getBarSpan(v):
    # print('validate:', v)
    # print(barFormat.get())
    # TODO: barsetとbarFormat.getが一致していない場合barsetを更新。
    #  barsetの値で分岐して、barsetで定義された範囲でgraphDataListを整形する(graph.pyに実装)
    global barset, scroll_length, span
    if barset != barFormat.get():
        barset = barFormat.get()
        graph.relativeMove(span/2)
        if barset == '1h':
            scroll_length = HOUR_LENGTH
            span = HALFDAY_LENGTH
        elif barset == '3h':
            scroll_length = HOUR_LENGTH
            span = DAY_LENGTH
        elif barset == '6h':
            scroll_length = HALFDAY_LENGTH
            span = DAY_LENGTH
        elif barset == '12h':
            scroll_length = HALFDAY_LENGTH
            span = WEEK_LENGTH
        elif barset == '1d':
            scroll_length = DAY_LENGTH
            span = WEEK_LENGTH
        elif barset == '1w':
            scroll_length = WEEK_LENGTH
            span = MONTH_LENGTH
        elif barset == '1m':
            scroll_length = MONTH_LENGTH
            span = YEAR_LENGTH
        # print(barset)
        graph.absoluteRange(span)
        graph.relativeMove(-span/2)

    return True


vcmd3 = (dateFrame.register(getBarSpan), '%V')
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


# TODO: ボタンを複数用意する？
def changeRange(sp):
    graph.relativeRange(sp)
    canvas.draw()
    canvas.get_tk_widget().pack(side='left', fill=tk.BOTH, expand=1)


# TODO:矢印は画像に差し替える
narrow_btn = tk.Button(master=widthFrame, text='→←', command=lambda: changeRange(-span))
wide_btn = tk.Button(master=widthFrame, text='←→', command=lambda: changeRange(span))


# グラフ設定：移動ボタン
# TODO:矢印は画像に差し替える
def locate(sclen):
    graph.relativeMove(sclen)
    canvas.draw()
    canvas.get_tk_widget().pack(side='left', fill=tk.BOTH, expand=1)


left_btn = tk.Button(master=graphTab, text='←', command=lambda: locate(-scroll_length))
right_btn = tk.Button(master=graphTab, text='→', command=lambda: locate(scroll_length))

# グラフ
graph = graph.Graph()
graphDataList = readData.parseData(FILEPATH, PASSWORD)

for wl in graphDataList:  # graphDataListをグラフに描画
    print(wl[0])
    x = pd.DatetimeIndex(pd.DatetimeIndex([wl[0] + ':00:00']))
    base = 0
    for w in wl[1].getworklist():
        # print(w[1].getdata()[0].total_seconds()/60)
        time = w[1].getdata()[0].total_seconds() / 60
        graph.getax().bar(x, time, bottom=base, align='edge', width=0.03)  # データの描画
        base += time

# print(graphDataList[-1][0])

graph.absoluteRange(span)  # TODO: spanとは別の変数を使用する？(spanは本来ボタンクリックで変化する幅の変数)
graph.absoluteMove(graphDataList[-1][0])
graph.relativeMove(-(span / 2))

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
canvas = FigureCanvasTkAgg(graph.getfig(), master=graphTab)
canvas.draw()
canvas.get_tk_widget().pack(side='left', fill=tk.BOTH, expand=1)
# 移動ボタン(右)
right_btn.pack(fill='x', padx=20, side='right')

# 実行
root.mainloop()
# TODO: グラフの横幅に応じて罫線を変える
# TODO: グラフの横幅に応じて横幅変更ボタンの振れ幅を変える
#  or 振れ幅を設定するコンボボックスを作る
#  or ボタンを廃止、コンボボックスに入力できるようにする
