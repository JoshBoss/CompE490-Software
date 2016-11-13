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
#from matplotlib.pyplot import figure, show
import numpy as np
import pylab
import PySide
import sys
from scipy.fftpack import fft
from scipy.fftpack import fftshift
import thread
import time
from classes.Data import GetData

class ZoomPan:
    def __init__(self):
        self.press = None
        self.cur_xlim = None
        self.cur_ylim = None
        self.x0 = None
        self.y0 = None
        self.x1 = None
        self.y1 = None
        self.xpress = None
        self.ypress = None


    def zoom_factory(self, ax, base_scale = 2.):
        def zoom(event):
            cur_xlim = ax.get_xlim()
            cur_ylim = ax.get_ylim()

            xdata = event.xdata # get event x location
            ydata = event.ydata # get event y location

            if event.button == 'down':
                # deal with zoom in
                scale_factor = 1 / base_scale
            elif event.button == 'up':
                # deal with zoom out
                scale_factor = base_scale
            else:
                # deal with something that should never happen
                scale_factor = 1
                print event.button

            new_width = (cur_xlim[1] - cur_xlim[0]) * scale_factor
            new_height = (cur_ylim[1] - cur_ylim[0]) * scale_factor

            relx = (cur_xlim[1] - xdata)/(cur_xlim[1] - cur_xlim[0])
            rely = (cur_ylim[1] - ydata)/(cur_ylim[1] - cur_ylim[0])

            ax.set_xlim([xdata - new_width * (1-relx), xdata + new_width * (relx)])
            ax.set_ylim([ydata - new_height * (1-rely), ydata + new_height * (rely)])
            ax.figure.canvas.draw()

        fig = ax.get_figure() # get the figure of interest
        fig.canvas.mpl_connect('scroll_event', zoom)

        return zoom

    def pan_factory(self, ax):
        def onPress(event):
            if event.inaxes != ax: return
            self.cur_xlim = ax.get_xlim()
            self.cur_ylim = ax.get_ylim()
            self.press = self.x0, self.y0, event.xdata, event.ydata
            self.x0, self.y0, self.xpress, self.ypress = self.press

        def onRelease(event):
            self.press = None
            ax.figure.canvas.draw()

        def onMotion(event):
            if self.press is None: return
            if event.inaxes != ax: return
            dx = event.xdata - self.xpress
            dy = event.ydata - self.ypress
            self.cur_xlim -= dx
            self.cur_ylim -= dy
            ax.set_xlim(self.cur_xlim)
            ax.set_ylim(self.cur_ylim)

            ax.figure.canvas.draw()

        fig = ax.get_figure() # get the figure of interest

        # attach the call back
        fig.canvas.mpl_connect('button_press_event',onPress)
        fig.canvas.mpl_connect('button_release_event',onRelease)
        fig.canvas.mpl_connect('motion_notify_event',onMotion)

        #return the function
        return onMotion       

