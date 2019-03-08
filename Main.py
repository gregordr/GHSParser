import Dangers
from multiprocessing import Pool
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
import Main


def getForAll(elements):
    pool = Pool()
    f = lambda A, n=5: [A[i:i + n] for i in range(0, len(A), n)]
    queries = f(elements) #Pubchem asks to only perform 5 requests per second, so we need to split into groups of 5.

    results = []

    for query in queries:
         results += pool.map(Dangers.getAllDangers, query)

    return results

class UI(Widget):
    pass

class UIApp(App):
    def build(self):
        Window.bind(on_key_down=self.key_action)
        return UI()

    def key_action(self, *args):
        if(list(args)[1] == 13 and list(args)[4] == ['ctrl'] ):
            Main.getForAll(["Water"])
UIApp().run()
