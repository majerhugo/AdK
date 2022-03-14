from draw import Draw
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
#from PyQt6.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog
#from PyQt6.QtGui import QIcon
import algorithms
from algorithms import Algorithms


class Ui_MainForm(object):
    def setupUi(self, MainForm):
        MainForm.setObjectName("MainForm")
        MainForm.resize(942, 600)
        self.horizontalLayout = QtWidgets.QHBoxLayout(MainForm)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.Canvas = Draw(MainForm)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Canvas.sizePolicy().hasHeightForWidth())
        self.Canvas.setSizePolicy(sizePolicy)
        self.Canvas.setObjectName("Canvas")
        self.horizontalLayout.addWidget(self.Canvas)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.pushButton_3 = QtWidgets.QPushButton(MainForm)
        self.pushButton_3.setObjectName("pushButton_3")
        self.verticalLayout.addWidget(self.pushButton_3)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.pushButton_4 = QtWidgets.QPushButton(MainForm)
        self.pushButton_4.setObjectName("pushButton_4")
        self.verticalLayout.addWidget(self.pushButton_4)
        spacerItem1 = QtWidgets.QSpacerItem(20, 118, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.pushButton_2 = QtWidgets.QPushButton(MainForm)
        self.pushButton_2.setObjectName("pushButton_2")
        self.verticalLayout.addWidget(self.pushButton_2)
        self.label = QtWidgets.QLabel(MainForm)
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        spacerItem2 = QtWidgets.QSpacerItem(20, 48, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout.addItem(spacerItem2)
        self.pushButton = QtWidgets.QPushButton(MainForm)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton)
        self.horizontalLayout.addLayout(self.verticalLayout)

        self.retranslateUi(MainForm)
        self.pushButton_3.clicked.connect(self.input) # type: ignore
        self.pushButton_4.clicked.connect(self.draw_point) # type: ignore
        self.pushButton_2.clicked.connect(self.change_algorithm) # type: ignore
        self.pushButton.clicked.connect(self.analyze) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(MainForm)

    def retranslateUi(self, MainForm):
        _translate = QtCore.QCoreApplication.translate
        MainForm.setWindowTitle(_translate("MainForm", "Widget"))
        self.pushButton_3.setText(_translate("MainForm", "INPUT SHP"))
        self.pushButton_4.setText(_translate("MainForm", "DRAW POINT"))
        self.pushButton_2.setText(_translate("MainForm", "WINDING NUMBER / RAY"))
        self.label.setText(_translate("MainForm", "Winding Number"))
        self.pushButton.setText(_translate("MainForm", "ANALYZE"))

    def input(self):
        # Store Canvas parameters for later rescale
        width = self.Canvas.frameGeometry().width()
        height = self.Canvas.frameGeometry().height()

        # Call setPath with specific Canvas parameters
        self.Canvas.setPath(width, height)

    def draw_point(self):
        self.Canvas.setSource()

    def change_algorithm(self):
        self.Canvas.switchMethod()
        if self.Canvas.method:
            self.label.setText("Winding Number")
        else:
            self.label.setText("Ray Crossing")

    def analyze(self):
        # Get point and polygon
        q = self.Canvas.getQ()
        pol = self.Canvas.getPolygon()

        # Analyse position
        a = Algorithms()

        # Initialise the length of result list & auxiliary counter
        self.Canvas.results = [0]*len(pol)
        count = -1

        # Analyse for each polygon
        for polygons in pol:

            count += 1

            if self.Canvas.method:
                # Use Winding Number Algorithm
                res = a.windingNumber(q, polygons)

                # Store the result in list
                self.Canvas.results[count] = res

            else:
                # Use Ray Crossing
                res = a.reducedRayCrossing(q, polygons)

                # Store the result in list
                self.Canvas.results[count] = res

        self.Canvas.repaint()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainForm = QtWidgets.QWidget()
    ui = Ui_MainForm()
    ui.setupUi(MainForm)
    MainForm.show()
    sys.exit(app.exec())
