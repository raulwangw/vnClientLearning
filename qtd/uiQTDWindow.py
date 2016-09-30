#encoding:UTF-8
from PyQt4 import QtGui,QtCore
import json

from Ui_Dir.ui_qtdMainWindow import Ui_qtdMainWindow 
from qtd.uiData import *
from qtdCustomerWidget.VtListRadioButtonWidget import VtListRadioButtonWidget
from qtdCustomerWidget.QTDSellOrBuyWidget import QTDSellOrBuyWidget

import indexView
from PyQt4.Qt import QHBoxLayout

from uiBasicWidget import *

from qtd.qtdManager import *

class uiQTDWindow(QtGui.QMainWindow):
    def __init__(self,parent = None,mainEngine=None,eventEngine=None):
        super(uiQTDWindow,self).__init__()
        self.setParent(parent)
        self.mainEngine = mainEngine
        self.eventEngine = eventEngine

        self.uiManager = qtdManager(self.mainEngine,self.eventEngine)

        self.ui = Ui_qtdMainWindow()
        self.ui.setupUi(self)
        
        self.ui.setupUi(self)
        self.initUi()
        self.showMaximized()
        self.mainEngine.connect("QTD")        
        
    def initUi(self):
        self.initQueryStockInforView()
        self.initKLineView()
        self.initIndexView()
        self.initStockCustomerView()
        self.initStratisticSelectionView()
        self.initTradeView()
        self.initQueryStorageInforView()
        self.initLogView()
        menu = self.menuBar().addMenu("Func")
        funcAct = menu.addAction("testMD")
        funcAct.triggered.connect(self.testMD)
        
        
    def testMD(self):
        self.uiManager.testMD()
        
    
    def initQueryStockInforView(self):
        
        wdg = QTDMarketMonitor(self.mainEngine,self.eventEngine,self.ui.Wdg_QueryStock)
        wdg.setGeometry(0,0,self.ui.Wdg_QueryStock.geometry().width(),self.ui.Wdg_QueryStock.geometry().height()) 
    
    def initKLineView(self):
        self.dailyKLineWidget = dailyKPictureMonitor(self.mainEngine,self.eventEngine,self.ui.Wdg_KLine)             
        
        
    def initIndexView(self):
        tabW = QtGui.QTabWidget()
        #tabW.setTabPosition(QtGui.QTabWidget.West)
        mLayout = QtGui.QVBoxLayout(self.ui.Wdg_Index)
        mLayout.addWidget(tabW)
        try:
            fp = open(UI_DEFINE_STRING_INDEXFILE,'r')
            indexObj = json.load(fp)
            for page in indexObj["indexViews"]:
                name = page.keys()[0]
                v = page[name]
                wdg = QtGui.QWidget()
                vLayout = QtGui.QVBoxLayout(wdg)
                thLayout = QtGui.QHBoxLayout()
                bhLayout = QtGui.QHBoxLayout()
                vLayout.addLayout(thLayout)
                vLayout.addLayout(bhLayout)
                for n,index in enumerate(v):
                    if n/2 == 1:
                        layout = bhLayout
                    else:
                        layout = thLayout
                    if index not in UI_DEFINE_LIST_INDEXVIEW:
                        continue
                    index="indexView."+index+"()"
                    iv = indexView.view1(1)
                    layout.addWidget(iv)
                thLayout.setMargin(0)
                bhLayout.setMargin(0)
                vLayout.setMargin(0)
                tabW.addTab(wdg,name)
        except IOError:
            print("no index json file")
        finally:
            print("close")
            fp.close()
            
    def initStockCustomerView(self):
        tv = QtGui.QTreeView(self.ui.Wdg_StockCustomer)
        nLst = UI_DEFINE_LIST_STOCKCUSTOMER
        model = QtGui.QStandardItemModel()    
        model.setHorizontalHeaderLabels(nLst)
        tv.setModel(model)
        tv.setGeometry(0,0,self.ui.Wdg_StockCustomer.geometry().width(),self.ui.Wdg_StockCustomer.geometry().height())

    def initStratisticSelectionView(self):

        tv = QTDStockSelectStratistic(self.mainEngine,self.eventEngine)
        
        self.ui.filterStratisticCB=QtGui.QComboBox()
        filterStratisticLabel = QtGui.QLabel(u'选股策略:')
        thLayout = QtGui.QHBoxLayout()
        thLayout.addWidget(filterStratisticLabel)
        thLayout.addWidget(self.ui.filterStratisticCB)
        thLayout.setStretch(0,1)
        thLayout.setStretch(1,5)
        thLayout.setAlignment(self.ui.filterStratisticCB,QtCore.Qt.AlignLeft)
        
        vLayout = QtGui.QVBoxLayout()
        vLayout.addLayout(thLayout)
        vLayout.addWidget(tv)
        self.ui.Wdg_StratisticSelection.setLayout(vLayout)        
        tv.setGeometry(0,0,self.ui.Wdg_StratisticSelection.geometry().width(),self.ui.Wdg_StratisticSelection.geometry().height())
        
        
        ### initial selection stratistic
        for name in self.uiManager.getAllStockSelectionNames():
            self.ui.filterStratisticCB.addItem(QtCore.QString(name))
        
        self.connect(self.ui.filterStratisticCB,QtCore.SIGNAL("activated(QString)"),self.activeStockSelectedStratistic)
    
    def activeStockSelectedStratistic(self,str):
        self.uiManager.activeStockSelectionStratistic(str)
    
    def initTradeView(self):
        trade = QtGui.QTabWidget(self.ui.Wdg_Trade)

        #stock pool
        name = UI_DEFINE_DICT_1_STOCKPOOL.keys()[0]
        lst = UI_DEFINE_DICT_1_STOCKPOOL[name]
        tv = QtGui.QTreeView(trade)
        model = QtGui.QStandardItemModel()    
        model.setHorizontalHeaderLabels(lst)
        tv.setModel(model)
        trade.addTab(tv,name)
        
        #buy
        name = UI_DEFINE_DICT_1_MANULTRIGGERBUYTRADE.keys()[0]
        buyWidget = QTDSellOrBuyWidget('b')
        buyWidget.setGeometry(0,0,200,400)
        trade.addTab(buyWidget,name)
        
        #sell
        name = UI_DEFINE_DICT_1_MANULTRIGGERSELLTRADE.keys()[0]
        sellWidget = QTDSellOrBuyWidget('s')
        trade.addTab(sellWidget,name)
        
        trade.setGeometry(0,0,self.ui.Wdg_Trade.geometry().width(),self.ui.Wdg_Trade.geometry().height())
            
    
    def initQueryStorageInforView(self):
        trade = QtGui.QTabWidget(self.ui.Wdg_QueryStorageInfor)
        hwdg = QTDHoldStockMonitor(self.mainEngine,self.eventEngine)
        twdg = QTDTransactionMonitor(self.mainEngine,self.eventEngine)
        cwdg = QTDCommissionMonitor(self.mainEngine,self.eventEngine)
        trade.addTab(hwdg,UI_DEFINE_DICT_1_HOLDSTORAGE.keys()[0])
        trade.addTab(cwdg,UI_DEFINE_DICT_1_TOTALCOMMISSION.keys()[0])
        trade.addTab(twdg,UI_DEFINE_DICT_1_TRANSACTIONLIST.keys()[0])
        trade.setGeometry(0,0,self.ui.Wdg_QueryStorageInfor.geometry().width(),self.ui.Wdg_QueryStorageInfor.geometry().height())
        
    def initLogView(self):
        trade = QtGui.QTabWidget(self.ui.Wdg_Log)
        
        #Log
        name = UI_DEFINE_DICT_1_LOG.keys()[0]
        lst = UI_DEFINE_DICT_1_LOG[name]
        lwdg = QTDLogMonitor(self.mainEngine,self.eventEngine)
        rw = VtListRadioButtonWidget(UI_DEFINE_LIST_LOGSELECTEDLIST)
        wdg = QtGui.QWidget()
        vLayout = QtGui.QVBoxLayout()
        vLayout.addWidget(rw)
        vLayout.addWidget(lwdg)
        wdg.setLayout(vLayout)
        trade.addTab(wdg,name)

        # Captal
        name = UI_DEFINE_DICT_1_CAPITAL.keys()[0]
        lst = UI_DEFINE_DICT_1_CAPITAL[name]
        cWdg = QTDCapitalMonitor(self.mainEngine,self.eventEngine)
        trade.addTab(cWdg,name)
        
        trade.setGeometry(0,0,self.ui.Wdg_Log.geometry().width(),self.ui.Wdg_Log.geometry().height())
    
    def findFrameObjectName(self,name):
        for child in self.ui.centralwidget.children():
            if child.objectName()[:len(name)] == name:
                return child
        return None
    
    def __del__(self):
        self.mainEngine.exit()
        self.deleteLater()    
        
