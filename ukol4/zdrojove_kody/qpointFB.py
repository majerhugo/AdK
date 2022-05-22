from pointandpolygonposition import *
from PyQt6.QtCore import *

class QPointFB(QPointF):
    def __init__(self, x: float, y: float, alpha: float = 0, beta: float = 0, pos = PointAndPolygonPosition.Inside):
        super().__init__(x, y)
        self.alpha = alpha
        self.beta = beta
        self.pos = PointAndPolygonPosition.Inside

    def getAlpha(self):
        return self.alpha

    def getBeta(self):
        return self.beta

    def setPosition(self, pos):
        self.pos = pos

    def getPosition(self):
        return self.pos
