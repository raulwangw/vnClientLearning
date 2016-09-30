# encoding: UTF-8

import sys
import ctypes
import platform
from vtSelectMain import SelectedMainWidget
from vtEngine import MainEngine
from PyQt4 import QtGui, QtCore
from uiMainWindow import *
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas

#----------------------------------------------------------------------
def main():
    """主程序入口"""
    # 重载sys模块，设置默认字符串编码方式为utf8
    reload(sys)
    sys.setdefaultencoding('utf8')
    
    # 设置Windows底部任务栏图标
    if 'Windows' in platform.uname() :
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('vn.trader')  

    # 初始化Qt应用对象
    app = QtGui.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon('vnpy.ico'))
    app.setFont(BASIC_FONT)
    mainEngine = MainEngine()
    
    sm = SelectedMainWidget(mainEngine,mainEngine.eventEngine)
    sm.show()
    
    #sm = MainWindow(mainEngine,mainEngine.eventEngine)
    #sm.showMaximized()
    
    # 在主线程中启动Qt事件循环
    sys.exit(app.exec_())
    
    print("------------------over")
    
    
if __name__ == '__main__':
    main()
