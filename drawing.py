import random
import cv2


def drawContours(img, contours, fill=True):
    # draw contours with fill to binary image
    img = cv2.drawContours(img, contours, -1, (0, 255, 0), cv2.FILLED if fill else 3)
    return img

def drawPieces(img, pieces):
    for piece in pieces:
        img = drawPiece(img, piece)
    return img

def drawPiece(img, piece):
    for segment in piece.segments:        
        img = drawPoints(img, segment.points, getRandomRgbColor())   
    img = drawPoints(img, piece.corners, (0, 0, 255))
    img = drawPoints(img, [piece.center], (255, 0, 0))
    return img

def drawSegmentIds(img, pieces):
    for piece in pieces:
        for segment in piece.segments:
            img = cv2.putText(img, f"{segment}{'UP' if segment.isUp else 'D'}", (int(segment.center[0]), int(segment.center[1])), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
    return img

def drawCanonicalSegment(img, segment):
    color = getRandomRgbColor()
    diplayPoints = segment.getDisplayPoints()
    for i in range(len(diplayPoints)):
        img = cv2.circle(img, (int(diplayPoints[i][0]), int(diplayPoints[i][1])), 1, color, -1)
    return img

def getRandomRgbColor():
    return (random.randint(0,255), random.randint(0,255), random.randint(0,255))

def drawPoints(img, points, color):
    for point in points:
        img = cv2.circle(img, point, 5, color, -1)
    return img