#class ZoomPan:
#    def __init__(self):
#        self.press = None
#        self.curxlim = None
#        self.curylim = None
#        self.x1 = None
#        self.x2 = None
#        self.y1 = None
#        self.y2 = None
#        self.xpress = None
#        self.ypress = None
#                    
#    def zoom_factory(self, ax, base_scale = 2.):
#        def zoom_fun(event):
#            cur_xlim=self.axes.get_xlim()
#            cur_ylim=self.axes.get_xylim()
#            xdata = event.xdata
#            ydata = event.ydata
#            
#            if event.button == 'down':
#                scale_factor = 1 / base_scale
#            elif event.button == 'up':
#                scale_factor = base_scale
#            else:
#                scale_factor = 1
#                print event.button
#            new_width = (cur_xlim[1] - cur_xlim[0]) * scale_factor
#            new_height = (cur_ylim[1] - cur_ylim[0]) * scale_factor
#            
#            relx = (cur_xlim[1] - xdata)/(cur_xlim[1] - cur_xlim[0])
#            rely = (cur_ylim[1] - ydata)/(cur_ylim[1] - cur_ylim[0])
#            ax.set_xlim([xdata - new_width * (1-relx), xdata + new_width * (relx)])
#            ax.set_ylim([ydata - new_height * (1-rely), ydata + new_height * (rely)])
#            ax.figure.canvas.draw()
#        fig2 = ax.get_figure()
#        fig2.canvas.mpl_connect('scroll_event', zoom)
#        
#        return zoom   
#             
#    def pan_factory(self, ax):
#        def onPress(event):
#            if event.inaxes != ax: return
#            self.cur_xlim = ax.get_xlim()
#            self.cur_ylim = ax.get_ylim()
#            self.press = self.x1, self.y1, event.xdata, event.ydata
#            self.x1, self.y1, self.xpress, self.ypress = self.press
#
#        def onRelease(event):
#            self.press = None
#            ax.figure.canvas.draw()
#
#        def onMotion(event):
#            if self.press is None: return
#            if event.inaxes != ax: return
#            dx = event.xdata - self.xpress
#            dy = event.ydata - self.ypress
#            self.cur_xlim -= dx
#            self.cur_ylim -= dy
#            ax.set_xlim(self.cur_xlim)
#            ax.set_ylim(self.cur_ylim)
#
#            ax.figure.canvas.draw()
#
#        fig2 = ax.get_figure() # get the figure of interest
#
#        # attach the call back
#        fig2.canvas.mpl_connect('button_press_event',onPress)
#        fig2.canvas.mpl_connect('button_release_event',onRelease)
#        fig2.canvas.mpl_connect('motion_notify_event',onMotion)
#
#        #return the function
#        return onMotion 
    
