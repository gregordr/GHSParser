import requests
import json
from bs4 import BeautifulSoup
import re

def getAllDangers(Name):
    CID = getCID(Name)
    section = getDangerSection(CID)
    dangers = getDangers(section)
    return dangers

def getCID(cpName):
    res = requests.get("https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/" + cpName + "/cids/JSON")
    info = json.loads(res.content)
    if (info.keys().__contains__('IdentifierList')):
        return info['IdentifierList']['CID'][0]
    else:
        return None

def getDangerSection(CID):
    res = requests.get("https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/" + str(CID) + "/JSON")
    info = json.loads(res.content)
    for section in info['Record']['Section']:
        if(section['TOCHeading'] == 'Safety and Hazards'):
            return section['Section'][0]['Section'][0]['Information'][0]['StringValue']

    return None

def getDangers(section):
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
        newArray.append(string.replace("*","").replace(" ",""))
    return newArray