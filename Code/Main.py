import multiprocessing

from Code import OutputProcessor, Dangers
import re
import os
os.environ["KIVY_NO_FILELOG"] = "1"
os.environ["KIVY_NO_CONSOLELOG"] = "1"

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

    def on_start(self, **kwargs):
        output = self.root.ids.output
        output.text = 'Enter compounds, seperated by ; or a newline. Press Ctrl+Enter to proceed!'

    def on_stop(self):
        raise SystemExit(0)

    def process(self):
        try:
            output = self.root.ids.output
            output.text = "Processing..."

            text = self.root.ids.input.text

            allCompounds = re.split("[\n;]" ,text)
            allCompounds = list(filter(lambda s: any([c.isalnum() for c in s]), allCompounds))
            allDangers = Dangers.getForAll(allCompounds)
            output.text = ""
            validDangers = []
            for danger in allDangers:
                if danger[0] == 'Error':
                    output.text = output.text + 'Error: Could not find information about ' + danger[1] + '\n'
                else:
                    validDangers.append(danger)

            location = OutputProcessor.doWord(validDangers)

            output.text = output.text + 'Saved document to ' + location
        except BaseException as e:
            output = self.root.ids.output
            output.text = str(e)

if __name__ == "__main__":
    multiprocessing.freeze_support()
    from kivy.lang import Builder
    from kivy.core.window import Window
    Builder.load_file('UI.kv')
    UIApp().run()
