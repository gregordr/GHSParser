from docx.shared import Cm

def importSettings():
    global size
    size = 75

    global path
    path = '..\\GHS.docx'

    global mainTableColWidth1
    global mainTableColWidth2
    global mainTableColWidth3
    global mainTableColWidth4

    mainTableColWidth1 = Cm(3.44)
    mainTableColWidth2 = Cm(4.75)
    mainTableColWidth3 = Cm(2.49)
    mainTableColWidth4 = Cm(4.56)

    global discTableColWidth1
    global discTableColWidth2

    discTableColWidth1 = Cm(3.44)
    discTableColWidth2 = Cm(11.8)