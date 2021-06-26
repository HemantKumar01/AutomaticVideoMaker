import cv2
import numpy as np
import imutils
import time
import sys

sys.setrecursionlimit(1000000000)


def createSketch(img, blurX=21, blurY=21):
    img = imutils.resize(img, height=600)
    grayImage = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    invertedGrayImage = 255 - grayImage

    blurred_gray = cv2.GaussianBlur(invertedGrayImage, (blurX, blurY), 0)
    inverted_blurred = 255 - blurred_gray

    image = cv2.divide(grayImage, inverted_blurred, scale=256.0)

    return image


def createLineDrawing(img, foreroundBGR=[0, 0, 0], backgroundBGR=[255, 255, 255]):
    time1 = time.time()

    img = createSketch(img)

    result = np.zeros((img.shape[0], img.shape[1], 3), img.dtype)
    for y in range(len(img)):
        result[y] = [(foreroundBGR if pixel <= 240 else backgroundBGR)
                     for pixel in img[y]]

    print(
        f'createLineDrawing() took: {time.time() - time1} seconds')
    return result
