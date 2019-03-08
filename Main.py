import Dangers
import OutputProcessor
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.lang import Builder
import re

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
        text = self.root.ids.input.text
        allCompounds = re.split("[\n;]" ,text)



if __name__ == "__main__":
    from kivy.core.window import Window
    Builder.load_file('UI.kv')
    UIApp().run()