class main_frame(wx.Frame): #Main frame

    def __init__(self): #inital values
        
        wx.Frame.__init__(self,None, title = 'Main Mode', size=(800,610)) #initialize frame
        self.Centre()   #center frame
        self.getdata = GetData()
        self.x = self.getdata.Data_top_x()
        self.y = self.getdata.Data_top_y()
        self.bottom_x = self.getdata.Data_bottom_x()
        self.bottom_y = self.getdata.Data_bottom_y()
        
        self.paused = False
        self.fourier= True

        self.create_menu()
        self.InitUI()
        #self.sp()
        #self.tp()

        self.redraw_timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.on_redraw_timer, self.redraw_timer)
        self.redraw_timer.Start(100)

    def create_menu(self):
        menubar = wx.MenuBar()  #init menu bar
        mode_menu = wx.Menu()    #mode
        graph_menu = wx.Menu()   #graph settings
        menubar.Append(mode_menu, '&Mode')   #mode under menu
        menubar.Append(graph_menu, '&Graph')
        m_main_mode = mode_menu.Append(wx.ID_ANY, 'Main Mode')
        m_config_mode = mode_menu.Append(wx.ID_ANY, 'Configuration Settings') #Configuration and kids mode subsections of mode
        m_kids_mode = mode_menu.Append(wx.ID_ANY, 'Kids Mode')
        g_save = graph_menu.Append(wx.ID_ANY, 'Save')
        
        self.SetMenuBar(menubar)    #function here      
        self.Bind(wx.EVT_MENU, self.on_main_mode, m_main_mode)
        self.Bind(wx.EVT_MENU, self.on_config_mode, m_config_mode)   #binding event to definition
        self.Bind(wx.EVT_MENU, self.on_kids_mode, m_kids_mode)   #...
        self.Bind(wx.EVT_MENU, self.on_save_plot, g_save)

    def InitUI(self):
        self.sizer = wx.BoxSizer() #main window sizer
        self.panel=wx.Panel(self, -1)    #init main_mode panel
        self.sizer.Add(self.panel, 1, flag=wx.EXPAND)
        self.init_plot()
        self.canvas = FigCanvas(self.panel, -1, self.fig)

        self.SetBackgroundColour('GRAY')    #set bg color gray
        
        
        self.vbox = wx.BoxSizer(wx.VERTICAL)         #main box sizer
                                                #everything goes in it
        #hlabel = wx.BoxSizer(wx.HORIZONTAL)     #row 1 (top row) horizontal sizer

        
            
        
        
        #hlabel.Add(self.labeli1, flag=wx.RIGHT, border=5)    #add inverter on/off label to first horizontal sizer
        #hlabel.Add(self.labeli2, flag=wx.RIGHT, border= 70)  #add inverter2 ...


        #hlabel.Add(self.labelf1, flag=wx.RIGHT, border=5) #add filter 1 to first horizontal sizer, pushes next label 5 pixels to the right   
        #hlabel.Add(self.labelf2, flag=wx.RIGHT, border=5) #add filter 2 ...
        #hlabel.Add(self.labelf3, flag=wx.RIGHT, border=5) #add filter 3 ...

        #self.vbox.Add(hlabel, flag=wx.LEFT, border=50)    #add horizontal label to main vertical sizer


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
        hlabeli.Add(self.labeliv, flag = wx.RIGHT, border=2)    #add inv voltage label to sizer
        hlabeli.Add(self.labelic)    #add current...
        vbtn.Add(hlabeli)   #add horizontal sizer to row 2 column 1 sizer
        hvtn.Add(vbtn, flag=wx.LEFT, border=30) #add column 1 to row 2
        
        vertical_inv_sizer = wx.BoxSizer(wx.VERTICAL)
        self.labeli1= wx.StaticText(self.panel, label='1', size = (20,20), style=wx.ALIGN_CENTRE)
        self.labeli2= wx.StaticText(self.panel, label='2', size = (20,20), style=wx.ALIGN_CENTRE)
        self.labeli1.SetBackgroundColour('green')    #inverter label initialization & on/off color coding
        self.labeli2.SetBackgroundColour('green')
        vertical_inv_sizer.Add(self.labeli1, flag=wx.BOTTOM, border=25)    #add inverter on/off label to first vertical sizer
        vertical_inv_sizer.Add(self.labeli2)    #add inverter2 ...
        hvtn.Add(vertical_inv_sizer)
        

        
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
        hlabelf.Add(self.labelfv, flag = wx.RIGHT, border =2)    #add filter values to sizer
        hlabelf.Add(self.labelfc)
        vbtnf.Add(hlabelf)  #horizontal sizer goes beneath virtical one (row 3 column 2)
        hvtn.Add(vbtnf, flag=wx.LEFT, border=40)    #add it to column 2
        
        vertical_filter_sizer = wx.BoxSizer(wx.VERTICAL)
        self.labelf1= wx.StaticText(self.panel, label='1', size = (20,20), style=wx.ALIGN_CENTRE) #filter 1 label initialization & on/off color coding
        self.labelf2= wx.StaticText(self.panel, label='2', size = (20,20), style=wx.ALIGN_CENTRE) #filter 2 ...
        self.labelf3= wx.StaticText(self.panel, label='3', size = (20,20), style=wx.ALIGN_CENTRE) #filter 3 ...
        self.labelf1.SetBackgroundColour('green')    #set background color
        self.labelf2.SetBackgroundColour('green')
        self.labelf3.SetBackgroundColour('green')
        vertical_filter_sizer.Add(self.labelf1, flag=wx.BOTTOM, border=10)#add filter 1 to vertical sizer, pushes next label 10 pixels to the bottom
        vertical_filter_sizer.Add(self.labelf2, flag=wx.BOTTOM, border=11)#add filter 2...
        vertical_filter_sizer.Add(self.labelf3)#add filter 3...
        hvtn.Add(vertical_filter_sizer)

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
        vlabelrt.Add(self.labelsys, flag = wx.TOP, border=25) #add to vertical sizer
        vlabelrt.Add(self.labelwifi, flag = wx.TOP, border=10)
        vlabelrt.Add(self.labeltime, flag = wx.TOP, border=10)
        hvtn.Add(vlabelrt, flag=wx.LEFT, border=20) #add vertical sizer to row 2
        
        
        self.pause_button = wx.Button(self.panel, -1, "pause")
        self.Bind(wx.EVT_BUTTON, self.on_pause_button, self.pause_button)
        self.Bind(wx.EVT_UPDATE_UI, self.on_update_pause_button, self.pause_button)
        
        self.fft_button = wx.Button(self.panel, -1 , "fft-off")
        self.Bind(wx.EVT_BUTTON, self.on_fft_button, self.fft_button)
        self.Bind(wx.EVT_UPDATE_UI, self.on_update_fft_button, self.fft_button)
        
        self.cb_grid = wx.CheckBox(self.panel, -1,
                                 "Top Grid")
        self.Bind(wx.EVT_CHECKBOX, self.on_cb_grid, self.cb_grid)
        self.cb_grid.SetValue(True)

        self.cb_grid2 = wx.CheckBox(self.panel, -1,
                    "Bottom Grid")
        self.Bind(wx.EVT_CHECKBOX, self.on_cb_grid_bottom, self.cb_grid2)
        self.cb_grid2.SetValue(True)

        settings_vertical = wx.BoxSizer(wx.VERTICAL)
        settings_vertical.Add(self.pause_button, flag=wx.TOP, border=20)
        settings_vertical.Add(self.fft_button, flag=wx.TOP, border=10)
        settings_vertical.Add(self.cb_grid, flag=wx.TOP, border = 10)
        settings_vertical.AddSpacer(10)
        settings_vertical.Add(self.cb_grid2)
        hvtn.Add(settings_vertical, flag=wx.LEFT, border=20)
        self.vbox.Add(hvtn)  #add row 2 to main vertical sizer
