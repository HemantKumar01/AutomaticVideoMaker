import imageFilters as imf
import cv2
import numpy as np
import threading
import sys
from progress.bar import ChargingBar

sys.setrecursionlimit(10**9)
threading.stack_size(10**8)

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


def setVideoWriter(name, fourcc, size, isColor=True):
    global videoWriter
    videoWriter = cv2.VideoWriter(f"{name}.avi", fourcc, 60, size, isColor)


def addToVideo(img):
    videoWriter.write(img)


def completeVideo():
    cv2.destroyAllWindows()
    videoWriter.release()


def createAnime(img_path: str, backgroundColor=[255, 255, 255], foregroundColor=[56, 50, 36]):
    global foreground, background, img, height, width, channel, done, bar
    foreground = foregroundColor
    background = backgroundColor

    image = cv2.imread(img_path)
    image = imf.createLineDrawing(image, foreground, background)

    img = image
    (height, width, channel) = img.shape

    blank_image = np.zeros([height, width, channel], img.dtype)
    blank_image.fill(255)

    done = np.zeros([height, width], img.dtype)

    bar = ChargingBar('Processing and Saving : ', max=(
        height*width))  # showing progress bar

    setVideoWriter("output", cv2.VideoWriter_fourcc(*'MJPG'), (width, height))
    threading.Thread(target=showAllForegrounds, args=(blank_image,)).start()


def searchNeighbour(blank_image, x, y):

    global done, countDone, bar, background, foreground

    done[y, x] = 1

    if list(img[y, x]) == background:
        return

    countDone += 1

    # print(f"size:{height*width} done:{countDone}")
    blank_image[y, x] = foreground

    # add frame to video after a change of 4 pixels
    if (countDone % 4 == 0):
        addToVideo(blank_image)  # *now blank_image is a modified image

    if x - 1 >= 0 and not(done[y, x - 1]):
        searchNeighbour(blank_image, x - 1, y)
    if x + 1 <= width - 1 and not(done[y, x + 1]):
        searchNeighbour(blank_image, x + 1, y)
    if y - 1 >= 0 and not(done[y - 1, x]):
        searchNeighbour(blank_image, x, y - 1)
    if y + 1 <= height - 1 and not(done[y + 1, x]):
        searchNeighbour(blank_image, x, y + 1)


def showAllForegrounds(blank_image):
    global done, countDone, bar

    for i in range(height):
        for j in range(width):
            bar.next()
            if not(done[i, j]) and list(img[i, j]) != background:
                searchNeighbour(blank_image, j, i)
    bar.finish()


createAnime("image.jfif")
