from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
import shapefile

class Draw (QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pol = []
        self.res = []

    def setPath(self, width, height):
        # Store the filename data
        filename = QFileDialog.getOpenFileName(None, "Select SHP", "", "SHP files (*.shp)")

        # Return previous polygon if dialog box cancelled
        if bool(filename[0]) == False:
            return self.pol

        # Store the path
        path = filename[0]

        # Read shapefile from path
        sf = shapefile.Reader(path)
        polygons = sf.shapes()

        # Initialise and extract x,y coordinates from .shp
        x = []
        y = []
        for k in range(len(sf)):
            pol_x = []
            pol_y = []
            for point in polygons[k].points:
                pol_x.append(point[0])
                pol_y.append(point[1])
            x.append(pol_x)
            y.append(pol_y)

        # Rescale loaded shapefile to screen resolution
        # Get minimum for x, y coordinates
        flat_x = []
        flat_x = [item for sublist in x for item in sublist]
        flat_y = []
        flat_y = [item for sublist in y for item in sublist]
        minimum_x = min(flat_x)
        minimum_y = min(flat_y)

        # Shift to the origin
        for i in range(len(x)):
            for j in range(len(x[i])):
                x[i][j] = (x[i][j] - minimum_x)
                y[i][j] = (y[i][j] - minimum_y)

        # Get the interval extent
        flat_xn = []
        flat_xn = [item for sublist in x for item in sublist]
        flat_yn = []
        flat_yn = [item for sublist in y for item in sublist]
        max_xn = max(flat_xn)
        max_yn = max(flat_yn)

        # Initialise the length of pol
        self.pol = [0] * len(x)

        # Normalise to the interval [0,1]
        for i in range(len(x)):
            self.pol[i] = QPolygon()
            for j in range(len(x[i])):
                x[i][j] = int(x[i][j] / max_xn * width)

                # Subtract from Canvas height for axial symmetry
                y[i][j] = int(height - (y[i][j] / max_yn * height))
                p = QPoint(x[i][j], y[i][j])
                self.pol[i].append(p)

        return self.pol

    def getPolygon(self):
        return self.pol

    def setResult(self, res: QPolygon):
        self.res.append(res)

    def paintEvent(self, e: QPaintEvent):
        # Paint action
        # Create new Painter object
        qp = QPainter(self)

        # Paint start
        qp.begin(self)

        # Loop through polygons in polygon list
        for polygon in self.pol:
            # Set color for all polygons
            qp.setPen(Qt.GlobalColor.blue)
            qp.setBrush(Qt.GlobalColor.white)

            # Paint polygons
            qp.drawPolygon(polygon)

        # Set pen and brush - result
        for result in self.res:
            qp.setPen(Qt.GlobalColor.magenta)
            qp.setBrush(Qt.BrushStyle.NoBrush)

            qp.drawPolygon(result)

        # Paint end
        qp.end()



