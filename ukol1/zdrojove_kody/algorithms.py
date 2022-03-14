from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from math import *

class Algorithms:
    def __init__(self):
        pass

    def getPointAndLinePosition(self, a: QPoint, p1: QPoint, p2: QPoint):
        # Analyse position point and line
        eps = 1.0e-10

        # Coordinate differences
        ux = p2.x() - p1.x()
        uy = p2.y() - p1.y()
        vx = a.x() - p1.x()
        vy = a.y() - p1.y()

        # Calculating determinant
        t = ux*vy - vx*uy

        # Point in left halfplane
        if t > eps:
            return 1

        # Point in right halfplane
        if t < -eps:
            return 0

        # Colinear point
        return -1

    def get2LinesAngle(self, p1: QPoint, p2: QPoint, p3: QPoint, p4: QPoint):
        # Get angle between 2 vectors
        ux = p2.x() - p1.x()
        uy = p2.y() - p1.y()
        vx = p4.x() - p3.x()
        vy = p4.y() - p3.y()

        # Dot product
        uv = ux*vx + uy*vy

        # Norms
        nu = (ux**2 + uy**2)**0.5
        nv = (vx**2 + vy**2)**0.5

        # Point on the vertex
        if nu == 0 or nv == 0:
            return 0

        # Round down to 1 if greater
        if uv/(nu*nv) > 1:
            return abs(acos(1))

        # Angle
        return abs(acos(uv/(nu*nv)))

    def windingNumber(self, q:QPoint, pol:QPolygon) -> int:
        # Analyse position of the point and polygon
        # Initialise n and omega_sum
        n = len(pol)
        omega_sum = 0

        # Loop through polygon list
        for i in range(n-1):
            pos = self.getPointAndLinePosition(q, pol[i], pol[(i+1)])
            omega = self.get2LinesAngle(q, pol[i], q, pol[(i+1)])

            if pos == 1:
            # Point in the left halfplane
                omega_sum += omega

            elif pos == 0:
            # Point in the right halfplane
                omega_sum -= omega

            else:
                # Colinear point
                # Investigate if point on the boundary / vertex
                if (q.x()-pol[i].x() )* (q.x()-pol[i+1].x()) <= 0 and (q.y()-pol[i].y()) * (q.y()-pol[i+1].y()) <= 0:
                    return 1

        # Calculate Winding Number
        # Point q inside polygon
        epsilon = 1.0e-10
        if abs(abs(omega_sum)-2*pi) < epsilon:
            return 1

        # Point q outside polygon
        return 0

    def reducedRayCrossing(self, q: QPoint, pol: QPolygon) -> int:
        # Apply Q-reduction and Ray Crossing algorithm
        # Initialise polygon length & intersection counters
        n = len(pol)
        k_l = 0
        k_r = 0

        # Reduce coordinate system against q as origin
        for i in range(n-1):

            # Solve for point on the vertex
            if q.x() == pol[i].x() and q.y() == pol[i].y():
                return 1

            # Solve for regular situation
            ux_r = pol[i].x() - q.x()
            uy_r = pol[i].y() - q.y()
            vx_r = pol[i+1].x() - q.x()
            vy_r = pol[i+1].y() - q.y()

            # Right ray
            if (uy_r > 0) != (vy_r > 0):
                x_m = (ux_r * vy_r - vx_r * uy_r) / (uy_r - vy_r)
                if x_m > 0:
                    k_r += 1

            # Left ray
            if (uy_r < 0) != (vy_r < 0):
                x_m = (ux_r * vy_r - vx_r * uy_r) / (uy_r - vy_r)
                if x_m < 0:
                    k_l += 1

        # Point on boundary
        if (k_l % 2) != (k_r % 2):
            return 1

        # Point inside the polygon
        if (k_r%2) != 0:
            return 1

        # Point outside the polygon
        return 0












