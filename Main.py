import Dangers
import OutputProcessor
from kivy.app import App
from kivy.uix.widget import Widget

class UI(Widget):
    pass

class UIApp(App):
    def build(self):
        Window.bind(on_key_down=self.key_action)
        return UI()

    def key_action(self, *args):
        if(list(args)[1] == 13 and list(args)[4] == ['ctrl'] ):
            self.process()

    def process(self):
        print(UI)
        a = UI.ids
        text = UI.ids.input
        print(text)
        #print(Dangers.getForAll(["Water"]))


if __name__ == "__main__":
    d=None
    #from kivy.core.window import Window
    #UIApp().run()
