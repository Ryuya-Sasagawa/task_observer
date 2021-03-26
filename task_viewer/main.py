import sys
import datetime
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
import readData, graph, myDate, fileOperator

# -----定数-----
HOUR_LENGTH: Final[float] = 1 / 24
HALFDAY_LENGTH: Final[float] = 1 / 2
DAY_LENGTH: Final[int] = 1
WEEK_LENGTH: Final[int] = 7
MONTH_LENGTH: Final[int] = 30
YEAR_LENGTH: Final[int] = 365
PASSWORD: Final[str] = 'OiC&0~ktz1%i4nUg1ZodLM+XUPf(f|E9ez_vys9p'
FILEPATH: Final[str] = '../data/log_1'

# -----初期設定-----
span = HOUR_LENGTH
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
        d1 = datetime.datetime.strptime(d[0]+'/'+d[1]+'/'+d[2]+'/'+d[3], '%Y/%m/%d/%H')
        d2 = datetime.datetime.strptime(d[4]+'/'+d[5]+'/'+d[6]+'/'+d[7], '%Y/%m/%d/%H')
        if d2 - d1 > datetime.timedelta(0):
            # print(year.get() + '/' + month.get() + '/' + day.get() + '-' + hour.get() + ':00:00')
            graph.absoluteMove(d[0] + '-' + d[1] + '-' + d[2] + ' ' + d[3], blank=span*0.3)
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
#         ax.barでグラフを追加
#         graph.rewrite()
#         span = spanList(barset)

def getBarSpan():
    spanDict = {'1h':HOUR_LENGTH, '3h':HOUR_LENGTH*3, '6h':HOUR_LENGTH*6,
                '12h':HALFDAY_LENGTH, '1d':DAY_LENGTH, '1w':WEEK_LENGTH, '1m':MONTH_LENGTH}
    # print(barFormat.get())
    global barset, span, reformedList
    if barset != barFormat.get():
        barset = barFormat.get()
        span = spanDict[barset]
        reformedList = readData.reform(graphDataList, barset)
        # print(reformedList)
        graph.reset()
        locDict = {'1h':'hour', '3h':'day', '6h':'day',
                '12h':'day', '1d':'day', '1w':'month', '1m':'month'}
        graph.init(ylim=span*24*62, barset=barset)
        for wl in reformedList:
            x = pd.DatetimeIndex([wl[0] + ':00:00'])
            graph.plotbar(x, wl, span*0.7)
        # print(reformedList[-1])
        graph.absoluteRange(span * 8)
        graph.absoluteMove(reformedList[-1][0], blank=span*0.3)
        graph.relativeMove(-(span * 4))
        graph.rewrite()
    return True


vcmd3 = (dateFrame.register(getBarSpan))
barFormat = ttk.Combobox(barFrame, state='readonly', width=5, font=12, validatecommand=vcmd3, validate='focusin')
barFormat["values"] = ("1h", "3h", "6h", "12h", "1d", "1w", "1m")
barFormat.current(0)
perLabel = tk.Label(barFrame, text='毎', font=12)

# グラフ設定：横幅
widthFrame = tk.Frame(frame, background='white', height=50)
widthLabel = tk.Label(widthFrame, text='グラフの幅', font=12)

def changeRange(sp):
    if graph.relativeRange(sp*2):
        graph.relativeMove(-sp)
    graph.rewrite()

# TODO:矢印は画像に差し替える
narrow_btn = tk.Button(master=widthFrame, text='→←', command=lambda: changeRange(-span))
wide_btn = tk.Button(master=widthFrame, text='←→', command=lambda: changeRange(span))


# グラフ設定：移動ボタン
# TODO:矢印は画像に差し替える
def locate(sp):
    graph.relativeMove(sp)
    graph.rewrite()


left_btn = tk.Button(master=graphTab, text='←', command=lambda: locate(-span))
right_btn = tk.Button(master=graphTab, text='→', command=lambda: locate(span))

# グラフ
def onclick(event):
    # print(event)
    if event.xdata is not None and event.ydata is not None:
        # print(event.xdata, event.ydata)
        for wl in reformedList:
            x = myDate.datetimeToFloat(wl[0])
            # print(x)
            if x < event.xdata < x + span*0.7:
                # print(event.xdata, event.ydata)
                l = [w[1] for w in wl[1].getworklist()]
                s = datetime.timedelta(0)
                for t in l:
                    s += t.getdata()[0]
                    if datetime.timedelta(minutes=event.ydata) < s:
                        # print(event.xdata, event.ydata, t.getname(), t.getdata())
                        x += span*0.35
                        s = (s.seconds - t.getdata()[0].seconds/2) / 60
                        graph.annotation(t.getname(), x, s)
                        graph.rewrite()
                        break
                return
    graph.hideannot()
    graph.rewrite()


graph = graph.Graph(lambda event: onclick(event))
fileoperator = fileOperator.fileOperator()
latest = fileoperator.searchlogfile(datetime.datetime.now())
graphDataList = readData.parseData(latest)
reformedList = readData.reform(graphDataList, '1h')
for wl in reformedList:  # graphDataListをグラフに描画
    # print(wl[0])
    x = pd.DatetimeIndex([wl[0] + ':00:00'])
    graph.plotbar(x, wl, span*0.7)

