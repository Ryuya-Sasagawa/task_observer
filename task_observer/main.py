import sys
import win32gui
import time
import datetime
from typing import Final
import inputDevice
import file

# 定数
LOGFILE_NAME: Final[str] = '../data/applicationLog'
LOGFILE_WRITE_TIMING: Final[int] = 100
PASSWORD: Final[str] = 'OiC&0~ktz1%i4nUg1ZodLM+XUPf(f|E9ez_vys9p'


def getActiveWindowTitle():
    activeWindowTitle = win32gui.GetWindowText(win32gui.GetForegroundWindow())
    return activeWindowTitle


if __name__ == '__main__':
    # 変数の初期化
    logBuffer = ''  # アプリ名などを取得してからファイルに保存するまでに一時的に保管するバッファ
    lb_lineCount = 0  # logBufferをファイルに書き込むタイミングを管理する変数
    lb_writeTiming = LOGFILE_WRITE_TIMING  # logBufferをファイルに書き込むタイミングを管理する変数
    bufWindowTitle = ''  # アプリ名(ウィンドウタイトル)を一時的に保管するバッファ
    now = datetime.datetime.fromtimestamp(time.time())  # 現在時刻
    mouse = inputDevice.Mouse()  # マウスの操作(クリックとスクロール)を監視するクラス
    keyboard = inputDevice.Keyboard()  # キーボードの操作を監視するクラス
    mouse.start()  # マウスの監視を開始する関数
    keyboard.start()  # キーボードの監視を開始する関数

    try:
        while True:
            activeWindowTitle = getActiveWindowTitle()  # 最前面のアプリのタイトルを取得

            # 分岐：最前面のアプリが変わったら
            #   ※len(active~~)はアプリを切り替えるときに、間にある名前のないアプリ(？)を除外するため。
            if bufWindowTitle != activeWindowTitle and len(activeWindowTitle) != 0:
                temp = datetime.datetime.fromtimestamp(time.time())  # アプリの使用開始時刻を取得
                # 「main.pyの起動から最初にアプリを開くまで」を除外
                if len(bufWindowTitle) != 0:
                    print(temp - now, end=' ')  # debug
                    print(str(mouse.getClick()) + " " + str(keyboard.getPress()))  # debug
                    logBuffer += 'e ' + temp.strftime('%Y-%m-%d %H:%M:%S') + '\n'  # アプリの使用終了時刻
                    logBuffer += 't ' + str(temp - now) + '\n'  # アプリの使用時間
                    # アプリ使用中のクリック、スクロール、キー入力
                    logBuffer += 'o ' + str(mouse.getClick()) + " " + \
                                 str(mouse.getScroll()) + " " + str(keyboard.getPress()) + '\n'
                    lb_lineCount += 1
                    # アプリの使用ログを一定数スタックしたら
                    if lb_lineCount == lb_writeTiming:
                        # AESで暗号化して書き込み
                        file.write(LOGFILE_NAME, PASSWORD, file.read(LOGFILE_NAME, PASSWORD) + logBuffer)
                        print('write down to file')  # debug
                        lb_lineCount = 0
                        logBuffer = ''

                now = temp  # アプリの使用開始時刻
                mouse.reset()  # クリック、スクロールのカウントをリセット
                keyboard.reset()  # キー入力のカウントをリセット
                print(now, activeWindowTitle)  # debug
                logBuffer += 'n ' + activeWindowTitle + '\n'  # アプリの名前
                logBuffer += 's ' + now.strftime('%Y-%m-%d %H:%M:%S') + '\n'  # アプリの使用開始時刻
                bufWindowTitle = activeWindowTitle

    # ctrl+cが入力されたら
    # TODO: PCのシャットダウン、再起動を検出したら以下の処理が実行されるようにする
    #  案1．タスクスケジューラで検出し、main.pyにctrl+cを入力する  案2．main.pyが検出できるようにする
    except KeyboardInterrupt:
        temp = datetime.datetime.fromtimestamp(time.time())
        logBuffer += 'e ' + temp.strftime('%Y-%m-%d %H:%M:%S') + '\n'
        logBuffer += 't ' + str(temp - now) + '\n'
        logBuffer += 'o ' + str(mouse.getClick()) + " " + \
                     str(mouse.getScroll()) + " " + str(keyboard.getPress()) + '\n'
        file.write(LOGFILE_NAME, PASSWORD, file.read(LOGFILE_NAME, PASSWORD) + logBuffer)
        mouse.stop()
        keyboard.reset()
        sys.exit(0)  # main.pyの終了
