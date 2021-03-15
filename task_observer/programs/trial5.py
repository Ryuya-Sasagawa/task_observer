import sys

# Mac用
if sys.platform == "darwin":
    from AppKit import NSWorkspace
    from Quartz import (
        CGWindowListCopyWindowInfo,
        kCGWindowListOptionOnScreenOnly,
        kCGNullWindowID
    )

    def getActiveWindowTitle():

        curr_app = NSWorkspace.sharedWorkspace().frontmostApplication()
        curr_pid = NSWorkspace.sharedWorkspace().activeApplication()['NSApplicationProcessIdentifier']
        curr_app_name = curr_app.localizedName()
        options = kCGWindowListOptionOnScreenOnly
        windowList = CGWindowListCopyWindowInfo(options, kCGNullWindowID)

        txt = ""

        for window in windowList:
            pid = window['kCGWindowOwnerPID']
            windowNumber = window['kCGWindowNumber']
            ownerName = window['kCGWindowOwnerName']
            geometry = window['kCGWindowBounds']
            windowTitle = window.get('kCGWindowName', u'Unknown')

            if curr_pid == pid:
                activeWindowTitle = ownerName + " - " + windowTitle

        return activeWindowTitle

# Windows用
elif sys.platform == "win32":
    import win32gui

    def getActiveWindowTitle():

        activeWindowTitle = win32gui.GetWindowText(win32gui.GetForegroundWindow());
        return activeWindowTitle

else:
    def getActiveWindowTitle():
        return ""

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

if __name__ == '__main__':
    main()