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

#a = self.axes.plot() [0]

class GetData(object):
    def __init__(self):  
        self.arr = []
        self.arr1 = []
    def Datax(self):
        self.arr = np.loadtxt("file3.txt")
        return self.arr
    
    def Datay(self):
        self.arr1 = np.loadtxt("file4.txt")
        return self.arr1

    
class mf(wx.Frame): #Main frame

    def __init__(self): #inital values
        
        wx.Frame.__init__(self,None, title = 'Block Diagram Mode', size=(670,610)) #initialize frame
        self.Centre()   #center frame
        self.getdata = GetData()
        self.x = [self.getdata.Datax()]
        self.y = [self.getdata.Datay()]
        self.paused = False
        self.fourier= False

        self.create_menu()
        self.main_panel()

        self.redraw_timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.on_redraw_timer, self.redraw_timer)
        self.redraw_timer.Start(100)

    def create_menu(self):
        menubar = wx.MenuBar()  #init menu bar
        modemenu = wx.Menu()    #mode
        #graphmenu = wx.Menu()   #graph
        menubar.Append(modemenu, '&Mode')   #mode under menu
        self.SetMenuBar(menubar)    #function here
        
        mmcm = modemenu.Append(1, 'Configuration Mode') #Configuration and kids mode subsections of mode
        mmkm = modemenu.Append(1, 'Kids Mode')

        self.Bind(wx.EVT_MENU, self.cm, mmcm)   #binding event to definition
        self.Bind(wx.EVT_MENU, self.km, mmkm)   #...
        
        

    def main_panel(self):
        self.panel=wx.Panel(self)    #init panel
    
        self.init_plot()
        self.canvas = FigCanvas(self.panel, -1, self.fig)
        
        self.SetBackgroundColour('GRAY')    #set bg color gray
        
        self.vbox = wx.BoxSizer(wx.VERTICAL)         #main box sizer
                                                #everything goes in it
        hlabel = wx.BoxSizer(wx.HORIZONTAL)     #row 1 (top row) horizontal sizer
        
        self.labeli1= wx.StaticText(self.panel, label='1', size = (20,20), style=wx.ALIGN_CENTRE)
        self.labeli2= wx.StaticText(self.panel, label='2', size = (20,20), style=wx.ALIGN_CENTRE)
        self.labeli1.SetBackgroundColour('green')    #inverter label initialization & on/off color coding
        self.labeli2.SetBackgroundColour('green')
        hlabel.Add(self.labeli1, flag=wx.RIGHT, border=5)    #add inverter on/off label to first horizontal sizer
        hlabel.Add(self.labeli2, flag=wx.RIGHT, border= 70)  #add inverter2 ...

        self.labelf1= wx.StaticText(self.panel, label='1', size = (20,20), style=wx.ALIGN_CENTRE) #filter 1 label initialization & on/off color coding
        self.labelf2= wx.StaticText(self.panel, label='2', size = (20,20), style=wx.ALIGN_CENTRE) #filter 2 ...
        self.labelf3= wx.StaticText(self.panel, label='3', size = (20,20), style=wx.ALIGN_CENTRE) #filter 3 ...
        self.labelf1.SetBackgroundColour('green')    #set background color
        self.labelf2.SetBackgroundColour('green')
        self.labelf3.SetBackgroundColour('green')
        hlabel.Add(self.labelf1, flag=wx.RIGHT, border=5) #add filter 1 to first horizontal sizer, pushes next label 5 pixels to the right   
        hlabel.Add(self.labelf2, flag=wx.RIGHT, border=5) #add filter 2 ...
        hlabel.Add(self.labelf3, flag=wx.RIGHT, border=5) #add filter 3 ...

        self.vbox.Add(hlabel, flag=wx.LEFT, border=50)    #add horizontal label to main vertical sizer


        hvtn = wx.BoxSizer(wx.HORIZONTAL)   #second horizontal (row)
    
        vbtn = wx.BoxSizer(wx.VERTICAL) #vertical sizer in second horizontal row (sizers stack from left -> right)
        btni1=wx.ToggleButton(self.panel, -1, label=('Inverter 1'))  #first inverter button intialization
        btni2=wx.ToggleButton(self.panel, -1, label=('Inverter 2'))  #second ...
        self.labeliv= wx.StaticText(self.panel, label='0.00V', size = (50,20), style=wx.ALIGN_CENTRE) #inverter voltage value label
        self.labelic= wx.StaticText(self.panel, label='0.00A', size = (50,20), style=wx.ALIGN_CENTRE) #inverter current ...
        self.labeliv.SetBackgroundColour('white')    #set background color to white
        self.labelic.SetBackgroundColour('white')
        vbtn.Add(btni1, flag=wx.BOTTOM, border = 20)    #add inv 1 to vertical sizer, pushes next button down 20 pixels
        vbtn.Add(btni2) #goes beneath it
        hlabeli = wx.BoxSizer(wx.HORIZONTAL) #horizontal sizer for put labels under inv buttons (one by the other)
        hlabeli.Add(self.labeliv)    #add inv voltage label to sizer
        hlabeli.Add(self.labelic)    #add current...
        vbtn.Add(hlabeli)   #add horizontal sizer to row 2 column 1 sizer
        
        hvtn.Add(vbtn, flag=wx.LEFT, border=30) #add column 1 to row 2
        
        vbtnf = wx.BoxSizer(wx.VERTICAL)    #filter buttons vertical sizer (row 2 column 2)
        btnf1=wx.ToggleButton(self.panel, -1, label=('Filter 1'))    #intialize filter buttons
        btnf2=wx.ToggleButton(self.panel, -1, label=('Filter 2'))
        btnf3=wx.ToggleButton(self.panel, -1, label=('Filter 3'))
        self.labelfv= wx.StaticText(self.panel, label='0.00V', size = (50,20),  style=wx.ALIGN_CENTRE)    #voltage value label
        self.labelfc= wx.StaticText(self.panel, label='0.00A', size = (50,20),  style=wx.ALIGN_CENTRE)    #current...
        self.labelfv.SetBackgroundColour('white')    #set bg color to white
        self.labelfc.SetBackgroundColour('white')
        vbtnf.Add(btnf1, flag = wx.BOTTOM, border=5)    #add filter button to vertical sizer, pushes down 5 pixels
        vbtnf.Add(btnf2, flag = wx.BOTTOM, border=5)
        vbtnf.Add(btnf3, flag = wx.BOTTOM, border=5)
        hlabelf = wx.BoxSizer(wx.HORIZONTAL)    #horizontal sizer for filter voltage and current labels
        hlabelf.Add(self.labelfv)    #add filter values to sizer
        hlabelf.Add(self.labelfc)
        vbtnf.Add(hlabelf)  #horizontal sizer goes beneath virtical one (row 3 column 2)
        hvtn.Add(vbtnf, flag=wx.LEFT, border=40)    #add it to column 2

        vbtnl = wx.BoxSizer(wx.VERTICAL)    #vertical sizer for load buttons (row 2 column 3)
        btnload1=wx.ToggleButton(self.panel, -1, label=('Load 1'))   #initialize load buttons
        btnload2=wx.ToggleButton(self.panel, -1, label=('Load 2'))
        btnload3=wx.ToggleButton(self.panel, -1, label=('Load 3'))  
        vbtnl.Add(btnload1, flag = wx.BOTTOM, border=5) #add buttons to vertical sizer
        vbtnl.Add(btnload2, flag = wx.BOTTOM, border=5)
        vbtnl.Add(btnload3, flag = wx.BOTTOM, border=5)
        hvtn.Add(vbtnl, flag=wx.LEFT, border=40)    #add vertical sizer to row 2

        vlabel = wx.BoxSizer(wx.VERTICAL)   #vertical sizer for load label
        self.labelload1= wx.StaticText(self.panel, label='1', size = (20,20), style=wx.ALIGN_CENTRE)  #on/off color coded labels
        self.labelload2= wx.StaticText(self.panel, label='2', size = (20,20), style=wx.ALIGN_CENTRE)
        self.labelload3= wx.StaticText(self.panel, label='3', size = (20,20), style=wx.ALIGN_CENTRE)
        self.labelload1.SetBackgroundColour('green') #init color coding to green
        self.labelload2.SetBackgroundColour('green')
        self.labelload3.SetBackgroundColour('green')
        vlabel.Add(self.labelload1, flag=wx.TOP, border=3)   #add labels to vertical sizer
        vlabel.Add(self.labelload2, flag=wx.TOP, border=12)
        vlabel.Add(self.labelload3, flag=wx.TOP, border=12)
        hvtn.Add(vlabel, flag=wx.LEFT, border=5)    #add vertical sizer to row 2

        
        vloadval = wx.BoxSizer(wx.VERTICAL) #load value vertical sizer
        self.labelload1v= wx.StaticText(self.panel, label='0.00V', size = (50,20), style=wx.ALIGN_CENTRE) #init current and voltage labels for all 3 loads
        self.labelload1c= wx.StaticText(self.panel, label='0.00A', size = (50,20), style=wx.ALIGN_CENTRE)
        self.labelload2v= wx.StaticText(self.panel, label='0.00V', size = (50,20), style=wx.ALIGN_CENTRE)
        self.labelload2c= wx.StaticText(self.panel, label='0.00A', size = (50,20), style=wx.ALIGN_CENTRE)
        self.labelload3v= wx.StaticText(self.panel, label='0.00V', size = (50,20), style=wx.ALIGN_CENTRE)
        self.labelload3c= wx.StaticText(self.panel, label='0.00A', size = (50,20), style=wx.ALIGN_CENTRE)
        self.labelload1v.SetBackgroundColour('white')    #set bg color to white
        self.labelload1c.SetBackgroundColour('white')
        self.labelload2v.SetBackgroundColour('white')
        self.labelload2c.SetBackgroundColour('white')
        self.labelload3v.SetBackgroundColour('white')
        self.labelload3c.SetBackgroundColour('white')
        vloadval.Add(self.labelload1v)   #add load value labels to vertical sizer
        vloadval.Add(self.labelload1c)
        vloadval.Add(self.labelload2v, flag=wx.TOP, border=10)
        vloadval.Add(self.labelload2c)
        vloadval.Add(self.labelload3v, flag=wx.TOP, border=10)
        vloadval.Add(self.labelload3c)
        hvtn.Add(vloadval, flag=wx.LEFT, border=5)  #add virtical sizer to row 2
        
        vlabelrt = wx.BoxSizer(wx.VERTICAL) #vertical sizer for system, wifi and time labels (delete to have it at far right end of the window
        self.labelsys= wx.StaticText(self.panel, label='ON', size = (100,20), style=wx.ALIGN_CENTRE)  #sys on/off label
        self.labelwifi= wx.StaticText(self.panel, label='Connected', size = (100,20), style=wx.ALIGN_CENTRE)  #wifi connected/disconnected label
        self.labeltime= wx.StaticText(self.panel, label='00:00 xx/xx/xx', size = (100,20), style=wx.ALIGN_CENTRE) #uptime label
        self.labelsys.SetBackgroundColour('green')   #set bg colors
        self.labelwifi.SetBackgroundColour('green')
        self.labeltime.SetBackgroundColour('white')
        vlabelrt.Add(self.labelsys, flag=wx.ALIGN_RIGHT) #add to vertical sizer
        vlabelrt.Add(self.labelwifi, flag=wx.ALIGN_RIGHT)
        vlabelrt.Add(self.labeltime, flag=wx.ALIGN_RIGHT)
        hvtn.Add(vlabelrt, flag=wx.ALIGN_RIGHT) #add vertical sizer to row 2
        self.vbox.Add(hvtn)  #add row 2 to main vertical sizer
    
