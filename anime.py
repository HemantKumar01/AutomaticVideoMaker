from numpy.core.numeric import NaN
import imageFilters as imf
import cv2
import numpy as np
import threading
import sys
from progress.bar import ChargingBar
from math import floor

sys.setrecursionlimit(10**9)
threading.stack_size(10**8)

blank_image = None
background = [255, 255, 255]
foreground = [0, 0, 0]
img = np.zeros((1, 1, 3), np.uint8)
height = 0
width = 0
channel = 0

done = []
countDone = 0
videoWriter = None
bar = None

duration = 12
skipFrames = 20
numFrames = 0
frameRate = 30  # default = 30 ; see it's changing according to numFrames in the function setVideoWriter


def setVideoWriter(name, fourcc, size, isColor=True):
    global videoWriter, numFrames, duration, skipFrames, frameRate
    frameRate = floor(numFrames / (skipFrames * duration))
    videoWriter = cv2.VideoWriter(f"{name}", fourcc, frameRate, size, isColor)


def addToVideo(img):
    videoWriter.write(img)


def completeVideo():
    cv2.destroyAllWindows()
    videoWriter.release()


def createAnime(
    img_path: str,
    outputName="output.avi",
    backgroundColor=[255, 255, 255],
    foregroundColor=[56, 50, 36],
):
    global foreground, background, img, height, width, channel, done, bar, numFrames, blank_image
    foreground = foregroundColor
    background = backgroundColor

    image = cv2.imread(img_path)
    image = imf.createLineDrawing(image, foreground, background)

    img = image
    (height, width, channel) = img.shape

    numFrames = np.count_nonzero(np.all(img == foreground, axis=2))
    if isinstance(background, str):
        blank_image = cv2.imread(background)
        blank_image = cv2.resize(blank_image, (width, height))
    else:
        blank_image = np.full([height, width, channel], background, dtype=img.dtype)

    done = np.zeros([height, width], img.dtype)

    bar = ChargingBar(
        "Processing and Saving : ", max=(height * width)
    )  # showing progress bar

    setVideoWriter(outputName, cv2.VideoWriter_fourcc(*"MJPG"), (width, height))
    threading.Thread(target=showAllForegrounds, args=(outputName,)).start()


def searchNeighbour(x, y):
    global done, countDone, bar, background, foreground, blank_image

    done[y, x] = 1

    if list(img[y, x]) != foreground:
        return

    countDone += 1

    # print(f"size:{height*width} done:{countDone}")
    blank_image[y, x] = foreground

    # add frame to video after a change of {skipFrames} pixels
    if countDone % skipFrames == 0:
        addToVideo(blank_image)  # *now blank_image is a modified image

    if x - 1 >= 0 and not (done[y, x - 1]):
        searchNeighbour(x - 1, y)
    if x + 1 <= width - 1 and not (done[y, x + 1]):
        searchNeighbour(x + 1, y)
    if y - 1 >= 0 and not (done[y - 1, x]):
        searchNeighbour(x, y - 1)
    if y + 1 <= height - 1 and not (done[y + 1, x]):
        searchNeighbour(x, y + 1)


def showAllForegrounds(outputName):
    global done, countDone, bar, blank_image, frameRate, duration, background, foreground, height, width

    for i in range(height):
        for j in range(width):
            bar.next()
            if not (done[i, j]) and list(img[i, j]) == foreground:
                searchNeighbour(j, i)
    bar.finish()

    print("Almost done! Finalizing Video File...")
    # adding the final image to appear for about 2 seconds;
    for i in range(frameRate * 2):
        addToVideo(blank_image)
    print(f"Congratulations! video saved with following details-")
    print(
        f"""------------------------------------------------------
Name: {outputName},     frameRate: {frameRate} frames/sec,
duration: {duration}sec,   height: {height}px,     width:{width}px,
backgroundColor: {background} ([b,g,r] or path),
foregroundColor: {foreground} ([b,g,r])
-------------------------------------------------------"""
    )


# (inputImageName, outputVideoName)
createAnime(
    "./image3.png",
    "output.avi",
    backgroundColor="assets/background.jpg",
    foregroundColor=[43, 47, 54],
)


# @PARAMS:
# * inputImageName : the image path(with extension) to be processed and made into a video
# * outputVideoName : the name of the video to be saved (with .avi)
# * backgroundColor: color of background in [B,G,R] format or Background image path
# * foregroundColor: color of foreground in [B,G,R] format
