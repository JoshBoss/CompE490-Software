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
#from __main__ import *
import sys
from scipy.fftpack import fft
from scipy.fftpack import fftshift
import thread
import time
from Data import GetData
import settings 

class Graph(wx.Panel):
    def __init__(self, parent, ID, title, paused, fourier):#, ID, size_hor, size_ver, title):
        wx.Panel.__init__(self, parent, ID)
        self.title = title
        self.getdata = GetData()
        self.x = self.getdata.Data_top_x()
        self.y = self.getdata.Data_top_y()
        self.bottom_x = self.getdata.Data_bottom_x()
        self.bottom_y = self.getdata.Data_bottom_y()
        self.init_plot()
        self.canvas = FigCanvas(self, -1, self.fig) 
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.paused = settings.paused
        self.fourier = settings.fourier
        print settings.fourier
        self.redraw_timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.on_redraw_timer, self.redraw_timer)
        self.redraw_timer.Start(100)
        
    def OnSize(self, event):
        size = self.GetSize()
        self.canvas.SetSize(size)       
        

    def init_plot(self):
        self.fig = Figure(tight_layout = True)
        self.axes = self.fig.add_subplot(211)
        self.axes.set_axis_bgcolor('black')
        self.axes.set_title(self.title, size=20)
        pylab.setp(self.axes.get_xticklabels(), fontsize=8)
        pylab.setp(self.axes.get_yticklabels(), fontsize=8)
        self.axes.grid(True, color='white')
        self.plot_data = self.axes.plot(self.x, self.y,linewidth=1,color=(1 , 0, 1)) [0]
        
        self.axes2 = self.fig.add_subplot(212)
        self.axes2.set_title('Voltage', size=20)
        self.axes2.set_axis_bgcolor('black')
        pylab.setp(self.axes2.get_xticklabels(), fontsize=8)
        pylab.setp(self.axes2.get_yticklabels(), fontsize=8)
        self.axes2.grid(True, color='white')
        self.plot_data2 = self.axes2.plot(self.bottom_x, self.bottom_y,linewidth=1,color=(1 , 0, 1)) [0]
       
    def draw_plot(self):
            self.x = self.getdata.Data_top_x()
            self.y = self.getdata.Data_top_y()
            self.bottom_x = self.getdata.Data_bottom_x()
            self.bottom_y = self.getdata.Data_bottom_y()
            if self.fourier:
                self.plot_data.set_xdata(self.x)
                self.plot_data.set_ydata(self.y) 
            elif not self.fourier:
                self.plot_data.set_xdata(self.x)
                self.plot_data.set_ydata(fft(self.y))
            self.plot_data2.set_xdata(self.bottom_x)
            self.plot_data2.set_ydata(self.bottom_y) 
            self.canvas.draw()
    
    #def draw_plot(self):
    #        self.x = self.getdata.Data_top_x()
    #        self.y = self.getdata.Data_top_y()
    #        if self.fourier:
    #            self.plot_data.set_xdata(self.x)
    #            self.plot_data.set_ydata(self.y) 
    #        elif not self.fourier:
    #            self.plot_data.set_xdata(self.x)
    #            self.plot_data.set_ydata(fft(self.y))
    #        self.canvas.draw()
    #            
    #def draw_plot2(self):
    #       self.bottom_x = self.getdata.Data_bottom_x()
    #       self.bottom_y = self.getdata.Data_bottom_y()
    #       self.plot_data2.set_xdata(self.bottom_x)
    #       self.plot_data2.set_ydata(self.bottom_y)
    #       self.canvas.draw()
            
    def on_redraw_timer(self, event):

          if  self.paused: #not
              self.x.append(self.getdata.Data_top_x())
              self.y.append(self.getdata.Data_top_y())
              self.bottom_x.append(self.getdata.Data_bottom_x())
              self.bottom_y.append(self.getdata.Data_bottom_y())
          #self.draw_plot()
  