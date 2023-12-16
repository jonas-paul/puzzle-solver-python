import cv2
import numpy as np


def threshold(img):
    # convert to grayscale
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # apply thresholding
    _, img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
    return img

def removeNoise(img):
    img = threshold(img)
    img = cv2.medianBlur(img, 5)

    # erode and dilate
    kernel = np.ones((5,5), np.uint8)
    img = cv2.erode(img, kernel, iterations=1)
    img = cv2.dilate(img, kernel, iterations=1)
    return img

def findContours(img):
    img = removeNoise(img)
    edged = cv2.Canny(img, 30, 200)
    contours, hierarchy = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    filteredContours = list(filter(lambda c: cv2.contourArea(c) > 1000, contours))
    return filteredContours