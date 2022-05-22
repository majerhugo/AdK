from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from math import *
from typing import List
from qpointFB import *
from pointandlineposition import *
from pointandpolygonposition import *
from lineandlineposition import *
from booleanoperation import *
from edge import *


class Algorithms:
    def __init__(self):
        pass

    def getPointAndLinePosition(self, a: QPointFB, p1: QPointFB, p2: QPointFB):
        # Analyze position point and line
        eps = 1.0e-10

        # Coordinate differences
        ux = p2.x() - p1.x()
        uy = p2.y() - p1.y()
        vx = a.x() - p1.x()
        vy = a.y() - p1.y()

        # Calculating determinant
        t = ux * vy - vx * uy

        # Point in left halfplane
        if t > eps:
            return PointAndLinePosition.Left_HP

        # Point in right halfplane
        if t < -eps:
            return PointAndLinePosition.Right_HP

        # Collinear point
        return PointAndLinePosition.On_Line

    def get2LinesAngle(self, p1: QPointFB, p2: QPointFB, p3: QPointFB, p4: QPointFB):
        # Get angle between 2 vectors
        ux = p2.x() - p1.x()
        uy = p2.y() - p1.y()
        vx = p4.x() - p3.x()
        vy = p4.y() - p3.y()

        # Dot product
        uv = ux * vx + uy * vy

        # Norms
        nu = (ux ** 2 + uy ** 2) ** 0.5
        nv = (vx ** 2 + vy ** 2) ** 0.5

        # Angle
        return abs(acos(uv / (nu * nv)))


    def getPositionPointAndPolygon(self, q: QPointFB, pol: List[QPointFB]):
        # Analyzes position of the point and polygon
        n = len(pol)
        omega_sum = 0

        # Loop through polygon nodes
        for i in range(n):

            # Analyze position of q and pi, pi+1
            pos = self.getPointAndLinePosition(q, pol[i], pol[(i + 1) % n])

            # Angle between q and pi, pi+1
            omega = self.get2LinesAngle(q, pol[i], q, pol[(i + 1) % n])

            # Computing winding number
            if pos == PointAndLinePosition.Left_HP:
                # Point in the left halfplane
                omega_sum += omega
            else:
                # Point in the right halfplane
                omega_sum -= omega

        # Point q inside polygon
        epsilon = 1.0e-10
        if abs(abs(omega_sum) - 2 * pi) < epsilon:
            return PointAndPolygonPosition.Inside

        # Point q outside polygon
        return PointAndPolygonPosition.Outside

    def get2LinesIntersection(self, p1: QPointFB, p2: QPointFB, p3: QPointFB, p4: QPointFB):
        # Compute intersection of two lines, if exists

        # Directions
        ux = p2.x() - p1.x()
        uy = p2.y() - p1.y()
        vx = p4.x() - p3.x()
        vy = p4.y() - p3.y()
        wx = p1.x() - p3.x()
        wy = p1.y() - p3.y()

        # Coefficients k1, k2, k3
        k1 = vx * wy - vy * wx
        k2 = ux * wy - uy * wx
        k3 = vy * ux - vx * uy

        # Collinear lines
        eps = 1e-10
        if abs(k3) < eps:
            return LineAndLinePosition.Collinear, None

        # Compute alpha, beta
        alpha = k1 / k3
        beta = k2 / k3

        # Parallel lines
        if abs(k1) <= eps and abs(k2) <= eps:
            return LineAndLinePosition.Parallel, None

        # Line intersect
        if 0 <= alpha <= 1 and 0 <= beta <= 1:
            # Get point of intersection
            x = p1.x() + alpha * ux
            y = p1.y() + alpha * uy

            Q = QPointFB(x, y, alpha, beta)

            return LineAndLinePosition.Intersect, Q

        # Skew lines
        return LineAndLinePosition.Skew, None

    def updateVertices(self, polA: List[QPointFB], polB: List[QPointFB]):
        # Add line segment intersections to polygon vertices

        # Epsilon
        eps = 1.0e-10

        # Process first polygon
        i = 0
        while i < len(polA):
            # Create dictionary
            D = {}

            # Process second polygon
            j = 0
            while j < len(polB):

                # Get intersection and its status
                status, I = self.get2LinesIntersection(polA[i], polA[(i + 1) % len(polA)], polB[j],
                                                       polB[(j + 1) % len(polB)])

                # Both segments intersect each other
                if status == LineAndLinePosition.Intersect:
                    # Getting parameters alpha and beta of intersection
                    alpha = I.getAlpha()
                    beta = I.getBeta()

                    # Add intersection to dictionary
                    if eps < alpha < 1 - eps:
                        D[alpha] = I

                    # Add intersection to segment
                    if eps < beta < 1 - eps:
                        # Increment j
                        j += 1

                        # Add to polygon
                        polB.insert(j, I)

                # Increment j
                j += 1

            # Any intersection exists?
            if len(D) > 0:

                # Process all intersections
                for k, v in D.items():
                    # Increment i
                    i += 1

                    # Add intersection to polygon A
                    polA.insert(i, QPointFB(v.x(), v.y()))

            # Increment i
            i += 1

    def setEdgePosition(self, polA: List[QPointFB], polB: List[QPointFB]):
        # Setting edge positions of Polygon A according to Polygon B

        # Process edges of Polygon A
        for i in range(len(polA)):
            # Get edge midpoint
            X_m = (polA[i].x() + polA[(i + 1) % len(polA)].x()) / 2
            Y_m = (polA[i].y() + polA[(i + 1) % len(polA)].y()) / 2

            m = QPointFB(X_m, Y_m)

            # Get position of midpoint to polB
            pos = self.getPositionPointAndPolygon(m, polB)

            # Set position of ith point
            polA[i].setPosition(pos)

    def getEdges(self, pol: List[QPointFB], position: PointAndPolygonPosition, edges: List[Edge]):
        # Choose edges by position

        # Iterate through
        for i in range(len(pol)):
            # Found edge of the same position
            if pol[i].getPosition() == position:
                # Create edge
                e = Edge(pol[i], pol[(i + 1) % len(pol)])

                # Add edge to list
                edges.append(e)

    def createOverlay(self, polA: List[QPointFB], polB: List[QPointFB], operation: BooleanOperation) -> List[Edge]:
        # Execute boolean operation over 2 polygons
        edges: List[Edge] = []

        # Update vertices of both polygons
        self.updateVertices(polA, polB)

        # Calculate edge position
        self.setEdgePosition(polA, polB)
        self.setEdgePosition(polB, polA)

        # Union operation
        if operation == BooleanOperation.Union:
            self.getEdges(polA, PointAndPolygonPosition.Outside, edges)
            self.getEdges(polB, PointAndPolygonPosition.Outside, edges)

        # Intersection operation
        elif operation == BooleanOperation.Intersection:
            self.getEdges(polA, PointAndPolygonPosition.Inside, edges)
            self.getEdges(polB, PointAndPolygonPosition.Inside, edges)

        # Difference AB operation
        elif operation == BooleanOperation.Difference_AB:
            self.getEdges(polA, PointAndPolygonPosition.Outside, edges)
            self.getEdges(polB, PointAndPolygonPosition.Inside, edges)

        # Difference BA operation
        elif operation == BooleanOperation.Difference_BA:
            self.getEdges(polA, PointAndPolygonPosition.Inside, edges)
            self.getEdges(polB, PointAndPolygonPosition.Outside, edges)

        return edges

    # from PyQt6.QtCore import *
