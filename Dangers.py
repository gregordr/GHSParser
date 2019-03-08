import requests
import json
from bs4 import BeautifulSoup
import re
from datetime import datetime
from multiprocessing import Pool

def getForAll(elements):
    pool = Pool()
    f = lambda A, n=5: [A[i:i + n] for i in range(0, len(A), n)]
    queries = f(elements) #Pubchem asks to only perform 5 requests per second, so we need to split into groups of 5.

    results = []

    for query in queries:
         results += pool.map(getAllDangers, query)

    return results

def getAllDangers(Name):
    print("Start: " + str(datetime.now()))
    CID = getCID(Name)
    print("Web1: " + str(datetime.now()))
    res = requests.get("https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/" + str(CID) + "/JSON")
    print("Web2: " + str(datetime.now()))
    try:
        info = json.loads(res.content)['Record']['Section']
    except:
        return res.content

    name = getName(info)
        
    dangers = [name] + getDangers(info)
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
    for section in info:
        if (section['TOCHeading'] == 'Names and Identifiers'):
            return section['Section'][0]['Information'][0]['StringValue']


def getDangerSection(info):
    for section in info:
        if (section['TOCHeading'] == 'Safety and Hazards'):
            return section['Section'][0]['Section'][0]['Information'][0]['StringValue']


def getDangers(info):
    section = getDangerSection(info)

    if section == None:
        return [[],[],[]]

    soup = BeautifulSoup(section, 'html.parser')

    images = soup.find("div", {"class": "pc-thumbnail-container"})
    imageArray = re.findall("\/images\/ghs\/GHS0(\d)\.svg", str(images))

    hazards = soup.find("div", {"class": "ghs-hazards"})
    hazardArray = re.findall("(H\d\d\d.*?):", str(hazards))
    hazardArray = cleanUp(hazardArray)

    precautions = soup.find("div", {"class": "ghs-precautionary"})
    precautionArray = re.findall("(P\d\d\d.*?)[,<]", str(precautions))

    return [imageArray, hazardArray, precautionArray]

def cleanUp(Array):
    newArray = []
    for string in Array:
        newArray.append(re.findall("(H\d\d\d)", string))
    return newArray