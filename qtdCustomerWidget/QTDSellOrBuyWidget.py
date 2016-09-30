#encoding:UTF-8
from PyQt4 import QtGui,QtCore

class QTDSellOrBuyWidget(QtGui.QWidget):
    def __init__(self,sob,parent=None):
        super(QTDSellOrBuyWidget,self).__init__(parent)
        self.initUi(sob)

    def initUi(self,sob):
        if sob == 'b':
            actName = u'买入'
        elif sob == 's':
            actName = u'卖出'
        else:
            raise()
        
        nameLab = QtGui.QLabel(u'股票名称:')
        priceLab = QtGui.QLabel(u'价格:')
        numLab = QtGui.QLabel(u'数量:')
        self.le_name = QtGui.QLineEdit()
        self.sb_price = QtGui.QLineEdit()
        self.sb_num = QtGui.QLineEdit()
        self.act = QtGui.QPushButton(actName)
        
        
        mainhLayout = QtGui.QHBoxLayout()
        
        thLayout = QtGui.QHBoxLayout()
        mhLayout = QtGui.QHBoxLayout()
        bhLayout = QtGui.QHBoxLayout()
        
        thLayout.addWidget(nameLab)
        thLayout.addWidget(self.le_name)
        
        mhLayout.addWidget(priceLab)
        mhLayout.addWidget(self.sb_price)
        
        bhLayout.addWidget(numLab)
        bhLayout.addWidget(self.sb_num)
        
        
        
        vLayout = QtGui.QVBoxLayout()
        vLayout.addLayout(thLayout)
        vLayout.addLayout(mhLayout)
        vLayout.addLayout(bhLayout)
        vLayout.addWidget(self.act)
        
        fiveWdg = pQTDB5S5Widget()
        fiveWdg.registerB5S5(self)
        
        mainhLayout.addLayout(vLayout)
        mainhLayout.addWidget(fiveWdg)
        
        self.setLayout(mainhLayout)
    
    def setPrice(self,price):
        self.sb_price.setText(price)

class pQTDB5S5Widget(QtGui.QTreeWidget):
    def __init__(self,parent=None):
        super(pQTDB5S5Widget,self).__init__(parent)
        self._b5s5 = None
        self.initUi()
        self.initSlot()
    
    def initUi(self):
        lst = QtCore.QStringList()
        lst.append('')
        lst.append('')
        lst.append('')
        self.setHeaderLabels(lst)
        self.setHeaderHidden(True)
        
        item = QtGui.QTreeWidgetItem()
        item.setText(0,'a')
        item.setText(1,'b')
        item.setText(2,'c')
        self.addTopLevelItem(item)
    
    def initSlot(self):
        self.itemClicked.connect(self.slotSetB5S5)
        
    
    def slotSetB5S5(self,item,column):
        print("1")
        if self._b5s5 != None:
            self._b5s5.setPrice(item.text(1))
        
    def registerB5S5(self,b5s5):
        self._b5s5 = b5s5
        
    
        
        
        
        