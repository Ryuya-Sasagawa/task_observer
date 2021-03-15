import sys
import win32gui

def getActiveWindowTitle():
    activeWindowTitle = win32gui.GetWindowText(win32gui.GetForegroundWindow());
    return activeWindowTitle


def main():
    bufWindowTitle = ""

    try:
        while True:
            activeWindowTitle = getActiveWindowTitle()
            if bufWindowTitle != activeWindowTitle:
                print(activeWindowTitle)
                bufWindowTitle = activeWindowTitle
    except KeyboardInterrupt:
        sys.exit(0)

import tkinter as tk

def window():
    win = tk.Tk()
    win.title("Hello, World!")  # タイトル
    win.geometry("400x300")  # サイズ

    # ウィンドウを動かす --- (*3)
    win.mainloop()