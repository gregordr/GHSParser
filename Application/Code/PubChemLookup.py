import requests
import json
from bs4 import BeautifulSoup
import re
from datetime import datetime
from multiprocessing import Pool

def processInputText(inputText):
    allCompounds = re.split("[\n;]", inputText)
    allCompounds = list(filter(lambda s: any([c.isalnum() for c in s]), allCompounds))

    pool = Pool()
    f = lambda A, n=5: [A[i:i + n] for i in range(0, len(A), n)]
    queries = f(allCompounds) #Pubchem asks to only perform 5 requests per second, so we need to split into groups of 5.

    results = []

    for query in queries:
         results += pool.map(processCompound, query)

    return results

def processCompound(Name):
    CID = getCID(Name)
    res = requests.get("https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/" + str(CID) + "/JSON")
    try:
        info = json.loads(res.content)['Record']
    except:
        return ['Error', Name]

    Name = getName(info)
        
    dangers = [Name] + getStatements(info)
    print("End: " + str(datetime.now()))
    return dangers

def getCID(cpName):
    res = requests.get("https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/" + str(cpName) + "/cids/JSON")
    info = json.loads(res.content)
    if (info.keys().__contains__('IdentifierList')):
        return info['IdentifierList']['CID'][0]
    else:
        return None

def getName(info):
        return info['RecordTitle']

def getSafetySection(info):
    for section in info['Section']:
        if (section['TOCHeading'] == 'Safety and Hazards'):
            return section['Section'][0]['Section'][0]['Information']

def getStatements(info):
    sections = getSafetySection(info)

    if(sections == None):
        return [[], [], []]

    images = None
    hazards = None
    precautions = None

    for section in sections:
        if(section['Name'] == 'Pictogram(s)'):
            images = section['Value']['StringWithMarkup'][0]['Markup']
        elif(section['Name'] == 'GHS Hazard Statements'):
            hazards = section['Value']['StringWithMarkup']
        elif(section['Name'] == 'Precautionary Statement Codes'):
            precautions = section['Value']['StringWithMarkup'][0]['String']

    imageArray = re.findall("\/images\/ghs\/GHS0(\d)\.svg", str(images))

    hazardArray = re.findall("(H\d\d\d.*?):", str(hazards))
    hazardArray = cleanUpHazards(hazardArray)

    precautionArray = re.findall("(P\d\d\d.*?)[,<]", str(precautions))

    return [imageArray, hazardArray, precautionArray]

def cleanUpHazards(Array):
    newArray = []
    for string in Array:
        newArray.append(re.findall("(H\d\d\d)", string)[0])
    return newArray