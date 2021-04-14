from PIL import Image
import os
import sys
import requests
from io import BytesIO
import hashlib
import base64
from os import path, remove
import random


class ImageUtils():
    def resizeImage(self, strForKey, pathImage, path='', sizeWidthList=[]):
        '''sizeWidthList = [500, 400, 300, 200]'''
        newNameImg = hashlib.md5(str(strForKey).encode()).hexdigest()
        try:
            if pathImage.startswith(('https://', 'http://')):
                response = requests.get(pathImage)
                img = Image.open(BytesIO(response.content))
            elif pathImage.startswith('data'):
                img = Image.open(
                    BytesIO(base64.b64decode(pathImage.split(',')[-1])))
            else:
                img = Image.open(pathImage)

            if img.mode in ('RGBA', 'LA'):
                background = Image.new(img.mode[:-1], img.size, '#ffffff')
                background.paste(img, img.split()[-1])
                img = background

            for i, a in enumerate(sizeWidthList):
                img = img.convert("RGB")
                img.thumbnail((a['w'], a['h']))
                img.save('{path}/{key}_w{index}.jpg'.format(
                    path=path, key=newNameImg, index=str(i)), quality=100)
        except:
            return None

        return newNameImg

    def delImage(self, url):
        if url and path.exists(url[1:]):
            remove(url[1:])

    def _saveImage(self, dataUrl, name, imagesRoot=imagesRoot):
        if not dataUrl:
            return ""
        b64url_arr = dataUrl.split(",", 1)
        img = base64.b64decode(b64url_arr[1])
        img_format = b64url_arr[0].split(";", 1)[0][11:]
        url = "{}{}_{}.{}".format(imagesRoot, name, random(), img_format)
        with open(url[1:], "wb") as f:
            f.write(img)
        return url

    def changeImgFromDb(self, newImg, oldImg, newImgFileName="img", minimized=False, withDeleteFiles=True):
        if newImg["url"] != "":
            newImg["url"] = oldImg["url"]
            if minimized:
                newImg["miniatureUrl"] = oldImg["miniatureUrl"]
        else:
            if withDeleteFiles:
                delImage(oldImg["url"])
            if minimized:
                if withDeleteFiles:
                    delImage(oldImg["miniatureUrl"])
                newImg["miniatureUrl"] = ""

        if "newDataUrl" in newImg.keys():
            if newImg["newDataUrl"]:
                if withDeleteFiles:
                    delImage(oldImg["url"])
                newImg["url"] = _saveImage(newImg["newDataUrl"], newImgFileName)
                if minimized:
                    if withDeleteFiles:
                        delImage(oldImg["miniatureUrl"])
                    newImg["miniatureUrl"] = _saveImage(newImg["newDataUrl"], newImgFileName + "-miniature")
            del newImg["newDataUrl"]
        return newImg