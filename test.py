import cv2
import numpy as np
import contourFinder
from piece import Piece


inputFilePath = "data/puzzle_sample_1.jpg"

originalImg = cv2.imread(inputFilePath) 
contours = contourFinder.findContours(originalImg)

pieces = [Piece(contour) for contour in contours]

# list number of points in each piece segment
for piece in pieces:
    for segment in piece.segments:
        npPoints = np.asarray([(np.float32(p[0]), np.float32(p[1])) for p in segment.getComparisonPoints()])
        print(f"{len(segment.getComparisonPoints())} {len(cv2.approxPolyDP(npPoints, 3, False))}")