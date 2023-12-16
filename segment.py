import numpy as np


class Segment:
    def __init__(self, piece, points):
        self.piece = piece
        self.nominalHalfSize = 1000
        self.points = points
        self.baseLength = self.calculateBaseLength()
        self.center = self.calculateCenter()
        self.angle = self.calculateAngle()
        self.relativeSize = self.calculateRelativeSize()
        self.normalizedPoints = self.getNormalizedPoints()
        self.isUp = self.isUp()

    def __str__(self) -> str:
        return f"P{self.piece.index}S{self.index}"

    def calculateBaseLength(self):
        return np.sqrt((self.points[0][0]-self.points[-1][0])**2 + (self.points[0][1]-self.points[-1][1])**2)
    
    def calculateCenter(self):
        return ((self.points[0][0] + self.points[-1][0]) / 2, (self.points[0][1] + self.points[-1][1]) / 2)
    
    def calculateAngle(self):
        self.angle = np.arctan2(self.points[-1][1] - self.points[0][1], self.points[-1][0] - self.points[0][0])

        base = self.calculateBaseLength()
        self.angleSin = -(self.points[-1][1] - self.points[0][1]) / base
        self.angleCos = (self.points[-1][0] - self.points[0][0]) / base

        return self.angle
    
    def getNormalizedPoints(self):
        angleSin = np.sin(-self.angle)
        angleCos = np.cos(-self.angle)
        translatedPoints = self.translatePoints(self.points, -self.center[0], -self.center[1])
        rotatedPoints = [(x[0]*angleCos - x[1]*angleSin, x[0]*angleSin + x[1]*angleCos) for x in translatedPoints]
        scale = 1 / self.relativeSize
        scaledPoints = [(x[0]*scale, x[1]*scale) for x in rotatedPoints]
        self.setYOfEnpointsToZero(scaledPoints)
        return scaledPoints
    
    def calculateRelativeSize(self):
        return self.baseLength / (2 * self.nominalHalfSize)
    
    def isUp(self):
        return np.mean([x[1] for x in self.normalizedPoints]) > 0
    
    def getComparisonPoints(self):
        if not self.isUp:
            return self.normalizedPoints
        return [(-x[0], -x[1]) for x in self.normalizedPoints]
    
    def translatePoints(self, points, dx, dy):        
        return [(x[0] + dx, x[1] + dy) for x in points]
    
    def setYOfEnpointsToZero(self, points):
        if abs(points[0][1]) < 10E-12 and abs(points[0][0] + self.nominalHalfSize) < 10E-12:
            points[0] = (-self.nominalHalfSize, 0)
        if abs(points[-1][1]) < 10E-12 and abs(points[-1][0] - self.nominalHalfSize) < 10E-12:
            points[-1] = (self.nominalHalfSize, 0)
    
    def getDisplayPoints(self):
        return self.translatePoints(self.getComparisonPoints(), 1.5 * self.nominalHalfSize, 1.5 * self.nominalHalfSize)