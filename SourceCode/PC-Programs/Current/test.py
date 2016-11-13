import wx
from wx.lib.buttons import GenBitmapTextButton
import pprint
import random
import sys
import os
import matplotlib
matplotlib.use('WXAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import \
     FigureCanvasWxAgg as FigCanvas, \
     NavigationToolbar2WxAgg as NavigationToolbar
import numpy as np
import pylab
import PySide
import sys
from scipy.fftpack import fft
from scipy.fftpack import fftshift
import thread
import time
from classes.Data import GetData

class graph(object):
    def __init__(self, size_hor, size_ver, title):
        self.dpi = 100
        self.size_hor = size_hor
        self.size_ver = size_ver
        self.title = title
        self.getdata = GetData()
        self.bottom_x = [self.getdata.Data_bottom_x()]
        self.bottom_y = [self.getdata.Data_bottom_y()]
        
    def init_plot(self):
        fig2 = Figure((self.size_hor, self.size_ver), dpi=self.dpi)
       
        axes = self.fig2.add_subplot(111)
        axes.set_axis_bgcolor('black')
        axes.set_title(self.title, size=20)
        
        pylab.setp(self.axes.get_xticklabels(), fontsize=6)
        pylab.setp(self.axes.get_yticklabels(), fontsize=6)
        plot_data = self.axes.plot(self.bottom_x, self.bottom_y,linewidth=1,color=(1 , 0, 1)) [0]
  
        
    def draw_plot(self):
            #pylab.setp(self.axes.get_xticklabels(),
            #    visible=self.cb_xlab.IsChecked())
        plot_data.set_xdata(self.bottom_x)
        plot_data.set_ydata(self.bottom_y)  
            #self.canvas_bottom.show()
            
class plot(wx.Frame):
    def __init__(self): #inital values
        
        wx.Frame.__init__(self,None, title = 'Block Diagram Mode', size=(670,610)) #initialize frame
        self.Centre()   #center frame
        self.getdata = GetData()
        self.x = self.arr = np.loadtxt("file1.txt")#self.getdata.Data_top_x()
        self.y = self.arr1 = np.loadtxt("file2.txt")#self.getdata.Data_top_y()
        self.bottom_x = self.arr_bot = np.loadtxt("file3.txt")#self.getdata.Data_bottom_x()
        self.bottom_y = self.arr_bot1 = np.loadtxt("file4.txt")#self.getdata.Data_bottom_y()
        
    def main_panel(self):
        self.panel=wx.Panel(self)
        self.a = graph(3,3,"dick")
        canvas = FigCanvas(self.panel, -1, self.a.figure())
        
if __name__=='__main__':
    app = wx.PySimpleApp() #App(False)
    app.frame= plot() #, title='Block Diagram Mode'
    app.frame.Show()
    app.MainLoop()
