from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from math import *

class Algorithms:
    def __init__(self):
        pass

    def get2LinesAngle(self, p1: QPoint, p2: QPoint, p3: QPoint, p4: QPoint):
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
        try:
            return abs(acos(uv / (nu * nv)))
        except:
            return 0

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

    def jarvisScanCH(self, pol: QPolygon, max_iter: int):
        ch = QPolygon()

        # Find pivot
        q = min(pol, key=lambda k: k.y())

        # Initialise Pj, Pj1
        pj = q
        pj1 = QPoint(q.x() - 10, q.y())

        # Appending pivot to convex hull
        ch.append(q)

        # Initialize iteration limit
        tries = 0

        # Jarvis scan
        first_pass = True

        while pj != q or first_pass:
            first_pass = False

            # Find point maximizing omega
            omega_max = 0
            index_max = -1

            # Limit iterations in case of infinite loop
            tries += 1
            if tries > max_iter+10:
                break

            for index in range(len(pol)):
                # Compute omega angle
                omega = self.get2LinesAngle(pj, pj1, pj, pol[index])

                # Updating maximum
                if omega >= omega_max:
                    omega_max = omega
                    index_max = index

            # Add vertex to convex hull
            ch.append(pol[index_max])

            # Update last two points of ch
            pj1 = pj
            pj = pol[index_max]


        return ch

    def grahamScanCH(self, pol: QPolygon):
        # Initialise Convex Hull & ancillary list (CH list)
        ch = QPolygon()
        ch_l = []

        # Find pivot and parallel to x
        q = min(pol, key=lambda k: k.y())
        pp = QPoint(q.x() + 10, q.y())

        # Add pivot to the CH list
        ch_l.append(q)

        # Initialise empty dictionary
        S = {}

        # Fill up the dictionary
        for i in range(len(pol)-1):

            # Skip pivot point
            if pol[i] == q:
                continue

            # Compute the angle between x-parallel and the next point
            omega = self.get2LinesAngle(q, pp, q, pol[i])

            # Store omega as key
            if omega not in S.keys():
                S[omega] = i
                d_max = self.getLength(q, pol[i])

            # Fix for collinear points
            else:
                d = self.getLength(q, pol[i])
                # Choose only the furthest point
                if d > d_max:
                    S[omega] = i

        # Sort the dictionary by omega (ascending order)
        S = {k: v for k, v in sorted(S.items(), key=lambda item: item[0])}

        # Graham scan
        # Initialise indexing & the first point of S as p
        j = 1
        p = pol[list(S.values())[0]]

        # Add p to CH list
        ch_l.append(p)

        # Browse points of the ordered dictionary until condition is fulfilled
        while j < len(S):
            pj = pol[list(S.values())[j]]

            # Do the Left/Right half plane test
            pos = self.getPointAndLinePosition(pj, ch_l[-2], ch_l[-1])

            # pj in the left half plane
            if pos != 0:
                # Add pj to the CH list and update j
                ch_l.append(pj)
                j += 1
            else:
                # Remove last point from CH list
                ch_l.pop()

        # Add points from CH list to the Convex Hull polygon
        for el in ch_l:
            ch.append(el)

        # Add q at the last position to Convex Hull
        ch.append(q)

        return ch

    def rotate(self, pol: QPolygon, angle: float):
        # Rotate polygon vertices by angle
        pol_rot = QPolygon()

        # Browse points one by one
        for i in range(len(pol)):
            # Apply rotation matrix
            xr = pol[i].x() * cos(angle) - sin(angle) * pol[i].y()
            yr = pol[i].x() * sin(angle) + cos(angle) * pol[i].y()

            # Add point to rotated polygon
            point = QPoint(int(xr), int(yr))
            pol_rot.append(point)

        return pol_rot

    def minMaxBox(self, pol: QPolygon):
        # Creating minmax box and calculating area
        # Finding extreme coordinates
        x_min = min(pol, key=lambda k: k.x()).x()
        x_max = max(pol, key=lambda k: k.x()).x()
        y_min = min(pol, key=lambda k: k.y()).y()
        y_max = max(pol, key=lambda k: k.y()).y()

        # Create vertices of bounding box
        v1 = QPoint(x_min, y_min)
        v2 = QPoint(x_max, y_min)
        v3 = QPoint(x_max, y_max)
        v4 = QPoint(x_min, y_max)

        # Area of rectangle
        a = x_max-x_min
        b = y_max-y_min
        S = a*b

        # Create QPolygon
        minmax_box = QPolygon([v1, v2, v3, v4])

        return S, minmax_box

    def minAreaEnclosingRectangle(self, pol: QPolygon, ch: int, length: int):
        # Create approximation of building using minimum area enclosing rectangle
        # Create convex hull
        if ch == 0:
            ch = self.jarvisScanCH(pol, length)
        if ch == 1:
            ch = self.grahamScanCH(pol)

        n_ch = len(ch)

        # Create initial approximation
        sigma_min = 0
        S_min, mmb_min = self.minMaxBox(ch)

        # Process all segments of convex hull
        for i in range(n_ch):
            dx = ch[(i+1)%n_ch].x()-ch[i].x()
            dy = ch[(i+1)%n_ch].y()-ch[i].y()

            # Direction of segment
            sigma_i = atan2(dy,dx)

            # Rotate by -sigma_i
            ch_rot = self.rotate(ch, -sigma_i)

            # Create MMB
            S_i, mmb_i = self.minMaxBox(ch_rot)

            # Updating minimum
            if S_i < S_min:
                S_min = S_i
                sigma_min = sigma_i
                mmb_min = mmb_i

        # Rotate mmb_min back by sigma_min
        er = self.rotate(mmb_min, sigma_min)

        # Resize mmb_res, S_mmb = S_building
        er_new = self.resizeRectangle(er, pol)

        return er_new

    def getArea(self, pol: QPolygon):
        # Calculating area of non-convex polygon using LH formula
        n = len(pol)
        S = 0

        for i in range(n):
            dS = pol[i].x()*(pol[(i+1) % n].y()-pol[(i-1+n) % n].y())
            S += dS

        return 0.5 * abs(S) # absolute value since it comes to node orientation CCW/CW

    def resizeRectangle(self, er: QPolygon, pol: QPolygon):
        # Resize MAER equally to building area (pol)
        # Calculate polygon area
        er_S = self.getArea(er)
        pol_S = self.getArea(pol)

        # Calculate ratio between er_S and pol_S
        k = pol_S/er_S

        # Define Mass centre point
        xc = (er[0].x() + er[1].x() + er[2].x() + er[3].x())/len(er)
        yc = (er[0].y() + er[1].y() + er[2].y() + er[3].y())/len(er)

        # Calculate directions
        u1x = er[0].x() - xc
        u1y = er[0].y() - yc
        u2x = er[1].x() - xc
        u2y = er[1].y() - yc
        u3x = er[2].x() - xc
        u3y = er[2].y() - yc
        u4x = er[3].x() - xc
        u4y = er[3].y() - yc

        # Calculate new nodes
        v1x = int(xc + sqrt(k) * u1x)
        v1y = int(yc + sqrt(k) * u1y)
        v2x = int(xc + sqrt(k) * u2x)
        v2y = int(yc + sqrt(k) * u2y)
        v3x = int(xc + sqrt(k) * u3x)
        v3y = int(yc + sqrt(k) * u3y)
        v4x = int(xc + sqrt(k) * u4x)
        v4y = int(yc + sqrt(k) * u4y)

        # Convert to QPoints
        v1 = QPoint(v1x, v1y)
        v2 = QPoint(v2x, v2y)
        v3 = QPoint(v3x, v3y)
        v4 = QPoint(v4x, v4y)

        # Create QPolygon
        er_rsz = QPolygon([v1, v2, v3, v4])

        return er_rsz

    def wallAverage(self, pol: QPolygon):
        # Determine building's orientation
        # Initialise r_sum, l_sum and sigma0
        r_sum = 0
        l_sum = 0
        sigma0 = 0

        # Find pivot and the initial sigma0
        dx = pol[(1) % len(pol)].x() - pol[0].x()
        dy = pol[(1) % len(pol)].y() - pol[0].y()
        sigma0 = atan2(dy, dx)

        # Browse all points to compute r_sum and l_sum
        for i in range(len(pol)):

            # Compute sigma for every edge
            dx = pol[(i+1) % len(pol)].x() - pol[i].x()
            dy = pol[(i+1) % len(pol)].y() - pol[i].y()
            sigma = atan2(dy, dx)

            # Compute ∆sigma, k & variance rest
            dsigma = sigma - sigma0
            k = round(2 * dsigma / pi)
            r = dsigma - k * pi / 2

            # Skip if the points identical
            if self.getLength(pol[i], pol[(i + 1) % len(pol)]) == 0:
                continue

            # Update r_sum and l_sum
            r_sum += r * self.getLength(pol[i], pol[(i + 1) % len(pol)])
            l_sum += self.getLength(pol[i], pol[(i + 1) % len(pol)])

        # Compute sigma_final from sigma 0 & weighted average
        sigma_f = sigma0 + r_sum/l_sum

        # Rotate building by -sigma_final
        pol_rot = self.rotate(pol, -sigma_f)

        # Compute MinMaxBox
        S_min, mmb = self.minMaxBox(pol_rot)

        # Rotate MinMaxBox back by sigma_final
        mmb_rot = self.rotate(mmb, sigma_f)

        # Resize MinMaxBox
        mmb_res = self.resizeRectangle(mmb_rot, pol)

        return mmb_res

    def longestEdge(self, pol: QPolygon):
        # Determine building's orientation
        # Initialise the longest edge l_max
        l_max = 0

        # Browse all the points to find the longest edge
        for i in range(len(pol)):

            # Compute the edge length
            l = self.getLength(pol[i], pol[(i+1)%len(pol)])

            # Update l_max if condition fulfilled
            if l > l_max:
                l_max = l

                # Compute the direction and store it
                dx = pol[(i + 1) % len(pol)].x() - pol[i].x()
                dy = pol[(i + 1) % len(pol)].y() - pol[i].y()
                sigma = atan2(dy, dx)

        # Rotate building by -sigma
        pol_rot = self.rotate(pol, -sigma)

        # Compute MinMaxBox
        S_min, mmb = self.minMaxBox(pol_rot)

        # Rotate MinMaxBox back by sigma
        mmb_rot = self.rotate(mmb, sigma)

        # Resize MinMaxBox
        mmb_res = self.resizeRectangle(mmb_rot, pol)

        return mmb_res

    def getLength(self, p1: QPoint, p2: QPoint):
        # Return the length of a line
        dx = p2.x() - p1.x()
        dy = p2.y() - p1.y()

        return sqrt(dx*dx + dy*dy)

    def weightedBisector(self, pol: QPolygon):
        # Determine building's orientation
        # Initialise empty lists for diagonals and edges
        U = []
        S = []

        # Add all possible diagonals to U and all edges to S
        for i in range(len(pol)-1):
            for j in range(len(pol)-1):
                if i == j:
                    continue
                U.append([pol[i], pol[j]])
            S.append([pol[i], pol[(i+1)]])

        # Investigate for an intersection between every diagonal and every edge
        for i in range(len(U)):
            p1 = U[i][0]
            p2 = U[i][1]
            for j in range(len(S)):
                a1 = S[j][0]
                a2 = S[j][1]

                # Half plane test between diagonal and both edges' point
                t1 = self.getPointAndLinePosition(a1, p1, p2)
                t2 = self.getPointAndLinePosition(a2, p1, p2)

                # Line intersection
                if (t1 == 0 and t2 == 1) or (t1 == 1 and t2 == 0):
                    U[i] = None
                    break
                # Collinear line
                elif t1 == -1 and t2 == -1:
                    U[i] = None
                    break
                # No intersection
                else:
                    continue

        # Create list with Diagonals
        D = []
        for el in U:
            if el != None:
                D.append(el)

        try:
            # Delete duplicates
            for i in range(len(D)):
                for j in range(len(D)):
                    if (D[i][0] == D[j][1]) and (D[i][1] == D[j][0]):
                        D[j][0] = QPoint(1, 1)
                        D[j][1] = QPoint(1, 1)

            # Find two longest diagonals
            for k in range(2):
                l_max = -1
                idx = -1
                for i in range(len(D)):

                    l = self.getLength(D[i][0], D[i][1])

                    if l > l_max:
                        l_max = l
                        idx = i

                if k == 0:
                    d1 = D.pop(idx)

                if k == 1:
                    d2 = D.pop(idx)

            # Calculate orientation and length of the longest diagonals
            d1x = d1[1].x() - d1[0].x()
            d1y = d1[1].y() - d1[0].y()
            d2x = d2[1].x() - d2[0].x()
            d2y = d2[1].y() - d2[0].y()

            sigma1 = atan2(d1y, d1x)
            sigma2 = atan2(d2y, d2x)
            l1 = self.getLength(d1[0], d1[1])
            l2 = self.getLength(d2[0], d2[1])

            # Calculate weighted average of diagonals' orientations
            sigma_f = (l1*sigma1 + l2*sigma2) / (l1+l2)

            # Rotate building by -sigma_f
            pol_rot = self.rotate(pol, -sigma_f)

            # Compute MinMaxBox
            S_min, mmb = self.minMaxBox(pol_rot)

            # Rotate MinMaxBox back by sigma_f
            mmb_rot = self.rotate(mmb, sigma_f)

            # Resize MinMaxBox
            mmb_res = self.resizeRectangle(mmb_rot, pol)

        except:
            return QPolygon()

        return mmb_res















