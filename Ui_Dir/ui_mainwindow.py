# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created: Tue Aug 30 20:38:22 2016
#      by: PyQt4 UI code generator 4.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(400, 300)
        self.centralWidget = QtGui.QWidget(MainWindow)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        self.btn_OpenBin = QtGui.QPushButton(self.centralWidget)
        self.btn_OpenBin.setGeometry(QtCore.QRect(332, 10, 51, 28))
        self.btn_OpenBin.setObjectName(_fromUtf8("btn_OpenBin"))
        self.le_bin = QtGui.QLineEdit(self.centralWidget)
        self.le_bin.setGeometry(QtCore.QRect(90, 10, 231, 21))
        self.le_bin.setObjectName(_fromUtf8("le_bin"))
        self.label = QtGui.QLabel(self.centralWidget)
        self.label.setGeometry(QtCore.QRect(10, 10, 72, 15))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(self.centralWidget)
        self.label_2.setGeometry(QtCore.QRect(10, 60, 72, 15))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.le_txt = QtGui.QLineEdit(self.centralWidget)
        self.le_txt.setGeometry(QtCore.QRect(90, 60, 231, 21))
        self.le_txt.setObjectName(_fromUtf8("le_txt"))
        self.btn_openTxt = QtGui.QPushButton(self.centralWidget)
        self.btn_openTxt.setGeometry(QtCore.QRect(330, 60, 51, 28))
        self.btn_openTxt.setObjectName(_fromUtf8("btn_openTxt"))
        self.btn_Bin2Text = QtGui.QPushButton(self.centralWidget)
        self.btn_Bin2Text.setGeometry(QtCore.QRect(290, 150, 93, 28))
        self.btn_Bin2Text.setObjectName(_fromUtf8("btn_Bin2Text"))
        self.btn_Text2Bin = QtGui.QPushButton(self.centralWidget)
        self.btn_Text2Bin.setGeometry(QtCore.QRect(290, 190, 93, 28))
        self.btn_Text2Bin.setObjectName(_fromUtf8("btn_Text2Bin"))
        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtGui.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 400, 26))
        self.menuBar.setObjectName(_fromUtf8("menuBar"))
        MainWindow.setMenuBar(self.menuBar)
        self.mainToolBar = QtGui.QToolBar(MainWindow)
        self.mainToolBar.setObjectName(_fromUtf8("mainToolBar"))
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)
        self.statusBar = QtGui.QStatusBar(MainWindow)
        self.statusBar.setObjectName(_fromUtf8("statusBar"))
        MainWindow.setStatusBar(self.statusBar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.btn_OpenBin.setText(_translate("MainWindow", "Open", None))
        self.label.setText(_translate("MainWindow", "bin", None))
        self.label_2.setText(_translate("MainWindow", "txt", None))
        self.btn_openTxt.setText(_translate("MainWindow", "Open", None))
        self.btn_Bin2Text.setText(_translate("MainWindow", "bin->str", None))
        self.btn_Text2Bin.setText(_translate("MainWindow", "str->bin", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

