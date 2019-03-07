import Dangers
from multiprocessing import Pool
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window


def getForAll(elements):
    pool = Pool()
    f = lambda A, n=5: [A[i:i + n] for i in range(0, len(A), n)]
    queries = f(elements) #Pubchem asks to only perform 5 requests per second, so we need to split into groups of 5.

    results = []

    for query in queries:
         results += pool.map(Dangers.getAllDangers, query)

    return results

class UI(Widget):
    def __init__(self, **kwargs):
        super(UI, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'w':
            print("yes")
            return False
        return True


class UIApp(App):
    def build(self):
        return UI()

UIApp().run()