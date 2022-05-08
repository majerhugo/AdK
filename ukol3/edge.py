from PyQt6.QtCore import *
from qpoint3d import *

#Triangle edge (oriented)
class Edge:
    def __init__(self, start: QPoint3D, end: QPoint3D):
        self.start = start
        self.end = end

    def getStart(self):
        #Return start point
        return self.start

    def getEnd(self):
        # Return end point
        return self.end

    def switch(self):
        #Change edge orientation
        return Edge(self.end, self.start)

    def __eq__(self, other):
        #Compare two edges
        return self.start == other.start and self.end == other.end