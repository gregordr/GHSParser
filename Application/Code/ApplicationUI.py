import multiprocessing

from Application.Code import Settings, OutputProcessor, PubChemLookup
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
        output = self.root.ids.output
        try:
            output.text = ""
            inputText = self.root.ids.input.text
            allDangers = PubChemLookup.processInputText(inputText)

            validDangers = []
            for danger in allDangers:
                if danger[0] == 'Error':
                    output.text = output.text + 'Error: Could not find information about ' + danger[1] + '\n'
                else:
                    validDangers.append(danger)

            location = OutputProcessor.doWord(validDangers)

            output.text = output.text + 'Saved document to ' + location +'\n'

            if(Settings.open):
                self.openFile(location)
            #Success
        except BaseException as e:
            output.text = output.text + str(e)

    def openFile(self, filepath):
        import subprocess, os, platform
        if platform.system() == 'Darwin':  # macOS
            subprocess.call(('open', filepath))
        elif platform.system() == 'Windows':  # Windows
            os.startfile(filepath)
        else:  # linux variants
            subprocess.call(('xdg-open', filepath))

if __name__ == "__main__":
    multiprocessing.freeze_support()
    Settings.importSettings()
    from kivy.lang import Builder
    from kivy.core.window import Window
    Builder.load_file('UI.kv')
    UIApp().run()