# from PyQt6.QtGui import *
# from PyQt6.QtWidgets import *
# from math import *
# from typing import List
# from qpointFB import *
# from pointandlineposition import *
# from pointandpolygonposition import *
# from lineandlineposition import *
# from booleanoperation import *
# from edge import *
#
#
# class Algorithms:
#     def __init__(self):
#         pass
#
#     def getPointAndLinePosition(self, a: QPointFB, p1: QPointFB, p2: QPointFB):
#         # Analyse position point and line
#         eps = 1.0e-10
#
#         # Coordinate differences
#         ux = p2.x() - p1.x()
#         uy = p2.y() - p1.y()
#         vx = a.x() - p1.x()
#         vy = a.y() - p1.y()
#
#         # Calculating determinant
#         t = ux*vy - vx*uy
#
#         # Point in left halfplane
#         if t > eps:
#             return PointAndLinePosition.Left_HP
#
#         # Point in right halfplane
#         if t < -eps:
#             return PointAndLinePosition.Right_HP
#
#         # Collinear point
#         return PointAndLinePosition.On_Line
#
#     def get2LinesAngle(self, p1: QPointFB, p2: QPointFB, p3: QPointFB, p4: QPointFB):
#         # Get angle between 2 vectors
#         ux = p2.x() - p1.x()
#         uy = p2.y() - p1.y()
#         vx = p4.x() - p3.x()
#         vy = p4.y() - p3.y()
#
#         # Dot product
#         uv = ux*vx + uy*vy
#
#         # Norms
#         nu = (ux**2 + uy**2)**0.5
#         nv = (vx**2 + vy**2)**0.5
#
#         # Point on the vertex
#         if nu == 0 or nv == 0:
#             return 0
#
#         # Round down to 1 if greater
#         if uv/(nu*nv) > 1:
#             return abs(acos(1))
#
#         # Round up to -1 if smaller
#         if uv/(nu*nv) < -1:
#             return abs(acos(-1))
#
#         # Angle
#         return abs(acos(uv/(nu*nv)))
#
#     def getPositionPointAndPolygon(self, q:QPoint, pol: List[QPointFB]) -> int:
#         # Analyse position of the point and polygon
#         # Initialise n and omega_sum
#         n = len(pol)
#         omega_sum = 0
#
#         # Loop through polygon list
#         for i in range(n-1):
#             pos = self.getPointAndLinePosition(q, pol[i], pol[(i+1)])
#             omega = self.get2LinesAngle(q, pol[i], q, pol[(i+1)])
#
#             if pos == 1:
#             # Point in the left halfplane
#                 omega_sum += omega
#
#             elif pos == 0:
#             # Point in the right halfplane
#                 omega_sum -= omega
#
#             else:
#                 # Colinear point
#                 # Investigate if point on the boundary/vertex
#                 if (q.x()-pol[i].x() )* (q.x()-pol[i+1].x()) <= 0 and (q.y()-pol[i].y()) * (q.y()-pol[i+1].y()) <= 0:
#                     return 1
#
#         # Calculate Winding Number
#         # Point q inside polygon
#         epsilon = 1.0e-10
#         if abs(abs(omega_sum)-2*pi) < epsilon:
#             return PointAndPolygonPosition.Inside
#
#         # Point q outside polygon
#         return PointAndPolygonPosition.Outside
#
#     def get2LinesIntersection(self, p1: QPointFB, p2: QPointFB, p3: QPointFB, p4:QPointFB):
#         # Line directions
#         ux = p2.x() - p1.x()
#         uy = p2.y() - p1.y()
#         vx = p4.x() - p3.x()
#         vy = p4.y() - p3.y()
#         wx = p1.x() - p3.x()
#         wy = p1.y() - p3.y()
#
#         # Coefficients k1, k2, k3
#         k1 = vx*wy - wx*vy
#         k2 = ux*wy - uy*wx
#         k3 = ux*vy - vx*uy
#
#         # Collinear lines
#         eps = 1e-10
#         if abs(k3) < eps:
#             return LineAndLinePosition.Collinear, None
#
#         alpha = k1/k3
#         beta = k2/k3
#
#         # Parallel lines
#         if abs(k1) <= eps and abs(k2) <= eps:
#             return LineAndLinePosition.Parallel, None
#
#         # Intersected lines
#         if eps < alpha < 1-eps and eps < beta < 1-eps:
#
#             # Get intersection
#             x = p1.x() + alpha*ux
#             y = p1.y() + alpha*uy
#
#             I = QPointFB(x, y, alpha, beta)
#
#             return LineAndLinePosition.Intersect, I
#
#         # No intersection
#         return LineAndLinePosition.Skew, None
#
#     def updatePolygonVertices(self, polA: List[QPointFB], polB: List[QPointFB]):
#         # Add line segments' intersections to polygon vertices
#
#         # Set epsilon value
#         eps = 1.0e-10
#
#         for i in range(len(polA)):
#             # Create dictionary
#             dictA = {}
#             for j in range(len(polB)):
#
#                 # Get intersection
#                 status, I = self.get2LinesIntersection(polA[i], polA[(i+1)%len(polA)], polB[j], polB[(j+1)%len(polB)])
#
#                 # Update dictionary if status is equal to Intersect
#                 if status == LineAndLinePosition.Intersect:
#
#                     # Get alpha and beta of intersect I
#                     alpha = I.getAlpha()
#                     beta = I.getBeta()
#
#                     # Add intersection to the dictionary A if condition fulfilled
#                     if eps < alpha < 1-eps:
#                         dictA[alpha] = I
#
#                     # Add intersection to the dictionary B if condition fulfilled
#                     if eps < beta < 1-eps:
#
#                         # Increment j
#                         j += 1
#
#                         # Add intersection to polygon B
#                         polB.insert(j, I)
#
#                 # Increment j
#                 j += 1
#
#             # Any intersection exists?
#             if len(dictA) > 0:
#
#                 # Increment i
#                 i += 1
#
#                 # Process all intersections
#                 for k, v in dictA.items():
#                     # Add intersection to polygon
#                     polA.insert(i, v)
#
#                     # Increment i
#                     i += 1
#
#             # Increment i
#             i += 1
#
#     def setEdgePosition(self, polA: List[QPointFB], polB: List[QPointFB]):
#         # Set edge positions of polygon A against polygon B
#
#         # Process edges of polygon A
#         for i in range(len(polA)):
#
#             # Get midpoint of an edge
#             x_m = (polA[i].x() + polA[(1+1)%len(polA)].x()) / 2
#             y_m = (polA[i].y() + polA[(1+1)%len(polA)].y()) / 2
#
#             m = QPointFB(x_m, y_m)
#
#             # Get position of midpoint m against polygon B
#             pos = self.getPositionPointAndPolygon(m, polB)
#
#             # Set position of i-th point
#             polA[i].setPosition(pos)
#
#     def getEdges(self, pol: List[QPointFB], position: PointAndPolygonPosition, edges: List[Edge]):
#         # Get edges by desired position
#
#         # Iterate polygon
#         for i in range(len(pol)):
#
#             # Find edge of the same position
#             if pol[i].getPosition() == position:
#
#                 # Create edge
#                 e = Edge(pol[i], pol[(i+1)%len(pol)])
#
#                 # Add edge to the list
#                 edges.append(e)
#
#     def createOverlay(self, polA: List[QPointFB], polB: List[QPointFB], operation: BooleanOperation) -> List[Edge]:
#         # Execute Boolean operation on input polygons
#         # Initialise list of output edges
#         edges: List[Edge] = []
#
#         # Update polygons' vertices
#         self.updatePolygonVertices(polA, polB)
#
#         # Set edge position
#         self.setEdgePosition(polA, polB)
#         self.setEdgePosition(polB, polA)
#
#         # Union operation
#         if operation == BooleanOperation.Union:
#             self.getEdges(polA, PointAndPolygonPosition.Outside, edges)
#             self.getEdges(polB, PointAndPolygonPosition.Outside, edges)
#
#         # Intersection operation
#         elif operation == BooleanOperation.Intersection:
#             self.getEdges(polA, PointAndPolygonPosition.Inside, edges)
#             self.getEdges(polB, PointAndPolygonPosition.Inside, edges)
#
#         # Difference operation (A-B)
#         elif operation == BooleanOperation.Intersection:
#             self.getEdges(polA, PointAndPolygonPosition.Outside, edges)
#             self.getEdges(polB, PointAndPolygonPosition.Inside, edges)
#
#         # Difference operation (B-A)
#         elif operation == BooleanOperation.Intersection:
#             self.getEdges(polA, PointAndPolygonPosition.Inside, edges)
#             self.getEdges(polB, PointAndPolygonPosition.Outside, edges)
#
#         return edges
