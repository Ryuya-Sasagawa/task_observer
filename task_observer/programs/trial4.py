from pynput import mouse, keyboard

class Monitor:
    def __init__(self):
        self.counter = 0
        self.over_count = 5

    def count(self):
        self.counter += 1
        print('Count:{0}'.format(self.counter))

    def is_over(self):
        return True if self.counter >= self.over_count else False

    def call(self):
        self.count()
        if self.is_over():
            print('Done')
            self.mouse_listener.stop() # 規定回数過ぎたら終了
            self.keyboard_listener.stop()

    # マウス入力
    def on_click(self, x, y, button, pressed):
        """クリック時に呼ばれる
        """
        print('{0} at {1}'.format(
            'Pressed' if pressed else 'Released',
            (x,y)))

        if pressed:
            self.call()

    # キーボード入力
    def on_press(self, key):
        """キーを押したときに呼ばれる"""
        try:
            print('alphanumeric key {0} pressed'.format(key.char))

        except AttributeError:
            print('special key {0} pressed'.format(key))

    def on_release(self, key):
        """キーを離したときに呼ばれる"""
        try:
            print('alphanumeric key {0} released'.format(key.char))

        except AttributeError:
            print('special key {0} released'.format(key))


    def start(self):
        with mouse.Listener(
            on_click=self.on_click) as self.mouse_listener, keyboard.Listener(
            on_press=self.on_press, on_release=self.on_release) as self.keyboard_listener:
            self.mouse_listener.join()
            self.keyboard_listener.join()


monitor = Monitor()
monitor.start()
#TODO: trial4->マウスとキーボードの入力を常時監視し、マウスのクリックと座標、キーボード押下とその種類を出力する(5回クリックするとプログラムが終了する)