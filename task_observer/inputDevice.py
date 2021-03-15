from pynput import mouse, keyboard
import time

class Mouse:
    def start(self):
        self.listener.start()
    def stop(self):
        self.listener.stop()
    def reset(self):
        self.clickCounter = self.scrollCounter = 0
    def getClick(self):
        return self.clickCounter
    def getScroll(self):
        return self.scrollCounter

    def click(self, x, y, button, pressed):
        if pressed:
            self.clickCounter += 1
    def scroll(self, x, y, dx, dy):
        self.scrollCounter += 1

    def __init__(self):
        self.clickCounter = 0
        self.scrollCounter = 0
        self.listener = mouse.Listener(on_click=self.click, on_scroll=self.scroll)

class Keyboard:
    def start(self):
        self.listener.start()
    def stop(self):
        self.listener.stop()
    def reset(self):
        self.keyCounter = 0

    def getPress(self):
        return self.keyCounter

    def press(self, key):
        self.keyCounter += 1

    def __init__(self):
        self.keyCounter = 0
        self.listener = keyboard.Listener(on_press=self.press)

if __name__ == '__main__':
    m = Mouse()
    k = Keyboard()

    m.start()
    k.start()
    time.sleep(10)
    print(m.getClick())
    print(m.getScroll())
    print(k.getPress())
    m.stop()
    k.stop()