graph.absoluteRange(span*8)
graph.absoluteMove(graphDataList[-1][0], blank=span*0.3)
graph.relativeMove(-(span*4))

# for wl in graphDataList:
#     print(wl[0])
#     for w in wl[1].getworklist():
#         print('  ', w[0], w[1].getdata())

# 表タブ
# 設定
settingTableFrame = tk.Frame(tableTab, background='gray', height=50)
tdateFrame = tk.Frame(settingTableFrame, background='white', height=50)
tdateLabel = tk.Label(tdateFrame, text='日時', font=12)


# グラフ設定：日時：from：年
tyear = tk.Entry(tdateFrame, width=4, validatecommand=vcmd1, font=('', 15, 'bold'), validate='key')
slashLabel5 = tk.Label(tdateFrame, text='/', font=12)
tyear.bind('<Return>', lambda event: enterevent(tmonth))
# グラフ設定：日時：from：月
tmonth = tk.Entry(tdateFrame, width=2, validatecommand=vcmd2, font=('', 15, 'bold'), validate='key')
slashLabel6 = tk.Label(tdateFrame, text='/', font=12)
tmonth.bind('<Return>', lambda event: enterevent(tday))
# グラフ設定：日時：from：日
tday = tk.Entry(tdateFrame, width=2, validatecommand=vcmd2, font=('', 15, 'bold'), validate='key')
minusLabel3 = tk.Label(tdateFrame, text='-', font=12)
tday.bind('<Return>', lambda event: enterevent(thour))
# グラフ設定：日時：from：時
thour = tk.Entry(tdateFrame, width=2, validatecommand=vcmd2, font=('', 15, 'bold'), validate='key')
restLabel3 = tk.Label(tdateFrame, text=':00:00', font=12)
thour.bind('<Return>', lambda event: enterevent(tdate_btn))
# グラフ設定：日時：ボタン
def tmove():
    d = tyear.get(), tmonth.get(), tday.get(), thour.get()
    flag = True
    for i in d:
        if not i.isdecimal():
            flag = False

    if flag is True:
        d = datetime.datetime.strptime(d[0]+'/'+d[1]+'/'+d[2]+'/'+d[3], '%Y/%m/%d/%H')
        if datetime.datetime(2020, 1, 1, 0) < d < datetime.datetime(2300, 1, 1, 0):
            last = len(table.get_children()) # = int(len(cmd)/5)
            loc = last
            for i in range(len(table.get_children())):
                s = datetime.datetime.strptime(cmd[i*5+1][2:], '%Y-%m-%d %H:%M:%S')
                if s > d:
                    loc = i
                    break
            table.yview_moveto(loc / last)
            return
        messagebox.showerror('エラー', '範囲が正しくありません。')
        return
    messagebox.showerror('エラー', '日付が正しくありません。')


tdate_btn = tk.Button(master=tdateFrame, text='MOVE', command=tmove)
tdate_btn.bind('<Return>', lambda event: tmove())

# 表
tableFrame = tk.Frame(tableTab, background='white', )
table = ttk.Treeview(tableFrame, height=30)
table['show'] = "headings"
table['columns'] = (1, 2, 3, 4, 5)
table.heading(1,text="名前")
table.heading(2,text="開始時刻")
table.heading(3,text="終了時刻")
table.heading(4,text="経過時間")
table.heading(5,text="クリック/スクロール/キー入力")
table.column(2, width=130)
table.column(3, width=130)
table.column(4, width=80)
table.column(5, width=150)

cmd = readData.openfile(latest)
for i in range(int(len(cmd)/5)):
    name = cmd[i*5][2:]
    s = datetime.datetime.strptime(cmd[i*5+1][2:], '%Y-%m-%d %H:%M:%S')
    e = datetime.datetime.strptime(cmd[i*5+2][2:], '%Y-%m-%d %H:%M:%S')
    o = cmd[i*5+4][2:].split(' ')
    o = o[0]+' / '+o[1]+' / '+o[2]
    table.insert("", "end", values=(name, s, e, e-s, o))


scroll = tk.Scrollbar(tableFrame, orient=tk.VERTICAL, command=table.yview)
table["yscrollcommand"] = scroll.set

# -----レイアウト生成-----
# タブ
nb.pack(fill='both', expand=1)
# グラフ設定
frame.pack(fill=tk.BOTH)
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
narrow_btn.pack(side='left')
wide_btn.pack(side='left')

# 移動ボタン(左)
left_btn.pack(fill='x', padx=20, side='left')
# グラフ
graph.pack(graphTab)
# 移動ボタン(右)
right_btn.pack(fill='x', padx=20, side='right')

# 表
settingTableFrame.pack(fill=tk.BOTH)
tdateFrame.pack(side='left', expand=True)
tdateLabel.pack(side='left')
tyear.pack(side='left')
slashLabel5.pack(side='left')
tmonth.pack(side='left')
slashLabel6.pack(side='left')
tday.pack(side='left')
minusLabel3.pack(side='left')
thour.pack(side='left')
restLabel3.pack(side='left')
tdate_btn.pack(side='left')

tableFrame.pack(fill=tk.BOTH)
scroll.pack(side='right', fill="y")
table.pack(fill=tk.BOTH)

# 実行
root.mainloop()
