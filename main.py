import cv2
import numpy as np
import contourFinder
import drawing
from piece import Piece


def showImage(src):
    cv2.namedWindow("Image", cv2.WINDOW_NORMAL)
    cv2.imshow("Image", src)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def createBlankImageInSizeOf(img):
    return createBlankImage(img.shape[1], img.shape[0])

def createBlankImage(width, height):
    return np.zeros((height,width,3), np.uint8)

def saveImage(img, name):
    cv2.imwrite("data/" + name + ".jpg", img)

inputFilePath = "data/puzzle_sample_1.jpg"

originalImg = cv2.imread(inputFilePath) 
contours = contourFinder.findContours(originalImg)

blank = createBlankImageInSizeOf(originalImg)

def setPieceIndex(pieces):
    sorted(pieces, key=lambda piece: (piece.center[1], piece.center[0]))
    # iterate and set index to piece.index
    for i in range(len(pieces)):
        pieces[i].index = i

pieces = [Piece(contour) for contour in contours][:8]
setPieceIndex(pieces)
for piece in pieces:
    piece.setSegmentIndex()

# get all pairs of pieces
piecePairs = []
for i in range(len(pieces)):
    for j in range(i+1, len(pieces)):
        piecePairs.append((pieces[i], pieces[j]))

# get all pairs of segments
segmentPairs = []
for piecePair in piecePairs:
    for segment1 in piecePair[0].segments:
        for segment2 in piecePair[1].segments:
            if segment1.isUp != segment2.isUp:
                segmentPairs.append((segment1, segment2))

# similarity test: https://stackoverflow.com/questions/70829034/how-to-compare-two-poly-lines-for-equality
def point_to_polyline_dist(p, polyline):
    polyline = [(np.float32(p[0]), (np.float32(p[1]))) for p in polyline]
    cnt = np.concatenate((polyline, polyline[::-1]))
    return np.abs(cv2.pointPolygonTest(cnt, (int(p[0]),int(p[1])), True))

def polyline_dist(polyline1, polyline2):
    return np.mean([point_to_polyline_dist(p, polyline2)**2 for p in polyline1])

def calculateDistanceFromSegment(segment, point):
    # https://stackoverflow.com/questions/849211/shortest-distance-between-a-point-and-a-line-segment
    x1, y1 = segment.points[0]
    x2, y2 = segment.points[-1]
    x3, y3 = point
    px = x2-x1
    py = y2-y1
    norm = px*px + py*py
    u =  ((x3 - x1) * px + (y3 - y1) * py) / float(norm)
    if u > 1:
        u = 1
    elif u < 0:
        u = 0
        

    

def getSimilarity(segmentPair):
    return polyline_dist(segmentPair[0].getComparisonPoints(), segmentPair[1].getComparisonPoints())

# store similarity along with segment pair
segmentPairs = [(segmentPair, getSimilarity(segmentPair)) for segmentPair in segmentPairs]
segmentPairs.sort(key=lambda x: x[1])

# list first 10 segment pairs
for i in range(len(segmentPairs)):
    print(f"{segmentPairs[i][0][0]} - {segmentPairs[i][0][1]}: {segmentPairs[i][1]}")


contourImage = drawing.drawContours(blank, contours, True)
showImage(contourImage)
cv2.imwrite("data/contours.jpg", contourImage)

piecesImg = drawing.drawPieces(createBlankImageInSizeOf(originalImg), pieces)
drawing.drawSegmentIds(piecesImg, pieces)
showImage(piecesImg)

segmentImage = createBlankImage(3000, 2000)
for piece in pieces:
    for segment in piece.segments:
        drawing.drawCanonicalSegment(segmentImage, segment)

showImage(segmentImage)

saveImage(segmentImage, "segments")



