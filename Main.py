import Dangers

def getForAll(compounds):
    dangers = []
    for compound in compounds:
        dangers.append(Dangers.getAllDangers(compound))
    return dangers