#################################################################################
        self.vbox.Add(self.canvas, proportion=1,  flag=wx.EXPAND) #############################################
#################################################################################
        
                             
        self.panel.SetSizer(self.vbox)    #link sizer to main panel
        
        self.Bind(wx.EVT_TOGGLEBUTTON, self.i1, btni1)
        self.Bind(wx.EVT_TOGGLEBUTTON, self.i2, btni2)
        self.Bind(wx.EVT_TOGGLEBUTTON, self.f1, btnf1)
        self.Bind(wx.EVT_TOGGLEBUTTON, self.f2, btnf2)
        self.Bind(wx.EVT_TOGGLEBUTTON, self.f3, btnf3)
        self.Bind(wx.EVT_TOGGLEBUTTON, self.l1, btnload1)
        self.Bind(wx.EVT_TOGGLEBUTTON, self.l2, btnload2)
        self.Bind(wx.EVT_TOGGLEBUTTON, self.l3, btnload3)
        
        self.panel2=wx.Panel(self, -1)
        self.sizer.Add(self.panel2, 1, flag=wx.EXPAND)
        self.panel2.Hide()
        self.vbox2 = wx.BoxSizer(wx.HORIZONTAL)
        b = wx.Button(self.panel2, label='button2', size=(50,50))
        self.vbox2.Add(b)
        self.panel2.SetSizer(self.vbox2)
        
        self.panel3=wx.Panel(self, -1)
        self.sizer.Add(self.panel3, 1, flag=wx.EXPAND)
        self.panel3.Hide()
        self.vbox3 = wx.BoxSizer(wx.HORIZONTAL)
        b2 = wx.Button(self.panel3, label='button3', size=(50,50))
        self.vbox3.Add(b2)
        self.panel3.SetSizer(self.vbox3)
        
        self.SetSizer(self.sizer) # Set main window sizer
        
    def  on_fft_button(self, event):
        self.fourier = not self.fourier
        self.draw_plot()
    def on_update_fft_button(self,event):
        label = "fft-off" if self.fourier else "fft-on"
        self.fft_button.SetLabel(label)

    def init_plot(self):
        self.dpi = 100
        self.fig = Figure((3.0, 3.0), dpi=self.dpi)
        self.axes = self.fig.add_subplot(111)
        self.axes.set_axis_bgcolor('black')
        self.axes.set_title('Current', size=20)

        pylab.setp(self.axes.get_xticklabels(), fontsize=6)
        pylab.setp(self.axes.get_yticklabels(), fontsize=6)
        
        self.axes.grid(True, color='white')
        self.plot_data = self.axes.plot(self.x, self.y,linewidth=1,color=(1 , 0, 1)) [0]
        scale = 1.1
        zp = ZoomPan()
        figZoom = zp.zoom_factory(self.axes, base_scale = scale)
        figPan = zp.pan_factory(self.axes)  
        #self.axes2 = self.fig.add_subplot(212)
        #self.axes2.set_title('Voltage', size=20)
        #self.axes2.set_axis_bgcolor('black')
        #pylab.setp(self.axes2.get_xticklabels(), fontsize=6)
        #pylab.setp(self.axes2.get_yticklabels(), fontsize=6)
        #
        #self.axes2.grid(True, color='white')
        #self.plot_data2 = self.axes2.plot(self.bottom_x, self.bottom_y,linewidth=1,color=(1 , 0, 1)) [0]
            
        
    def draw_plot(self):
            if self.cb_grid.IsChecked():
                self.axes.grid(True, color='white')
            else:
                self.axes.grid(False)
            if self.cb_grid2.IsChecked():
                self.axes2.grid(True, color='white')
            else:
                self.axes2.grid(False)
            #ymin = round(min(self.y), 0) 
            #ymax = round(max(self.y), 0) 
            #xmin = round(0, min(self.x))
            #xmax = round(0, max(self.x))
            #self.axes.set_xbound(lower=xmin, upper=xmax)
            #self.axes.set_ybound(lower=ymin, upper=ymax)

            if self.fourier:
                self.plot_data.set_xdata(self.x)
                self.plot_data.set_ydata(self.y) 
            elif not self.fourier:
                self.plot_data.set_xdata(self.x)
                self.plot_data.set_ydata(fft(self.y))
                
            self.plot_data2.set_xdata(self.bottom_x)
            self.plot_data2.set_ydata(self.bottom_y) 
            self.canvas.draw() 
            

    
    
    
    def on_pause_button(self, event):
            self.paused = not self.paused
            
    def on_update_pause_button(self, event):
            label = "Resume" if self.paused else "Pause"
            self.pause_button.SetLabel(label)

    def on_cb_grid(self, event):
           self.draw_plot()

    def on_cb_grid_bottom(self, event):
           self.draw_plot()
            
    def on_save_plot(self, event):
            file_choices = "PNG (*.png)|*.png"

            dlg = wx.FileDialog(
                 self,
                 message="Save plot as...",
                 defaultDir=os.getcwd(), #Return a string representing the current working directory
                 defaultFile="plot.png",
                 wildcard=file_choices,
                 style=wx.SAVE)

            if dlg.ShowModal() == wx.ID_OK:
                path = dlg.GetPath()
                #self.canvas.print_figure(path, dpi=self.dpi)
                
                self.flash_status_message("Saved to %s" % path)

    def on_redraw_timer(self, event):

          if not self.paused:
              self.x.append(self.getdata.Data_top_x())
              self.y.append(self.getdata.Data_top_y())
              self.bottom_x.append(self.getdata.Data_bottom_x())
              self.bottom_y.append(self.getdata.Data_bottom_y())

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
    
    def on_main_mode(self, event):
        self.panel.Show()
        self.panel2.Hide()
        self.panel3.Hide()
        self.sizer.Layout()
        

    def on_config_mode(self, event):    #configuration frame event
        self.panel2.Show()
        self.panel.Hide()
        self.panel3.Hide()
        self.sizer.Layout()
    
    def on_kids_mode(self, event):    #kids frame event
        self.panel3.Show()
        self.panel.Hide()
        self.panel2.Hide()
        self.sizer.Layout()


            
if __name__=='__main__':
    app = wx.App(False)#wx.PySimpleApp() 
    app.frame= main_frame() #, title='Block Diagram Mode'
    app.frame.Show()
    app.MainLoop()