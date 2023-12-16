import math
import cv2

from segment import Segment


class Piece:
    def __init__(self, contour):
        self.contour = contour
        self.points = [tuple(x[0]) for x in contour.tolist()]
        self.center = self.getCenter()
        self.corners = self.getCorners()
        self.segments = self.getSegments()

    def getCenter(self):
        M = cv2.moments(self.contour)
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
        return cx, cy    

    def getExtremePoints(self):
        # get contour points which are further from center than their neighbors
        distances = [math.dist(self.center, p) for p in self.points]
        extremes = []
        lookupSize = 20
        for i in range(len(self.points)):
            isExtreme = True
            for j in range(i - lookupSize, i + lookupSize):
                if distances[j % len(distances)] > distances[i]:
                    isExtreme = False
                    break
            if isExtreme:
                extremes.append(self.points[i])
        return extremes

    def getCorners(self):
        extremes = self.getExtremePoints()
        furthestExtreme = max(extremes, key=lambda p: math.dist(self.center, p))
        mirrorPoint = (2*self.center[0] - furthestExtreme[0], 2*self.center[1] - furthestExtreme[1])
        closestToMirrorPointExtreme = min(extremes, key=lambda p: math.dist(mirrorPoint, p))
        extremes.remove(furthestExtreme)
        extremes.remove(closestToMirrorPointExtreme)
        return extremes

    def getSegments(self):
        current = []
        segments = []
        for i in range(len(self.points)):
            current.append(self.points[i])
            if self.points[i] in self.corners:            
                segments.append(current)
                current = []

        if len(current) > 0:
            segments[0] = current + segments[0]
        
        return [Segment(self, segment) for segment in segments]
    
    def setSegmentIndex(self):
        sorted(self.segments, key=lambda segment: (segment.center[1], segment.center[0]))
        # iterate and set index to segment.index
        for i in range(len(self.segments)):
            self.segments[i].index = i
