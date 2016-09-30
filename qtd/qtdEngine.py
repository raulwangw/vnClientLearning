from matplotlib.backends.backend_qt4agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure
import numpy as np

######## QTD PictureEngine######################

from abc import abstractmethod

class PictureEngine(object):    
    def __init__(self,eventEngine):
        self.eventEngine = eventEngine
        
    def setWidgetData(self,widgetData):
        self.font = widgetData.font
        self.widget = widgetData.widget
        self.data = widgetData.data
        
    @abstractmethod
    def initFrame(self):
        pass
    
    @abstractmethod
    def updateData(self,widgetData):
        pass
    
class PictureDaily_KLineEngine(PictureEngine):
    def __init__(self,widgetData):
        self.setWidgetData(widgetData)
    
    def initFrame(self):
        self.fig = Figure((7.68,5.0),dpi=100)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self.widget)
        self.axes = self.fig.add_subplot(212)
        self.axes.imshow(np.arange(20).reshape([4, 5]).copy(), interpolation='nearest')

        print("kline initFrame")
        pass
    
    def updateData(self,widgetData):
        print("kline updateData")
        pass    
    
