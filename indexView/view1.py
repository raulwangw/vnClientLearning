
from matplotlib.backends.backend_qt4agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure
import matplotlib.pyplot as plt 
import numpy as np
from PyQt4 import QtGui

class view1(QtGui.QWidget):
    def __init__(self,sql,parent=None):
        super(view1,self).__init__(parent)
        self.__initUi()
        
    
    def __initUi(self):
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        x = [1,2,3]
        y = [4,5,6]
        plt.plot(x,y)
        plt.title('Example')
        plt.xlabel('x')
        plt.ylabel('y')
        self.canvas.draw()
        layout = QtGui.QHBoxLayout(self)
        layout.addWidget(self.canvas)
