from PyQt6.QtCore import *

# Creating new class QPoint3D derived from class QPointF
class QPoint3D(QPointF):
    def __init__(self, x:float, y:float, z:float = 0):
        super().__init__(x, y)
        self.z=z

    def getZ(self):
        return self.z


