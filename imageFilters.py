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
    imageBackground = False
    if isinstance(backgroundBGR, str):
        backgroundImage = cv2.imread(backgroundBGR)
        backgroundImage = cv2.resize(backgroundImage, (img.shape[1], img.shape[0]))
        imageBackground = True

    img = createSketch(img)

    result = np.zeros((img.shape[0], img.shape[1], 3), img.dtype)
    for y in range(len(img)):
        if not imageBackground:
            result[y] = [
                (foreroundBGR if pixel <= 240 else backgroundBGR) for pixel in img[y]
            ]
        else:
            result[y] = [
                (foreroundBGR if img[y][z] <= 240 else backgroundImage[y][z])
                for z in range(len(img[y]))
            ]
    print(f"createLineDrawing() took: {time.time() - time1} seconds")
    return result


# inputImg = cv2.imread("./demo1.jpg")
# img1 = createLineDrawing(inputImg, [43, 47, 54], "./assets/background.jpg")
# img2 = createSketch(inputImg)

# cv2.imwrite("image1.jpg", img1)
# cv2.imwrite('image2.jpg', img2)
