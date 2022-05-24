from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from random import *
import csv

from typing import List
from qpoint3d import *
from edge import *

class Draw (QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.points : List[QPoint3D] = []       #Input points
        self.dt : List[Edge] = []               #Delaunay edges
        self.cont_lines : List[Edge] = []       #Contour lines
        self.slopes : List[float] = []          #Slope
        self.exposition : List[float] = []      #Exposition
        self.maximum_XN = 0                     #Maximum of x-coordinates
        self.maximum_YN = 0                     #Maximum of y-coordinates
        self.intervalCL = 0                     #Contourline interval step

    def getPoints(self):
        return self.points

    def getTranformationParameters(self):
        return self.maximum_XN, self.maximum_YN

    def getDT(self):
        return self.dt

    def setDT(self, dt):
        self.dt = dt

    def setCL(self, cont_lines):
        self.cont_lines = cont_lines

    def setIntervalCL(self, interval_step):
        self.intervalCL = interval_step

    def setSlope(self, slopes):
        self.slopes = slopes
        self.exposition = []

    def setExposition(self, exposition):
        self.exposition = exposition
        self.slopes = []

    def setPath(self, width, height):
        # Return input data
        # Store filename
        filename = QFileDialog.getOpenFileName(None, "Select TXT/CSV", "", "TXT files (*.txt *.csv)")

        # Return data inserted in case no new data are chosen
        if bool(filename[0]) == False:
            return self.points

        # Return empty list if new data are chosen
        if self.points != []:
            self.points = []

        # Store the path
        path = filename[0]

        # Initialise and extract x,y,z coordinates from input
        x = []
        y = []
        z = []

        # Read txt/csv file
        with open(path, 'r') as f:
            if 'csv' in path:
                for row in csv.reader(f, delimiter=';'):
                    # Extract x,y,z coordinates
                    x.append(row[0])
                    y.append(row[1])
                    z.append(row[2])
            else:
                for row in csv.reader(f, delimiter='\t'):

                    # Extract x,y,z coordinates
                    x.append(row[0])
                    y.append(row[1])
                    z.append(row[2])

        # Convert string to float
        try:
            for i in range(len(x)):
                x[i] = float(x[i])
                y[i] = float(y[i])
                z[i] = float(z[i])
        except:
            # Delete header
            del x[0]
            del y[0]
            del z[0]
            for i in range(len(x)):
                x[i] = float(x[i])
                y[i] = float(y[i])
                z[i] = float(z[i])

        # Store minimum for x,y coordinates
        self.minimum_X = min(x)
        self.minimum_Y = min(y)

        # Shift coordinates to the origin
        for i in range(len(x)):
            x[i] = (x[i] - self.minimum_X)
            y[i] = (y[i] - self.minimum_Y)

        # Store extent of x,y coordinates
        self.maximum_XN = max(x)
        self.maximum_YN = max(y)

        # Normalise to the interval [0,1]
        for i in range(len(x)):
            x[i] = int(x[i] / self.maximum_XN * width)

            # Subtract from Canvas height for axial symmetry
            y[i] = int(height - (y[i] / self.maximum_YN * height))

            # Store x,y,z coordinates in one QPoint3D
            p = QPoint3D(x[i], y[i], z[i])

            # Add point to the list
            self.points.append(p)

        return self.points

    def paintEvent(self, e: QPaintEvent):
        # Create new object
        qp = QPainter(self)

        # Start draw
        qp.begin(self)

        # Set pen and brush
        qp.setPen(Qt.GlobalColor.black)
        qp.setBrush(Qt.GlobalColor.white)

        # Draw points
        radius = 3
        for p in self.points:
            qp.drawEllipse(int(p.x()- radius), int(p.y()) - radius, 2 * radius, 2 * radius)

        #Draw Delaunay edges
        qp.setPen(Qt.GlobalColor.black)
        for e in self.dt:
            qp.drawLine(int(e.getStart().x()), int(e.getStart().y()), int(e.getEnd().x()), int(e.getEnd().y()))
            #qp.drawLine(QPointF(e.getStart()), QPointF(e.getEnd()))

        # Draw contour lines
        pen = QPen(QColor(150, 75, 0, 255))
        qp.setPen(pen)

        for e in self.cont_lines:

            # Get altitude of contour line
            z = e.getStart().getZ()

            # Highlight every fifth conout line
            if z % (5*self.intervalCL) == 0:
                pen.setWidth(2)
                qp.setPen(pen)
                qp.drawLine(int(e.getStart().x()), int(e.getStart().y()),
                            int(e.getEnd().x()), int(e.getEnd().y()))

            else:
                pen.setWidth(1)
                qp.setPen(pen)
                qp.drawLine(int(e.getStart().x()), int(e.getStart().y()),
                            int(e.getEnd().x()), int(e.getEnd().y()))

        # Colour Delaunay triangles by slope
        if len(self.slopes) > 0:
            # Draw slopes
            qp.setPen(Qt.GlobalColor.transparent)
            idx_slope = 0
            for i in range(0, len(self.dt), 3):
                pol = QPolygon()
                p1 = self.dt[i].getStart()
                p1 = QPoint(int(p1.x()), int(p1.y()))
                p2 = self.dt[i + 1].getStart()
                p2 = QPoint(int(p2.x()), int(p2.y()))
                p3 = self.dt[i + 2].getStart()
                p3 = QPoint(int(p3.x()), int(p3.y()))

                pol.append(p1)
                pol.append(p2)
                pol.append(p3)

                if self.slopes[idx_slope] >= 0 and self.slopes[idx_slope] < 2:
                    qp.setBrush(QColor(229, 229, 229, 127)) #lightgreen semi-transparent

                if self.slopes[idx_slope] >= 2 and self.slopes[idx_slope] < 4:
                    qp.setBrush(QColor(204, 204, 204, 127))   #limegreen semi-transparent

                if self.slopes[idx_slope] >= 4 and self.slopes[idx_slope] < 6:
                    qp.setBrush(QColor(178, 178, 178, 127))     #green semi-transparent

                if self.slopes[idx_slope] >= 6 and self.slopes[idx_slope] < 8:
                    qp.setBrush(QColor(153, 153, 153, 127))     #darkgreen semi-transparent

                if self.slopes[idx_slope] >= 8 and self.slopes[idx_slope] < 10:
                    qp.setBrush(QColor(127, 127, 127, 127)) #orange semi-transparent

                if self.slopes[idx_slope] >= 10 and self.slopes[idx_slope] < 14:
                    qp.setBrush(QColor(102, 102, 102, 127))   #darkorange semi-transparent

                if self.slopes[idx_slope] >= 15 and self.slopes[idx_slope] < 20:
                    qp.setBrush(QColor(76, 76, 76, 127))  #coral semi-transparent

                if self.slopes[idx_slope] >= 20 and self.slopes[idx_slope] < 25:
                    qp.setBrush(QColor(51, 51, 51, 127))  #tomato semi-transparent

                if self.slopes[idx_slope] >= 25 and self.slopes[idx_slope] < 90:
                    qp.setBrush(QColor(25, 25, 25, 127))   #orange-red semitransparent

                qp.drawPolygon(pol)
                idx_slope += 1

        # Colour Delaunay triangles by exposition
        if len(self.exposition) > 0:
            # Draw slopes
            qp.setPen(Qt.GlobalColor.transparent)
            idx_exp = 0
            for i in range(0, len(self.dt), 3):
                pol = QPolygon()
                p1 = self.dt[i].getStart()
                p1 = QPoint(int(p1.x()), int(p1.y()))
                p2 = self.dt[i + 1].getStart()
                p2 = QPoint(int(p2.x()), int(p2.y()))
                p3 = self.dt[i + 2].getStart()
                p3 = QPoint(int(p3.x()), int(p3.y()))

                pol.append(p1)
                pol.append(p2)
                pol.append(p3)

                if -112.5 <= self.exposition[idx_exp] < -67.5:
                    qp.setBrush(QColor(255, 0, 0, 127))         #red semi-transparent North

                elif -157.5 <= self.exposition[idx_exp] < -112.5:
                    qp.setBrush(QColor(255, 165, 0, 127))       #orange semi-transparent Northeast

                elif self.exposition[idx_exp] < -157.5 or self.exposition[idx_exp] >= 157.5:
                    qp.setBrush(QColor(255, 255, 0, 127))       #yellow semi-transparent East

                elif 112.5 <= self.exposition[idx_exp] < 157.5:
                    qp.setBrush(QColor(0, 255, 0, 127))         #lime semi-transparent Southeast

                elif 67.5 <= self.exposition[idx_exp] < 112.5:
                    qp.setBrush(QColor(0, 191, 255, 127))       #deepskyblue semi-transparent South

                elif 22.5 <= self.exposition[idx_exp] < 67.5:
                    qp.setBrush(QColor(100, 149, 237, 127))     #cornflowerblue semi-transparent Southwest

                elif -22.5 <= self.exposition[idx_exp] < 22.5:
                    qp.setBrush(QColor(0, 0, 255, 127))         #blue semi-transparent West

                elif -67.5 <= self.exposition[idx_exp] < 22.5:
                    qp.setBrush(QColor(255, 0, 255, 127))       #magenta semi-transparent Northwest


                qp.drawPolygon(pol)
                idx_exp += 1

        # End draw
        qp.end()