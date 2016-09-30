#encoding: UTF-8
import os
import sys
sys.path.append("C:/Users/new/Anaconda3/Lib/site-packages/PyQt4")

from PyQt4 import QtGui, QtCore
from uiMainWindow import *
from Ui_Dir.Ui_SelectedWidget import Ui_SelectedWidget
from Ui_Dir.ui_mainwindow import *
from qtd.uiQTDWindow import uiQTDWindow


class selectWdg(QtGui.QWidget):
    def __init__(self,parent=None):
        super(selectWdg, self).__init__()
        self.setParent(parent)
        self.parent = parent
         
class SelectedMainWidget(QtGui.QMainWindow):
    def __init__(self,mainEngine, eventEngine):
        super(SelectedMainWidget, self).__init__()

        self.mainEngine = mainEngine
        self.eventEngine = eventEngine
        
        self.setFixedSize(QtCore.QSize(300,200))
        self.ui = Ui_SelectedWidget()
        self.ui.setupUi(self)
        
        #if 'QTD' in self.mainEngine.gatewayDict:
      #      self.ui.btn_Qtd.setEnabled(True)
   #     else:
            #self.ui.btn_Qtd.setEnabled(False)
        
        
    @QtCore.pyqtSlot()
    def on_btn_Qtd_clicked(self):
        print(self.parent)
        if self.parent != None:
            self.selectQTD()
            
            
    @QtCore.pyqtSlot()
    def on_btn_Origin_clicked(self):
        if self.parent != None:
            self.selectOriginWidget()
    
    def __delete__(self):
        print("delete")
        
    
    def mousePressEvent(self, evt):
        return QtGui.QMainWindow.mousePressEvent(self, evt)
    
    def closeEvent(self, evt):
        print("closeEvent")
        self.mainEngine.exit()
        self.deleteLater()
        import sys
        QtGui.QApplication
        return QtGui.QMainWindow.closeEvent(self, evt)
    
    def test(self):
        print("tttest")
        return 1
        
    def selectQTD(self):        
        self.qtdWdgx = uiQTDWindow(None,self.mainEngine,self.eventEngine)
        self.qtdWdgx.show()
        self.deleteLater()
    
    def selectOriginWidget(self):
        try:
            f = file("VT_setting.json")
            setting = json.load(f)    
            if setting['darkStyle']:
                import qdarkstyle
                app.setStyleSheet(qdarkstyle.load_stylesheet(pyside=False))
        except:
            pass
        
        self.mainWindow = MainWindow(self.mainEngine, self.eventEngine)
        
        self.mainWindow.showMaximized()
        self.deleteLater()


