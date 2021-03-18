#!/usr/bin/env python3
from random import choice
from PIL import Image, ImageEnhance
from pytesseract import image_to_string
import cv2 as cv
import numpy as np
import base64
import math
from os import system
TAGS_SEC = (0.225,0.185)
CHARACTER_FRAMES_SEC = (0.425,0.385)
def extractTags(frame):
    frame = prepImage(frame, TAGS_SEC)
    print(image_to_string(frame))
    
def extractPortraits(frame):
    frame, sig = prepCharacterImage(frame, CHARACTER_FRAMES_SEC)
    return frame, sig

def prepCharacterImage(image, adjusts):
    croppedImage = cv.cvtColor(image[890:1045, 1130:1280], cv.COLOR_BGR2GRAY)
    _, croppedImage = cv.threshold(croppedImage,127,255,cv.THRESH_BINARY)
    signature = 0
    for x in range(croppedImage.shape[0]):
        for y in range(croppedImage.shape[1]):
            pixel = croppedImage[x,y]
            signature += (pixel // 10)
            
    
    return croppedImage, signature
    



def prepImage(image, adjusts):
    image = Image.fromarray(image)
    oWidth, oHeight = image.size
    #Adjust Image Width to only extract tags
    wAdjust = oWidth * adjusts[0]
    lAdjust = wAdjust
    rAdjust = oWidth - wAdjust
    #Adjust Image Height to only extract tags
    hAdjust = oHeight * adjusts[1]
    tAdjust = hAdjust
    bAdjust = oHeight - hAdjust
    adjusted_image = image.crop((lAdjust, bAdjust, rAdjust, tAdjust))
    #adjusted_image.show()
    
    #adjusted_image = adjusted_image.convert('RBG')
    #adjusted_image.show()
    
    #This destroys the image and only produces contrasting differences
    pixel_data = adjusted_image.load()
    for y in range(adjusted_image.size[1]):
        for x in range(adjusted_image.size[0]):
            if pixel_data[x,y][0] < 90:
                pixel_data[x,y] = (0, 0, 0, 255)
    
    for y in range(adjusted_image.size[1]):
        for x in range(adjusted_image.size[0]):
            if pixel_data[x,y][1] < 136:
                pixel_data[x,y] = (0, 0, 0, 255)
    
    for y in range(adjusted_image.size[1]):
        for x in range(adjusted_image.size[0]):
            if pixel_data[x,y][2] > 0:
                pixel_data[x,y] = (255, 255, 255, 255)

    adjusted_image.save("input-black.gif", "GIF")
    adjusted_image = Image.open("input-black.gif")
    bigger = adjusted_image.resize((1000,500), Image.NEAREST)
    ext = '.gif'
    bigger.save("input-NEAREST" + ext)
    adjusted_image = np.asarray(adjusted_image)
    return adjusted_image
