from PyQt4 import QtGui,QtCore

class VtListRadioButtonWidget(QtGui.QWidget):
    def __init__(self,lst,parent=None):
        super(VtListRadioButtonWidget,self).__init__(parent)
        self.initUi(lst)
        
    def initUi(self,lst):
        hLayout = QtGui.QHBoxLayout()
        for name in lst:
            hLayout.addWidget(QtGui.QRadioButton(name,self))
        self.setLayout(hLayout)