#####################################
        labelvoltage= wx.StaticText(self.panel, label='Voltage', size = (100,20))    #label " Voltage" for second graph
        graphpan = wx.Panel(self.panel) #initializing first graph panel
        graphpan.SetBackgroundColour('red') #setting the bg color
        #self.canvas = canvas(self.panel) #initializing second graph panel
        self.vbox.Add(self.canvas, proportion=1, flag=wx.EXPAND) #############################################
        self.vbox.Add(labelvoltage)
        self.vbox.Add(graphpan, proportion=1, flag=wx.EXPAND)
        
        #self.vbox.Add(self.canvas, proportion=1, flag=wx.EXPAND)
####################################
        
        self.pause_button = wx.Button(self.panel, -1, "pause")
        self.Bind(wx.EVT_BUTTON, self.on_pause_button, self.pause_button)
        self.Bind(wx.EVT_UPDATE_UI, self.on_update_pause_button, self.pause_button)
        self.fft_button = wx.Button(self.panel, -1, "fft-off")
        self.Bind(wx.EVT_BUTTON, self.on_fft_button, self.fft_button)
        self.Bind(wx.EVT_UPDATE_UI, self.on_update_fft_button, self.fft_button)
        
        self.cb_grid = wx.CheckBox(self.panel, -1,
                                 "Show Grid")
        self.Bind(wx.EVT_CHECKBOX, self.on_cb_grid, self.cb_grid)
        self.cb_grid.SetValue(True)

        self.cb_xlab = wx.CheckBox(self.panel, -1,
                    "Show X labels")
        self.Bind(wx.EVT_CHECKBOX, self.on_cb_xlab, self.cb_xlab)
        self.cb_xlab.SetValue(True)

        self.newcodehbox = wx.BoxSizer(wx.HORIZONTAL)
        self.newcodehbox.Add(self.pause_button)
        self.newcodehbox.Add(self.fft_button)
        self.newcodehbox.Add(self.cb_grid, flag=wx.LEFT, border = 10)
        self.newcodehbox.AddSpacer(10)
        self.newcodehbox.Add(self.cb_xlab, flag=wx.LEFT, border= 10)
        self.vbox.Add(self.newcodehbox)
                             
        self.panel.SetSizer(self.vbox)    #link sizer functionality to main panel
        
        self.Bind(wx.EVT_TOGGLEBUTTON, self.i1, btni1)
        self.Bind(wx.EVT_TOGGLEBUTTON, self.i2, btni2)
        self.Bind(wx.EVT_TOGGLEBUTTON, self.f1, btnf1)
        self.Bind(wx.EVT_TOGGLEBUTTON, self.f2, btnf2)
        self.Bind(wx.EVT_TOGGLEBUTTON, self.f3, btnf3)
        self.Bind(wx.EVT_TOGGLEBUTTON, self.l1, btnload1)
        self.Bind(wx.EVT_TOGGLEBUTTON, self.l2, btnload2)
        self.Bind(wx.EVT_TOGGLEBUTTON, self.l3, btnload3)
        #self.Bind(wx.EVT_TOGGLEBUTTON, self.fft, fftbutton)

    def  on_fft_button(self, event):
            self.fourier = not self.fourier
    def on_update_fft_button(self,event):
            label = "fft-off" if self.fourier else "fft-on"
            self.fft_button.SetLabel(label)

    def init_plot(self):
        #global a
        self.dpi = 100
        self.fig = Figure((1.5, 3.0), dpi=self.dpi)
        self.axes = self.fig.add_subplot(111)
        self.axes.set_axis_bgcolor('black')
        self.axes.set_title('Current', size=20)

        pylab.setp(self.axes.get_xticklabels(), fontsize=6)
        pylab.setp(self.axes.get_xticklabels(), fontsize=6)
        
        self.axes.grid(True, color='white')
        self.plot_data = self.axes.plot(self.x, self.y,linewidth=1,color=(1 , 0, 1)) [0]
        


    
        
    def draw_plot(self):

            

            if self.cb_grid.IsChecked():
                self.axes.grid(True, color='white')
            else:
                self.axes.grid(False)
            #ymin = round(min(self.y), 0) 
            #ymax = round(max(self.y), 0) 
            #xmin = round(0, min(self.x))
            #xmax = round(0, max(self.x))
            #self.axes.set_xbound(lower=xmin, upper=xmax)
            #self.axes.set_ybound(lower=ymin, upper=ymax)
            #pylab.setp(self.axes.get_xticklabels(),
              #  visible=self.cb_xlab.IsChecked())
            pylab.setp(self.axes.get_xticklabels(),
                visible=self.cb_xlab.IsChecked())
            #if self.fourier:
            #self.plot_data = self.axes.plot(self.x, self.y,linewidth=1,color=(1 , 0, 1)) [0]
            #elif not self.fourier:
             #   self.plot_data = self.axes.plot(self.x, fft(self.y),linewidth=1,color=(1 , 0, 1)) [0]
            self.plot_data.set_xdata(self.x)
            if self.fourier:
                self.plot_data.set_ydata(self.y)
            elif not self.fourier:
                self.plot_data.set_ydata(fft(self.y))
            #self.canvas.clear()
            self.canvas.draw()


    
    def on_pause_button(self, event):
            self.paused = not self.paused
            
    def on_update_pause_button(self, event):
            label = "Resume" if self.paused else "Pause"
            self.pause_button.SetLabel(label)

    def on_cb_grid(self, event):
            self.draw_plot()

    def on_cb_xlab(self, event):
            self.draw_plot()
            
    #def on_save_plot(self, event):
     #       file_choices = "PNG (*.png)|*.png"

     #       dlg = wx.FileDialog(
     #            self,
     #            message="Save plot as...",
     #            defaultDir=os.getcwd(), #Return a string representing the current working directory
     #            defaultFile="plot.png",
     #            wildcard=file_choices,
     #            style=wx.SAVE)

     #       if dlg.ShowModal() == wx.ID_OK:
     #           path = dlg.GetPath()
     #           self.canvas.print_figure(path, dpi=self.dpi)
     #           self.flash_status_message("Saved to %s" % path)

    def on_redraw_timer(self, event):

          if not self.paused:
              self.x.append(self.getdata.Datax())
              self.y.append(self.getdata.Datay())

          self.draw_plot()

