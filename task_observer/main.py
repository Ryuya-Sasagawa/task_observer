import sys
import win32gui
import time
import datetime
from typing import Final
import inputDevice
import file

# 定数
LOGFILE_NAME: Final[str] = 'data/applicationLog'
LOGFILE_WRITE_TIMING: Final[int] = 100
PASSWORD: Final[str] = 'OiC&0~ktz1%i4nUg1ZodLM+XUPf(f|E9ez_vys9p'

def getActiveWindowTitle():
    activeWindowTitle = win32gui.GetWindowText(win32gui.GetForegroundWindow());
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
            activeWindowTitle = getActiveWindowTitle()

            if bufWindowTitle != activeWindowTitle and len(activeWindowTitle) != 0:
                temp = datetime.datetime.fromtimestamp(time.time())
                if len(bufWindowTitle) != 0:
                    print(temp - now, end=' ')
                    print(str(mouse.getClick()) + " " + str(keyboard.getPress()))
                    logBuffer += 'e '+temp.strftime('%Y-%m-%d %H:%M:%S')+'\n'
                    logBuffer += 't '+str(temp - now)+'\n'
                    logBuffer += 'o '+str(mouse.getClick())+" "+\
                                 str(mouse.getScroll())+" "+str(keyboard.getPress())+'\n'
                    lb_lineCount += 1
                    if lb_lineCount == lb_writeTiming:
                        file.write(LOGFILE_NAME, PASSWORD, file.read(LOGFILE_NAME, PASSWORD) + logBuffer)
                        print('write down to file')
                        lb_lineCount = 0
                        logBuffer = ''
                now = temp
                mouse.reset()
                keyboard.reset()
                print(now, activeWindowTitle)
                logBuffer += 'n ' + activeWindowTitle + '\n'
                logBuffer += 's ' + now.strftime('%Y-%m-%d %H:%M:%S') + '\n'
                bufWindowTitle = activeWindowTitle

    except KeyboardInterrupt:
        temp = datetime.datetime.fromtimestamp(time.time())
        logBuffer += 'e ' + temp.strftime('%Y-%m-%d %H:%M:%S') + '\n'
        logBuffer += 't ' + str(temp - now) + '\n'
        logBuffer += 'o ' + str(mouse.getClick()) + " " + \
                     str(mouse.getScroll()) + " " + str(keyboard.getPress()) + '\n'
        file.write(LOGFILE_NAME, PASSWORD, file.read(LOGFILE_NAME, PASSWORD) + logBuffer)
        mouse.stop()
        keyboard.reset()
        sys.exit(0)

    # with open('data/applicationLog', 'a', encoding='utf-8') as f:
    #     try:
    #         while True:
    #             activeWindowTitle = getActiveWindowTitle()
    #
    #             if bufWindowTitle != activeWindowTitle and len(activeWindowTitle) != 0:
    #                 temp = datetime.datetime.fromtimestamp(time.time())
    #                 if len(bufWindowTitle) != 0:
    #                     print(temp-now, end=' ')
    #                     print(str(mouse.getClick()) + " " + str(keyboard.getPress()))
    #                     f.write('end ' + temp.strftime('%Y-%m-%d %H:%M:%S') + '\n')
    #                     f.write('time ' + str(temp-now) + '\n')
    #                     f.write('operation ' + str(mouse.getClick()) + " " + str(mouse.getScroll()) + " " + str(keyboard.getPress()) + '\n')
    #                 now = temp
    #                 mouse.reset()
    #                 keyboard.reset()
    #                 print(now, activeWindowTitle)
    #                 f.write('name ' + activeWindowTitle + '\n')
    #                 f.write('start ' + now.strftime('%Y-%m-%d %H:%M:%S') + '\n')
    #                 bufWindowTitle = activeWindowTitle
    #
    #     except KeyboardInterrupt:
    #         temp = datetime.datetime.fromtimestamp(time.time())
    #         f.write('end ' + temp.strftime('%Y-%m-%d %H:%M:%S') + '\n')
    #         f.write('time ' + str(temp - now) + '\n')
    #         f.write('operation ' + str(mouse.getClick()) + " " + str(mouse.getScroll()) + " " + str(keyboard.getPress()) + '\n')
    #         mouse.stop()
    #         keyboard.reset()
    #         sys.exit(0)
