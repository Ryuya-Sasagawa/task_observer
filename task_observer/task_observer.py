# ウィンドウAPI
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


import time
import threading
import sys
import win32gui
import time
import datetime
from typing import Final
import inputDevice
import fileOperator

# 定数
LOGFILE_WRITE_TIMING: Final[int] = 100

def getActiveWindowTitle():
    activeWindowTitle = win32gui.GetWindowText(win32gui.GetForegroundWindow())
    return activeWindowTitle

def window():
    global phase

    root = tk.Tk()
    root.title('')
    root.geometry("200x100")
    root.resizable(False, False)
    titleframe = tk.Frame(root)
    title = tk.Label(titleframe, text='Task Observer', font=15)
    buttonframe = tk.Frame(root)
    def switch():
        global phase
        phase += 1
        if phase == 1:
            button['text'] = '開始'
            while True:
                # print('app wait')
                if phase == 2:
                    break
                # time.sleep(1)
        elif phase == 3:
            button['text'] = '停止'
            while True:
                # print('app wait')
                if phase == 0:
                    break
                # time.sleep(1)
        else:
            print('error')
            phase -= 1

    button = tk.Button(buttonframe, text='停止', font=20, command=switch)

    titleframe.pack(fill='x')
    title.pack()
    buttonframe.pack(fill=tk.BOTH, expand=True)
    button.pack(expand=True)

    root.mainloop()
    phase = 4

def observer():
    global phase
    # 変数の初期化
    logBuffer = ''  # アプリ名などを取得してからファイルに保存するまでに一時的に保管するバッファ
    lb_lineCount = 0  # logBufferをファイルに書き込むタイミングを管理する変数
    lb_writeTiming = LOGFILE_WRITE_TIMING  # logBufferをファイルに書き込むタイミングを管理する変数
    fileoperator = fileOperator.fileOperator()
    bufWindowTitle = ''  # アプリ名(ウィンドウタイトル)を一時的に保管するバッファ
    now = datetime.datetime.fromtimestamp(time.time())  # 現在時刻
    mouse = inputDevice.Mouse()  # マウスの操作(クリックとスクロール)を監視するクラス
    keyboard = inputDevice.Keyboard()  # キーボードの操作を監視するクラス
    mouse.start()  # マウスの監視を開始する関数
    keyboard.start()  # キーボードの監視を開始する関数

    while True:
        if phase == 0:
            # print('observer running')
            activeWindowTitle = getActiveWindowTitle()  # 最前面のアプリのタイトルを取得

            # 分岐：最前面のアプリが変わったら
            #   ※len(active~~)はアプリを切り替えるときに、間にある名前のないアプリ(？)を除外するため。
            if bufWindowTitle != activeWindowTitle and len(activeWindowTitle) != 0:
                temp = datetime.datetime.fromtimestamp(time.time())  # アプリの使用開始時刻を取得
                # 「main.pyの起動から最初にアプリを開くまで」を除外
                if len(bufWindowTitle) != 0:
                    # print(temp - now, end=' ')  # debug
                    # print(str(mouse.getClick()) + " " + str(keyboard.getPress()))  # debug
                    logBuffer += 'e ' + temp.strftime('%Y-%m-%d %H:%M:%S') + '\n'  # アプリの使用終了時刻
                    logBuffer += 't ' + str(temp - now) + '\n'  # アプリの使用時間
                    # アプリ使用中のクリック、スクロール、キー入力
                    logBuffer += 'o ' + str(mouse.getClick()) + " " + \
                                 str(mouse.getScroll()) + " " + str(keyboard.getPress()) + '\n'
                    lb_lineCount += 1
                    # アプリの使用ログを一定数スタックしたら
                    if lb_lineCount == lb_writeTiming:
                        # AESで暗号化して書き込み
                        fileoperator.addlog(logBuffer)
                        # file.write(LOGFILE_NAME, PASSWORD, file.read(LOGFILE_NAME, PASSWORD) + logBuffer)
                        # print('write down to file')  # debug
                        lb_lineCount = 0
                        logBuffer = ''

                now = temp  # アプリの使用開始時刻
                mouse.reset()  # クリック、スクロールのカウントをリセット
                keyboard.reset()  # キー入力のカウントをリセット
                # print(now, activeWindowTitle)  # debug
                logBuffer += 'n ' + activeWindowTitle + '\n'  # アプリの名前
                logBuffer += 's ' + now.strftime('%Y-%m-%d %H:%M:%S') + '\n'  # アプリの使用開始時刻
                bufWindowTitle = activeWindowTitle
        elif phase == 1:
            # print('phase=1')
            temp = datetime.datetime.fromtimestamp(time.time())
            logBuffer += 'e ' + temp.strftime('%Y-%m-%d %H:%M:%S') + '\n'
            logBuffer += 't ' + str(temp - now) + '\n'
            logBuffer += 'o ' + str(mouse.getClick()) + " " + \
                         str(mouse.getScroll()) + " " + str(keyboard.getPress()) + '\n'
            fileoperator.addlog(logBuffer)
            # file.write(LOGFILE_NAME, PASSWORD, file.read(LOGFILE_NAME, PASSWORD) + logBuffer)
            lb_lineCount = 0
            logBuffer = ''
            mouse.reset()
            keyboard.reset()
            phase = 2
        elif phase == 2:
            pass
        elif phase == 3:
            # print('phase=3')
            logBuffer += 'n ' + activeWindowTitle + '\n'  # アプリの名前
            logBuffer += 's ' + now.strftime('%Y-%m-%d %H:%M:%S') + '\n'  # アプリの使用開始時刻
            bufWindowTitle = activeWindowTitle
            # time.sleep(5)
            phase = 0
        elif phase == 4:
            print('observer: sync being false')
            temp = datetime.datetime.fromtimestamp(time.time())
            logBuffer += 'e ' + temp.strftime('%Y-%m-%d %H:%M:%S') + '\n'
            logBuffer += 't ' + str(temp - now) + '\n'
            logBuffer += 'o ' + str(mouse.getClick()) + " " + \
                         str(mouse.getScroll()) + " " + str(keyboard.getPress()) + '\n'
            fileoperator.addlog(logBuffer)
            # file.write(LOGFILE_NAME, PASSWORD, file.read(LOGFILE_NAME, PASSWORD) + logBuffer)
            mouse.stop()
            keyboard.stop()
            break

if __name__ == '__main__':
    phase = 0
    # 遷移図
    # →   →アプリ終了→   4　　
    # ↑      　　　　　  ↑
    # 0 →ボタン押下→ 1   アプリ終了
    # ↑  　　　　　  ↓   ↑
    # 3 ←ボタン押下← 2 → ↑
    #####
    # 0: アプリ：待機中　監視：実行中
    # 1: アプリ：ボタン押下時。開始/停止ボタン、終了ボタンがロック
    #    監視：実行→停止に遷移中
    # 2: アプリ：ロック解除。待機中　監視：停止中
    # 3: アプリ：ボタン押下時。開始/停止ボタン、終了ボタンがロック
    #    監視：停止→実行に遷移中
    # 4: ウィンドウが閉じられた。監視プログラムも終了する。
    windowappThread = threading.Thread(target=window)
    observerThread = threading.Thread(target=observer)

    windowappThread.start()
    observerThread.start()
    windowappThread.join()
    observerThread.join()