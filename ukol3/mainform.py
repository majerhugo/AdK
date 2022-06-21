from PyQt6 import QtCore, QtGui, QtWidgets
from draw import Draw
from algorithms import *
from settings import *

class Ui_MainForm(object):
    def setupUi(self, MainForm):
        MainForm.setObjectName("MainForm")
        MainForm.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainForm)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.Canvas = Draw(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Canvas.sizePolicy().hasHeightForWidth())
        self.Canvas.setSizePolicy(sizePolicy)
        self.Canvas.setObjectName("Canvas")
        self.horizontalLayout.addWidget(self.Canvas)
        MainForm.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainForm)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 18))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuAnalyze = QtWidgets.QMenu(self.menubar)
        self.menuAnalyze.setObjectName("menuAnalyze")
        self.menuSettings = QtWidgets.QMenu(self.menubar)
        self.menuSettings.setObjectName("menuSettings")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainForm.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainForm)
        self.statusbar.setObjectName("statusbar")
        MainForm.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(MainForm)
        self.toolBar.setObjectName("toolBar")
        MainForm.addToolBar(QtCore.Qt.ToolBarArea.TopToolBarArea, self.toolBar)
        self.actionOpen = QtGui.QAction(MainForm)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icons/open_file2.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionOpen.setIcon(icon)
        self.actionOpen.setObjectName("actionOpen")
        self.actionExit = QtGui.QAction(MainForm)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("icons/refresh2.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionExit.setIcon(icon1)
        self.actionExit.setObjectName("actionExit")
        self.actionCreate_DT = QtGui.QAction(MainForm)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("icons/triangles5.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionCreate_DT.setIcon(icon2)
        self.actionCreate_DT.setObjectName("actionCreate_DT")
        self.actionCreate_Contour_Lines = QtGui.QAction(MainForm)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("icons/contours7.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionCreate_Contour_Lines.setIcon(icon3)
        self.actionCreate_Contour_Lines.setObjectName("actionCreate_Contour_Lines")
        self.actionAnalyze_Slope = QtGui.QAction(MainForm)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("icons/slope3.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionAnalyze_Slope.setIcon(icon4)
        self.actionAnalyze_Slope.setObjectName("actionAnalyze_Slope")
        self.actionAnalyze_Exposition = QtGui.QAction(MainForm)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("icons/orientation2.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionAnalyze_Exposition.setIcon(icon5)
        self.actionAnalyze_Exposition.setObjectName("actionAnalyze_Exposition")
        self.actionAbout = QtGui.QAction(MainForm)
        self.actionAbout.setObjectName("actionAbout")
        self.actionOptions = QtGui.QAction(MainForm)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("icons/settings2.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionOptions.setIcon(icon6)
        self.actionOptions.setObjectName("actionOptions")
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menuAnalyze.addAction(self.actionCreate_DT)
        self.menuAnalyze.addAction(self.actionCreate_Contour_Lines)
        self.menuAnalyze.addAction(self.actionAnalyze_Slope)
        self.menuAnalyze.addAction(self.actionAnalyze_Exposition)
        self.menuSettings.addAction(self.actionOptions)
        self.menuHelp.addAction(self.actionAbout)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuAnalyze.menuAction())
        self.menubar.addAction(self.menuSettings.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.toolBar.addAction(self.actionOpen)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionCreate_DT)
        self.toolBar.addAction(self.actionCreate_Contour_Lines)
        self.toolBar.addAction(self.actionAnalyze_Slope)
        self.toolBar.addAction(self.actionAnalyze_Exposition)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionOptions)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionExit)

        # Create dialog window
        self.dialog = QtWidgets.QDialog()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self.dialog)

        self.retranslateUi(MainForm)
        QtCore.QMetaObject.connectSlotsByName(MainForm)

        # Connect icon and function: open file
        self.actionOpen.triggered.connect(self.openFile)

        # Connect icon and function: DT
        self.actionCreate_DT.triggered.connect(self.runDT)

        # Connect icon and function: Setting dialog
        self.actionOptions.triggered.connect(self.showSettings)

        # Connect icon and function: create contour lines
        self.actionCreate_Contour_Lines.triggered.connect(self.runContourLines)

        # Connect icon and function: calculate slope
        self.actionAnalyze_Slope.triggered.connect(self.runCalculateSlope)

        # Connect icon and function: calculate exposure
        self.actionAnalyze_Exposition.triggered.connect(self.runCalculateExposition)

        # Connect icon and function: refresh button
        self.actionExit.triggered.connect(self.refreshCanvas)


    def retranslateUi(self, MainForm):
        _translate = QtCore.QCoreApplication.translate
        MainForm.setWindowTitle(_translate("MainForm", "DTM analysis"))
        self.menuFile.setTitle(_translate("MainForm", "File"))
        self.menuAnalyze.setTitle(_translate("MainForm", "Analyze"))
        self.menuSettings.setTitle(_translate("MainForm", "Settings"))
        self.menuHelp.setTitle(_translate("MainForm", "Help"))
        self.toolBar.setWindowTitle(_translate("MainForm", "toolBar"))
        self.actionOpen.setText(_translate("MainForm", "Open .TXT"))
        self.actionOpen.setToolTip(_translate("MainForm", "Open .TXT"))
        self.actionOpen.setShortcut(_translate("MainForm", "Ctrl+O"))
        self.actionExit.setText(_translate("MainForm", "Refresh"))
        self.actionCreate_DT.setText(_translate("MainForm", "Create DT"))
        self.actionCreate_Contour_Lines.setText(_translate("MainForm", "Create Contour Lines"))
        self.actionAnalyze_Slope.setText(_translate("MainForm", "Analyze Slope"))
        self.actionAnalyze_Exposition.setText(_translate("MainForm", "Analyze Exposition"))
        self.actionAnalyze_Exposition.setToolTip(_translate("MainForm", "Analyze Exposition"))
        self.actionAbout.setText(_translate("MainForm", "About DTM analysis"))
        self.actionOptions.setText(_translate("MainForm", "Options..."))
        self.actionOptions.setToolTip(_translate("MainForm", "Options"))

    def openFile(self):
        # Store Canvas parameters for later rescale
        width = self.Canvas.frameGeometry().width()
        height = self.Canvas.frameGeometry().height()

        self.Canvas.setPath(width, height)

    def refreshCanvas(self):
        # Refresh/Clear screen
        self.Canvas.points = []
        self.Canvas.dt = []
        self.Canvas.cont_lines = []
        self.Canvas.slopes = []
        self.Canvas.exposition = []

        self.Canvas.repaint()

    def runDT(self):
        #Get points
        points = self.Canvas.getPoints()

        if bool(points) != 0:
            #Create DT
            a = Algorithms()
            dt = a.DT(points)

            #Set DT
            self.Canvas.setDT(dt)
            self.Canvas.repaint()

    def runContourLines(self):
        #Get contour line settings
        z_min = float(self.ui.lineEdit.text())
        z_max = float(self.ui.lineEdit_2.text())
        dz = float(self.ui.lineEdit_3.text())

        # Set step dz for correct visualisation
        self.Canvas.setIntervalCL(dz)

        # Get triangulation
        dt = self.Canvas.getDT()
        if len(dt) == 0:
            self.runDT()
            dt = self.Canvas.getDT()

        # Create contour lines
        a = Algorithms()
        contour_lines = a.createCL(dt, z_min, z_max, dz)
        self.Canvas.setCL(contour_lines)

        self.Canvas.repaint()

    def runCalculateSlope(self):
        # Get triangulation
        dt = self.Canvas.getDT()
        if len(dt) == 0:
            self.runDT()
            dt = self.Canvas.getDT()

        # Get transformation parameters
        parameters = self.Canvas.getTranformationParameters()
        width = self.Canvas.frameGeometry().width()
        height = self.Canvas.frameGeometry().height()

        # Compute slope
        a = Algorithms()
        slopes = a.calculateSlope(dt, parameters, width, height)
        self.Canvas.setSlope(slopes)

        self.Canvas.repaint()


    def runCalculateExposition(self):
        # Get triangulation
        dt = self.Canvas.getDT()
        if len(dt) == 0:
            self.runDT()
            dt = self.Canvas.getDT()

        # Get transformation parameters
        parameters = self.Canvas.getTranformationParameters()
        width = self.Canvas.frameGeometry().width()
        height = self.Canvas.frameGeometry().height()

        # Compute aspect
        a = Algorithms()
        exposition = a.calculateExposition(dt, parameters, width, height)
        self.Canvas.setExposition(exposition)

        self.Canvas.repaint()


    def showSettings(self):
        #Show dialog window: settings
        self.dialog.exec()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainForm = QtWidgets.QMainWindow()
    ui = Ui_MainForm()
    ui.setupUi(MainForm)
    MainForm.show()
    sys.exit(app.exec())