#    def flash_status_message(self, msg, flash_len_ms=1500):
#             self.statusbar.SetStatusText(msg)
#             self.timeroff = wx.Timer(self)
#             self.Bind(
#                 wx.EVT_TIMER,
#                 self.on_flash_status_off,
#                 self.timeroff)
#             self.timeroff.Start(flash_lens_ms, oneShot=True)

#    def on_flash_status_off(self, event):
#            self.statusbar.SetStatusText('') 
            

    def i1(self,event):
        
        obj = event.GetEventObject()
        isPressed = obj.GetValue()

        if isPressed:
            self.labeli1.SetBackgroundColour('red')
            self.labeli1.SetForegroundColour('white')
        else:
            self.labeli1.SetBackgroundColour('green')
            self.labeli1.SetForegroundColour('black')
            
        self.labeli1.Refresh()

    def i2(self,event):
        
        obj = event.GetEventObject()
        isPressed = obj.GetValue()

        if isPressed:
            self.labeli2.SetBackgroundColour('red')
            self.labeli2.SetForegroundColour('white')
        else:
            self.labeli2.SetBackgroundColour('green')
            self.labeli2.SetForegroundColour('black')
            
            
        self.labeli2.Refresh()
        
    def f1(self,event):
        
        obj = event.GetEventObject()
        isPressed = obj.GetValue()

        if isPressed:
            self.labelf1.SetBackgroundColour('red')
            self.labelf1.SetForegroundColour('white')
        else:
            self.labelf1.SetBackgroundColour('green')
            self.labelf1.SetForegroundColour('black')
            
        self.labelf1.Refresh()

    def f2(self,event):
        
        obj = event.GetEventObject()
        isPressed = obj.GetValue()

        if isPressed:
            self.labelf2.SetBackgroundColour('red')
            self.labelf2.SetForegroundColour('white')
        else:
            self.labelf2.SetBackgroundColour('green')
            self.labelf2.SetForegroundColour('black')
            
        self.labelf2.Refresh()

    def f3(self,event):
        obj = event.GetEventObject()
        isPressed = obj.GetValue()

        if isPressed:
            self.labelf3.SetBackgroundColour('red')
            self.labelf3.SetForegroundColour('white')
        else:
            self.labelf3.SetBackgroundColour('green')
            self.labelf3.SetForegroundColour('black')
            
        self.labelf3.Refresh()

    def l1(self,event):
        
        obj = event.GetEventObject()
        isPressed = obj.GetValue()

        if isPressed:
            self.labelload1.SetBackgroundColour('yellow')
            self.labelload1.SetForegroundColour('black')
        else:
            self.labelload1.SetBackgroundColour('green')
            self.labelload1.SetForegroundColour('white')
            
        self.labelload1.Refresh()

    def l2(self,event):
        
        obj = event.GetEventObject()
        isPressed = obj.GetValue()

        if isPressed:
            self.labelload2.SetBackgroundColour('yellow')
            self.labelload2.SetForegroundColour('black')
        else:
            self.labelload2.SetBackgroundColour('green')
            self.labelload2.SetForegroundColour('white')
            
        self.labelload2.Refresh()

    def l3(self,event):
        
        obj = event.GetEventObject()
        isPressed = obj.GetValue()

        if isPressed:
            self.labelload3.SetBackgroundColour('yellow')
            self.labelload3.SetForegroundColour('black')
        else:
            self.labelload3.SetBackgroundColour('green')
            self.labelload3.SetForegroundColour('white')
            
        self.labelload3.Refresh()      
        
    #def fft(self,event):
     #   global a
      #  obj = event.GetEventObject()
       # isPressed = obj.GetValue()

       # if isPressed:
       #     a = self.axes.plot(arr,arr1,linewidth=1,color=(1 , 0, 0)) [0]
            
       # else:
       #     a = self.axes.plot(arr,fft(arr1),linewidth=1,color=(1 , 0, 0)) [0]
            
       # return a
            
                  


    def cm(self, e):    #configuration frame event
        frame = sf()
        frame.Show()
    
    def km(self, e):    #kids frame event
        frame2 = tf()
        frame2.Show()

    

class sf(wx.Frame): #configuartion frame
    def __init__(self):
        wx.Frame.__init__(self,None, title = 'Configuration Mode', size=(500,350))  #initialize frame
        panel = wx.Panel(self)#init panel

    
class tf(wx.Frame): #kids frame
    def __init__(self):
        wx.Frame.__init__(self,None, title = 'Kids Mode', size=(500,350))   #initialize frame
        panel = wx.Panel(self)  #init panel

            
if __name__=='__main__':
    app = wx.PySimpleApp() #App(False)
    app.frame= mf() #, title='Block Diagram Mode'
    app.frame.Show()
    app.MainLoop()
