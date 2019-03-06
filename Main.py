import Dangers

def getForAll(compounds):
    dangers = []
    for compound in compounds:
        dangers.append([compound] + Dangers.getAllDangers(compound))
    return dangers