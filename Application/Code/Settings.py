import configparser
from docx.shared import Cm

def importSettings():
    config = configparser.ConfigParser()
    config.read('config.ini')
    formatting = config['Document Formatting']

    global size
    size = formatting.getint('IconSize', fallback = 75)

    global mainTableColWidth1
    global mainTableColWidth2
    global mainTableColWidth3
    global mainTableColWidth4

    mainTableColWidth1 = Cm(formatting.getfloat('mainTableColWidth1', fallback = 3.44))
    mainTableColWidth2 = Cm(formatting.getfloat('mainTableColWidth2', fallback = 4.75))
    mainTableColWidth3 = Cm(formatting.getfloat('mainTableColWidth3', fallback = 2.49))
    mainTableColWidth4 = Cm(formatting.getfloat('mainTableColWidth4', fallback = 4.56))

    global discTableColWidth1
    global discTableColWidth2

    discTableColWidth1 = Cm(formatting.getfloat('discTableColWidth1', fallback = 3.44))
    discTableColWidth2 = Cm(formatting.getfloat('discTableColWidth2', fallback = 11.8))

    output = config['Output Settings']
    global path
    path = output.get('path', fallback = '..\\GHS') + '.docx'

    global open
    open = output.getboolean('open', fallback = True)