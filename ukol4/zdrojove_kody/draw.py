from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from edge import *
from typing import List
from qpointFB import *
import csv

class Draw(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.polA: List[QPointFB] = []
        self.polB: List[QPointFB] = []
        self.res: List[Edge] = []
        self.addA = True


    def switchPolygon(self):
        self.addA = not self.addA

    def getPolygons(self):
        return self.polA, self.polB

    def setResults(self, edges):
        self.res = edges

    def clearResults(self):
        self.res.clear()

    def clearCanvas(self):
        self.polA.clear()
        self.polB.clear()
        self.res.clear()

    def setPath(self):
        # Return input data
        # Store filename
        filename = QFileDialog.getOpenFileName(None, "Select TXT", "", "TXT files (*.txt)")

        # Return data inserted in case no new data are chosen
        if bool(filename[0]) == False:
            return self.polA, self.polB


        # Return empty list if new data are chosen
        if self.addA:
            if self.polA != []:
                self.polA = []

        else:
            if self.polB != []:
                self.polB = []

        # Store the path
        path = filename[0]

        # Initialise x, y-coordinates lists
        x = []
        y = []

        # Read txt/csv file
        with open(path, 'r') as f:
            for row in csv.reader(f, delimiter='\t'):

                # Extract x,y coordinates
                x.append(row[0])
                y.append(row[1])


        if self.addA:
            for i in range(len(x)):
                point = QPointFB(float(x[i]), float(y[i]))
                self.polA.append(point)

            return self.polA

        else:
            for i in range(len(x)):
                point = QPointFB(float(x[i]), float(y[i]))
                self.polB.append(point)

            return self.polB

    def mousePressEvent(self, e: QMouseEvent):
        # Get position
        x = e.position().x()
        y = e.position().y()

        # Create point
        p = QPointFB(int(x), int(y))

        # Add point to particular polygon
        if self.addA:
            self.polA.append(p)
        else:
            self.polB.append(p)

        #print(self.polB)
        # Repaint
        self.repaint()

    def paintEvent(self, e: QPaintEvent):

        # Create graphic object
        qp = QPainter(self)

        # Start draw
        qp.begin(self)

        # Set pen for polygon A and B, separately
        penA = QPen(QColor(30,144,255,127))
        penA.setWidth(5)

        penB = QPen(QColor(220,20,60,127))
        penB.setWidth(5)

        # Copy points from polygon A to QPolygonF A
        q_polA = QPolygonF()
        for p in self.polA:
            q_polA.append(p)

        # Draw polygon A
        qp.setPen(penA)
        qp.drawPolygon(q_polA)

        # Copy points from polygon B to QPolygonF B
        q_polB = QPolygonF()
        for p in self.polB:
            q_polB.append(p)

        # Draw polygon B
        qp.setPen(penB)
        qp.drawPolygon(q_polB)

        #Draw results
        penR = QPen(QColor(154,205,50))
        penR.setWidth(5)
        qp.setPen(penR)
        for e in self.res:
            qp.drawLine(e.getStart(), e.getEnd())
        
        # End draw
        qp.end()





