from PyQt6 import QtCore, QtGui, QtWidgets
from algorithms import *
from draw import Draw


class Ui_MainForm(object):
    def setupUi(self, MainForm):
        MainForm.setObjectName("MainForm")
        MainForm.resize(895, 600)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainForm.sizePolicy().hasHeightForWidth())
        MainForm.setSizePolicy(sizePolicy)
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
        self.label = QtWidgets.QLabel(MainForm)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.comboBox = QtWidgets.QComboBox(MainForm)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.verticalLayout.addWidget(self.comboBox)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.label_2 = QtWidgets.QLabel(MainForm)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.comboBox_2 = QtWidgets.QComboBox(MainForm)
        self.comboBox_2.setObjectName("comboBox_2")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.verticalLayout.addWidget(self.comboBox_2)
        spacerItem2 = QtWidgets.QSpacerItem(20, 78, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout.addItem(spacerItem2)
        self.pushButton = QtWidgets.QPushButton(MainForm)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton)
        spacerItem3 = QtWidgets.QSpacerItem(20, 178, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout.addItem(spacerItem3)
        self.pushButton_2 = QtWidgets.QPushButton(MainForm)
        self.pushButton_2.setObjectName("pushButton_2")
        self.verticalLayout.addWidget(self.pushButton_2)
        self.horizontalLayout.addLayout(self.verticalLayout)

        self.retranslateUi(MainForm)
        self.pushButton.clicked.connect(self.simplifyClick) # type: ignore
        self.pushButton_2.clicked.connect(self.clearClick) # type: ignore
        self.pushButton_3.clicked.connect(self.input) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(MainForm)

    def input(self):
        # Store Canvas parameters for later rescale
        width = self.Canvas.frameGeometry().width()
        height = self.Canvas.frameGeometry().height()

        # Call setPath with specific Canvas parameters
        self.Canvas.setPath(width-100, height-100)

    def simplifyClick(self):
        # Get polygon
        pol = self.Canvas.getPolygon()

        # Create MAER
        a = Algorithms()

        # Set the length of the result list
        self.Canvas.res = [0] * len(pol)

        # Initialise the counter
        count = -1

        # Analyse for each polygon
        for polygons in pol:

            count += 1
            if self.comboBox.currentIndex() == 0:
                # Use MAER
                res = a.minAreaEnclosingRectangle(polygons, self.comboBox_2.currentIndex(), len(polygons))

            if self.comboBox.currentIndex() == 1:
                # Use Wall Average
                res = a.wallAverage(polygons)

            if self.comboBox.currentIndex() == 2:
                # Use Longest Edge
                res = a.longestEdge(polygons)

            if self.comboBox.currentIndex() == 3:
                # Use Longest Edge
                res = a.weightedBisector(polygons)

                # Store the result in list
            self.Canvas.res[count] = res

        # Repaint
        self.Canvas.repaint()

    def clearClick(self):
        self.Canvas.res = []
        self.Canvas.pol = []

        self.Canvas.repaint()

    def retranslateUi(self, MainForm):
        _translate = QtCore.QCoreApplication.translate
        MainForm.setWindowTitle(_translate("MainForm", "BuildingSimplify"))
        self.pushButton_3.setText(_translate("MainForm", "INPUT SHP"))
        self.label.setText(_translate("MainForm", "SIMPLIFY METHOD"))
        self.comboBox.setItemText(0, _translate("MainForm", "Min. Area ER"))
        self.comboBox.setItemText(1, _translate("MainForm", "Wall Average"))
        self.comboBox.setItemText(2, _translate("MainForm", "Longest Edge"))
        self.comboBox.setItemText(3, _translate("MainForm", "Weighted Bisector"))
        self.label_2.setText(_translate("MainForm", "CONVEX HULL METHOD"))
        self.comboBox_2.setItemText(0, _translate("MainForm", "Jarvis Scan"))
        self.comboBox_2.setItemText(1, _translate("MainForm", "Graham Scan"))
        self.pushButton.setText(_translate("MainForm", "SIMPLIFY"))
        self.pushButton_2.setText(_translate("MainForm", "CLEAR"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainForm = QtWidgets.QWidget()
    ui = Ui_MainForm()
    ui.setupUi(MainForm)
    MainForm.show()
    sys.exit(app.exec())
