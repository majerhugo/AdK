from draw import Draw
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
#from PyQt6.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog
#from PyQt6.QtGui import QIcon
import algorithms
from algorithms import Algorithms
from draw import Draw

class Ui_MainForm(object):
    def setupUi(self, MainForm):
        MainForm.setObjectName("MainForm")
        MainForm.resize(942, 600)
        self.Canvas = Draw(MainForm)
        self.Canvas.setGeometry(QtCore.QRect(9, 9, 774, 582))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Canvas.sizePolicy().hasHeightForWidth())
        self.Canvas.setSizePolicy(sizePolicy)
        self.Canvas.setObjectName("Canvas")
        self.widget = QtWidgets.QWidget(MainForm)
        self.widget.setGeometry(QtCore.QRect(800, 10, 131, 581))
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.pushButton_3 = QtWidgets.QPushButton(self.widget)
        self.pushButton_3.setObjectName("pushButton_3")
        self.verticalLayout.addWidget(self.pushButton_3)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.pushButton_4 = QtWidgets.QPushButton(self.widget)
        self.pushButton_4.setObjectName("pushButton_4")
        self.verticalLayout.addWidget(self.pushButton_4)
        spacerItem1 = QtWidgets.QSpacerItem(20, 118, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.comboBox = QtWidgets.QComboBox(self.widget)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.verticalLayout.addWidget(self.comboBox)
        spacerItem2 = QtWidgets.QSpacerItem(20, 248, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout.addItem(spacerItem2)
        self.pushButton = QtWidgets.QPushButton(self.widget)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton)

        self.retranslateUi(MainForm)
        self.pushButton_3.clicked.connect(self.input) # type: ignore
        self.pushButton_4.clicked.connect(self.draw_point) # type: ignore
        self.pushButton.clicked.connect(self.analyze) # type: ignore
        #self.comboBox.currentIndexChanged.connect(self.changeAlgorithm)

        QtCore.QMetaObject.connectSlotsByName(MainForm)

    def retranslateUi(self, MainForm):
        _translate = QtCore.QCoreApplication.translate
        MainForm.setWindowTitle(_translate("MainForm", "Widget"))
        self.pushButton_3.setText(_translate("MainForm", "INPUT SHP"))
        self.pushButton_4.setText(_translate("MainForm", "DRAW POINT"))
        self.comboBox.setCurrentText(_translate("MainForm", "WINDING NUMBER"))
        self.comboBox.setItemText(0, _translate("MainForm", "WINDING NUMBER"))
        self.comboBox.setItemText(1, _translate("MainForm", "RAY CROSSING"))
        self.pushButton.setText(_translate("MainForm", "ANALYZE"))

    def input(self):
        # Store Canvas parameters for later rescale
        width = self.Canvas.frameGeometry().width()
        height = self.Canvas.frameGeometry().height()

        # Call setPath with specific Canvas parameters
        self.Canvas.setPath(width, height)

    def draw_point(self):
        self.Canvas.setSource()

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

            if self.comboBox.currentIndex() == 0:
                # Use Winding Number Algorithm
                res = a.windingNumber(q, polygons)

                # Store the result in list
                self.Canvas.results[count] = res

            if self.comboBox.currentIndex() == 1:
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
