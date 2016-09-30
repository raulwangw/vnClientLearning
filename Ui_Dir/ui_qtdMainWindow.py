# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qtdMainWindow.ui'
#
# Created: Mon Sep 12 18:56:32 2016
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

class Ui_qtdMainWindow(object):
    def setupUi(self, qtdMainWindow):
        qtdMainWindow.setObjectName(_fromUtf8("qtdMainWindow"))
        qtdMainWindow.resize(1920, 1080)
        self.centralwidget = QtGui.QWidget(qtdMainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.Wdg_Log = QtGui.QWidget(self.centralwidget)
        self.Wdg_Log.setGeometry(QtCore.QRect(1340, 800, 576, 221))
        self.Wdg_Log.setObjectName(_fromUtf8("Wdg_Log"))
        self.Wdg_QueryStock = QtGui.QWidget(self.centralwidget)
        self.Wdg_QueryStock.setGeometry(QtCore.QRect(0, 0, 768, 360))
        self.Wdg_QueryStock.setObjectName(_fromUtf8("Wdg_QueryStock"))
        self.Wdg_Index = QtGui.QWidget(self.centralwidget)
        self.Wdg_Index.setGeometry(QtCore.QRect(0, 860, 768, 171))
        self.Wdg_Index.setObjectName(_fromUtf8("Wdg_Index"))
        self.Wdg_KLine = QtGui.QWidget(self.centralwidget)
        self.Wdg_KLine.setGeometry(QtCore.QRect(0, 360, 768, 500))
        self.Wdg_KLine.setObjectName(_fromUtf8("Wdg_KLine"))
        self.Wdg_StratisticSelection = QtGui.QWidget(self.centralwidget)
        self.Wdg_StratisticSelection.setGeometry(QtCore.QRect(768, 590, 572, 441))
        self.Wdg_StratisticSelection.setObjectName(_fromUtf8("Wdg_StratisticSelection"))
        self.Wdg_StockCustomer = QtGui.QWidget(self.centralwidget)
        self.Wdg_StockCustomer.setGeometry(QtCore.QRect(768, 0, 572, 591))
        self.Wdg_StockCustomer.setObjectName(_fromUtf8("Wdg_StockCustomer"))
        self.Wdg_QueryStorageInfor = QtGui.QWidget(self.centralwidget)
        self.Wdg_QueryStorageInfor.setGeometry(QtCore.QRect(1340, 470, 576, 330))
        self.Wdg_QueryStorageInfor.setObjectName(_fromUtf8("Wdg_QueryStorageInfor"))
        self.Wdg_Trade = QtGui.QWidget(self.centralwidget)
        self.Wdg_Trade.setGeometry(QtCore.QRect(1340, 0, 576, 470))
        self.Wdg_Trade.setObjectName(_fromUtf8("Wdg_Trade"))
        qtdMainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(qtdMainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1920, 23))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        qtdMainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(qtdMainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        qtdMainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(qtdMainWindow)
        QtCore.QMetaObject.connectSlotsByName(qtdMainWindow)

    def retranslateUi(self, qtdMainWindow):
        qtdMainWindow.setWindowTitle(_translate("qtdMainWindow", "MainWindow", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    qtdMainWindow = QtGui.QMainWindow()
    ui = Ui_qtdMainWindow()
    ui.setupUi(qtdMainWindow)
    qtdMainWindow.show()
    sys.exit(app.exec_())

