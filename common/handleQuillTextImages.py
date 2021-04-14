from bs4 import BeautifulSoup
from config import langs, backendAddress
from common.image_utils import _saveImage, delImage
from datetime import datetime
from random import random


def generateUniqueId():  # max 64
    return str(datetime.now().timestamp()) + "." + str(random())

def handleQuillTextImages(quillText, oldQuillTextImagesArr, deleteMissingImages=True):
    resp = {
        "text": None,
        "images": None
    }

    if type(quillText) is str:
        parsingRezult = _changeImages(quillText or "")
        resp["text"] = parsingRezult["quillText"]
    else:  # LocaleStr
        quillText = {**quillText}
        parsingRezult = None
        for lang in langs:
            langParsingRezult = _changeImages(quillText[lang] or "")
            quillText[lang] = langParsingRezult["quillText"]
            if not parsingRezult:
                parsingRezult = langParsingRezult
            else:
                parsingRezult["newImages"].extend(
                    langParsingRezult["newImages"])
                parsingRezult["oldImages"].extend(
                    langParsingRezult["oldImages"])
        resp["text"] = quillText

    if deleteMissingImages:
        for item in oldQuillTextImagesArr:
            if item not in parsingRezult["oldImages"]:
                delImage(item.split(backendAddress)[1])
    else:
        parsingRezult["oldImages"] = [*oldQuillTextImagesArr]
    resp["images"] = [*parsingRezult["newImages"], *parsingRezult["oldImages"]]

    return resp


def _changeImages(quillText):
    htmlObj = BeautifulSoup(quillText, features="html.parser")
    newImages = []
    oldImages = []
    for img in htmlObj.find_all("img"):
        img["loading"] = "lazy"
        if img["src"].startswith("data:"):
            fileUrl = _saveImage(img["src"], generateUniqueId())
            img["src"] = backendAddress + fileUrl
            newImages.append(img["src"])
        else:
            oldImages.append(img["src"])
    return {
        "quillText": str(htmlObj),
        "newImages": newImages,
        "oldImages": oldImages
    }