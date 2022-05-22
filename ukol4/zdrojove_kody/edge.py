from PyQt6.QtCore import *
from qpointFB import *

#Oriented edge
class Edge:
    def __init__(self, start: QPointFB, end: QPointFB):
        self.start = start
        self.end = end

    def getStart(self):
        #Return start point
        return self.start

    def getEnd(self):
        # Return end point
        return self.end
