import Dangers
from kivy.app import App
from kivy.uix.widget import Widget
from docx import Document
from tkinter import Tk
from docx.shared import Inches

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
        text = UI.ids.test1
        print(text)
        #print(Dangers.getForAll(["Water"]))

def buildString(allDangers):
    used = "Name\tSymbols\tHazards\tPrecautions\n"
    for danger in allDangers:
        used += danger[0] + "\t"
        used += str(danger[1]) + "\t"
        for hazard in danger[2]:
            used += hazard[0] + ", "
        if (len(danger[2]) != 0):
            used = used[:-2] + "\t"
        for precaution in danger[3]:
            used += precaution + ", "
        if (len(danger[3]) != 0):
            used = used[:-2] + "\n"

    return used

#def doWord(allDangers):
#     document = Document()
#     table = document.add_table(rows=len(allDangers), cols=4)
#     hdr_cells = table.rows[0].cells
#     hdr_cells[0].text = 'Name'
#     hdr_cells[1].text = 'Symbols'
#     hdr_cells[2].text = 'Hazards'
#     hdr_cells[3].text = 'Precautions'

#     for danger in allDangers:
#         row_cells = table.add_row().cells
#         row_cells[0].text = danger[0]
#         row_cells[1].text = danger[1]
#         for hazard in danger[2]:
#             row_cells[2].text = row_cells[2].text + hazard[0] + ","

#         for precaution in danger[3]:
#             row_cells[3].text = row_cells[3].text + precaution + ","

#     document.save("here.docx")

if __name__ == "__main__":
    d=None
    #from kivy.core.window import Window
    #UIApp().run()
