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
