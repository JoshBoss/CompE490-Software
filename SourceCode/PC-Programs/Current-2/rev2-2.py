import wx
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
from scipy.fftpack import fft
from scipy.fftpack import fftshift
import thread
from classes.Data import GetData
from classes.About import AboutDlg as about
from classes.Help import AboutDlg as help
from classes.Box import BoundControlBox

    
class main_frame(wx.Frame): #Main frame

    def __init__(self): #inital values
        on_top = wx.DEFAULT_FRAME_STYLE | wx.STAY_ON_TOP
        wx.Frame.__init__(self,None, title = 'Main Mode', size=(1100,810))#, style=on_top) #initialize frame
        self.Centre()   #center frame
        #self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.getdata = GetData()
        self.init_top = 0
        self.init_bottom = 0
        self.paused = False
        self.fourier= True
        self.x = self.getdata.Data_top_x()
        self.y = self.getdata.Data_top_y()
        self.bottom_x = self.getdata.Data_bottom_x()
        self.bottom_y = self.getdata.Data_bottom_y()

        self.create_menu()
        self.InitUI()

        self.redraw_timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.on_redraw_timer, self.redraw_timer)
        self.redraw_timer.Start(100)

    def create_menu(self):
        menubar = wx.MenuBar()  #init menu bar
        mode_menu = wx.Menu()    #mode
        graph_menu = wx.Menu()   #graph settings
        help_menu = wx.Menu()
        menubar.Append(mode_menu, '&Mode')   #mode under menu
        menubar.Append(graph_menu, '&Graph')
        menubar.Append(help_menu, '&Help')
        m_main_mode = mode_menu.Append(wx.ID_ANY, 'Main Mode')
        m_config_mode = mode_menu.Append(wx.ID_ANY, 'Configuration Settings') #Configuration and kids mode subsections of mode
        m_kids_mode = mode_menu.Append(wx.ID_ANY, 'Kids Mode')
        g_save = graph_menu.Append(wx.ID_ANY, 'Save Data')
        h_about = help_menu.Append(wx.ID_ANY, 'About')
        h_help = help_menu.Append(wx.ID_ANY, 'User Manual')
        
        self.SetMenuBar(menubar)    #function here      
        self.Bind(wx.EVT_MENU, self.on_main_mode, m_main_mode)
        self.Bind(wx.EVT_MENU, self.on_config_mode, m_config_mode)   #binding event to definition
        self.Bind(wx.EVT_MENU, self.on_kids_mode, m_kids_mode)   #...
        self.Bind(wx.EVT_MENU, self.on_save_data, g_save)
        self.Bind(wx.EVT_MENU, self.on_about, h_about)
        self.Bind(wx.EVT_MENU, self.on_help, h_help)

    def InitUI(self):
        self.SetBackgroundColour('GRAY')    #set bg color gray
        self.sizer = wx.BoxSizer() #main window sizer
        self.panel=wx.Panel(self, -1)    #init main_mode panel
        self.sizer.Add(self.panel, 1, flag=wx.EXPAND)
        self.init_plot()
        self.canvas = FigCanvas(self.panel, -1, self.fig)

        self.vbox = wx.BoxSizer(wx.VERTICAL)         #main box sizer
                                                #everything goes in it
                                                
        hvtn = wx.BoxSizer(wx.HORIZONTAL)   #second horizontal (row)
        
        vbtn = wx.BoxSizer(wx.VERTICAL) #vertical sizer in second horizontal row (sizers stack from left -> right)
        self.btni1=wx.ToggleButton(self.panel, -1, label=('Inverter 1'))  #first inverter button intialization
        self.btni2=wx.ToggleButton(self.panel, -1, label=('Inverter 2'))  #second ...
        self.labeliv= wx.StaticText(self.panel, label='0.00V', size = (50,20), style=wx.ALIGN_CENTRE) #inverter voltage value label
        self.labelic= wx.StaticText(self.panel, label='0.00A', size = (50,20), style=wx.ALIGN_CENTRE) #inverter current ...
        self.labeliv.SetBackgroundColour('white')    #set background color to white
        self.labelic.SetBackgroundColour('white')
        vbtn.Add(self.btni1, flag=wx.BOTTOM, border = 20)    #add inv 1 to vertical sizer, pushes next button down 20 pixels
        vbtn.Add(self.btni2, flag=wx.BOTTOM, border = 5) #goes beneath it
        hlabeli = wx.BoxSizer(wx.HORIZONTAL) #horizontal sizer for put labels under inv buttons (one by the other)
        hlabeli.Add(self.labeliv, flag = wx.RIGHT, border=2)    #add inv voltage label to sizer
        hlabeli.Add(self.labelic)    #add current...
        vbtn.Add(hlabeli)   #add horizontal sizer to row 2 column 1 sizer
        hvtn.Add(vbtn, flag=wx.LEFT, border=30) #add column 1 to row 2
        
        vbtnf = wx.BoxSizer(wx.VERTICAL)    #filter buttons vertical sizer (row 2 column 2)
        self.btnf1=wx.ToggleButton(self.panel, -1, label=('Filter 1'))    #intialize filter buttons
        self.btnf2=wx.ToggleButton(self.panel, -1, label=('Filter 2'))
        self.btnf3=wx.ToggleButton(self.panel, -1, label=('Filter 3'))
        self.labelfv= wx.StaticText(self.panel, label='0.00V', size = (50,20),  style=wx.ALIGN_CENTRE)    #voltage value label
        self.labelfc= wx.StaticText(self.panel, label='0.00A', size = (50,20),  style=wx.ALIGN_CENTRE)    #current...
        self.labelfv.SetBackgroundColour('white')    #set bg color to white
        self.labelfc.SetBackgroundColour('white')
        vbtnf.Add(self.btnf1, flag = wx.BOTTOM, border=5)    #add filter button to vertical sizer, pushes down 5 pixels
        vbtnf.Add(self.btnf2, flag = wx.BOTTOM, border=5)
        vbtnf.Add(self.btnf3, flag = wx.BOTTOM, border=5)
        hlabelf = wx.BoxSizer(wx.HORIZONTAL)    #horizontal sizer for filter voltage and current labels
        hlabelf.Add(self.labelfv, flag = wx.RIGHT, border =2)    #add filter values to sizer
        hlabelf.Add(self.labelfc)
        vbtnf.Add(hlabelf)  #horizontal sizer goes beneath virtical one (row 3 column 2)
        hvtn.Add(vbtnf, flag=wx.LEFT, border=40)    #add it to column 2

        vbtnl = wx.BoxSizer(wx.VERTICAL)    #vertical sizer for load buttons (row 2 column 3)
        self.btnload1=wx.ToggleButton(self.panel, -1, label=('Load 1'))   #initialize load buttons
        self.btnload2=wx.ToggleButton(self.panel, -1, label=('Load 2'))
        self.btnload3=wx.ToggleButton(self.panel, -1, label=('Load 3')) 
        vbtnl.Add(self.btnload1, flag = wx.TOP, border=8) #add buttons to vertical sizer
        vbtnl.Add(self.btnload2, flag = wx.TOP, border=23)
        vbtnl.Add(self.btnload3, flag = wx.TOP, border=23)
        hvtn.Add(vbtnl, flag=wx.LEFT, border=40)    #add vertical sizer to row 2

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
        
        self.fft_button = wx.Button(self.panel, -1 , "FFT-off")
        self.Bind(wx.EVT_BUTTON, self.on_fft_button, self.fft_button)
        self.Bind(wx.EVT_UPDATE_UI, self.on_update_fft_button, self.fft_button)
        
        #box = wx.StaticBox(self.panel, -1, "Number of graphs")
        #graph_sizer = wx.StaticBoxSizer(box, wx.VERTICAL)
        #self.radio_2graphs = wx.RadioButton(self.panel, -1,
        #        label="2", style=wx.RB_GROUP, size=(10,10))
        #self.radio_4graphs = wx.RadioButton(self.panel, -1,
        #        label="4", style=wx.RB_GROUP, size=(10,10))
        #graph_sizer.Add(self.radio_2graphs, -1, wx.ALL, 5)
        #graph_sizer.Add(self.radio_4graphs, -1, wx.ALL, 5)
  
        settings_vertical = wx.BoxSizer(wx.VERTICAL)
        settings_vertical.Add(self.pause_button, flag=wx.TOP, border=20)
        settings_vertical.Add(self.fft_button, flag=wx.TOP, border=10)
        #settings_vertical.Add(box, flag=wx.TOP, border=10)
        hvtn.Add(settings_vertical, flag=wx.LEFT, border=20)
        
        self.top_graph = BoundControlBox(self.panel, -1, "Top Graph", self.init_top)
        self.bottom_graph = BoundControlBox(self.panel, -1, "Bottom Graph", self.init_bottom)
        hvtn.Add(self.top_graph, border=5, flag=wx.ALL)
        hvtn.Add(self.bottom_graph, border=5, flag=wx.ALL)
        
        self.vbox.Add(hvtn)  #add row 2 to main vertical sizer
#################################################################################
        self.vbox.Add(self.canvas, proportion=1,  flag=wx.EXPAND) #############################################
#################################################################################                    
        self.panel.SetSizer(self.vbox)    #link sizer to main panel
        
        self.Bind(wx.EVT_TOGGLEBUTTON, self.i1, self.btni1)
        self.Bind(wx.EVT_TOGGLEBUTTON, self.i2, self.btni2)
        self.Bind(wx.EVT_TOGGLEBUTTON, self.f1, self.btnf1)
        self.Bind(wx.EVT_TOGGLEBUTTON, self.f2, self.btnf2)
        self.Bind(wx.EVT_TOGGLEBUTTON, self.f3, self.btnf3)
        self.Bind(wx.EVT_TOGGLEBUTTON, self.l1, self.btnload1)
        self.Bind(wx.EVT_TOGGLEBUTTON, self.l2, self.btnload2)
        self.Bind(wx.EVT_TOGGLEBUTTON, self.l3, self.btnload3)
        
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
        


    def init_plot(self):
        self.fig = Figure(tight_layout = True)#,subplotParams(wspace=0, hspace=0)
        self.axes = self.fig.add_subplot(211)
        self.axes.set_axis_bgcolor('black')
        self.axes.set_title('Current', size=20)

        pylab.setp(self.axes.get_xticklabels(), fontsize=8)
        pylab.setp(self.axes.get_yticklabels(), fontsize=8)
        
        self.axes.grid(True, color='white')
        self.plot_data = self.axes.plot(self.x, self.y,linewidth=1,color=(1 , 0, 1)) [0]
        
            
        self.axes2 = self.fig.add_subplot(212)
        self.axes2.set_title('Voltage', size=20)
        self.axes2.set_axis_bgcolor('black')
        pylab.setp(self.axes2.get_xticklabels(), fontsize=8)
        pylab.setp(self.axes2.get_yticklabels(), fontsize=8)
        self.init_top = max(self.y)#self.axes.get_ylim([1])
        self.init_bottom = max(self.bottom_y)#self.axes2.get_ylim([1])

         
        self.axes2.grid(True, color='white')
        self.plot_data2 = self.axes2.plot(self.bottom_x, self.bottom_y,linewidth=1,color=(1 , 0, 1)) [0]
            
        
    def draw_plot(self):
            self.x = self.getdata.Data_top_x()
            self.y = self.getdata.Data_top_y()
            self.bottom_x = self.getdata.Data_bottom_x()
            self.bottom_y = self.getdata.Data_bottom_y()

            if self.top_graph.on_grid():
                self.axes.grid(True, color='white')
            else:
                self.axes.grid(False)
            if self.bottom_graph.on_grid():
                self.axes2.grid(True, color='white')
            else:
                self.axes2.grid(False)
                
            #if self.top_graph.on_click():
            #    self.axes.relim()
            #    self.axes.autoscale()
            #if self.bottom_graph.on_click():
            #    self.axes2.relim()
            #    self.axes2.autoscale()
        
            if self.fourier:
                self.plot_data.set_xdata(self.x)
                self.plot_data.set_ydata(self.y) 
            elif not self.fourier:
                self.plot_data.set_xdata(self.x)
                self.plot_data.set_ydata(fft(self.y))
                
            self.plot_data2.set_xdata(self.bottom_x)
            self.plot_data2.set_ydata(self.bottom_y) 
            self.axes.set_ybound(upper=self.top_graph.update_value())
            self.axes2.set_ybound(upper=self.bottom_graph.update_value())
            #self.axes.set_ylim(self.top_graph.update_value(),self.top_graph.Update_value())#*self.axes.get_ybound())
            self.canvas.draw() 
            
    #Pause Button Controls
    def on_pause_button(self, event):
            self.paused = not self.paused
            
    def on_update_pause_button(self, event):
            label = "Resume" if self.paused else "Pause"
            self.pause_button.SetLabel(label)
            
    #Save Button Control       
    def on_save_data(self, event):
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
                
    #when paused append data
    def on_redraw_timer(self, event):

          if  self.paused: #not
              self.x.append(self.getdata.Data_top_x())
              self.y.append(self.getdata.Data_top_y())
              self.bottom_x.append(self.getdata.Data_bottom_x())
              self.bottom_y.append(self.getdata.Data_bottom_y())
          self.draw_plot()
    
    #FFT controls      
    def on_fft_button(self, event):
        self.fourier = not self.fourier
        self.draw_plot()
    def on_update_fft_button(self,event):
        label = "FFT-OFF" if self.fourier else "FFT-ON"
        self.fft_button.SetLabel(label)

    #Inverter Event Functions
    def i1(self,event):
        if self.btni1.GetValue():
            self.btni1.SetLabel("Inv 1-ON")
        else:
            self.btni1.SetLabel("Inv 1-OFF")   
        self.btni1.Refresh()

    def i2(self,event):
        if self.btni2.GetValue():
            self.btni2.SetLabel("Inv 2-ON")
        else:
            self.btni2.SetLabel("Inv 2-OFF")
        self.btni2.Refresh()
     
    #Filter Event Functions       
    def f1(self,event):
        if self.btnf1.GetValue():
            self.btnf1.SetLabel("Filter 1-ON")
        else:
            self.btnf1.SetLabel("Filter 1-OFF") 
        self.btnf1.Refresh()

    def f2(self,event):
        if self.btnf2.GetValue():
            self.btnf2.SetLabel("Filter 2-ON")
        else:
            self.btnf2.SetLabel("Filter 2-OFF")  
        self.btnf3.Refresh()

    def f3(self,event):
        if self.btnf3.GetValue():
            self.btnf3.SetLabel("Filter 3-ON")
        else:
            self.btnf3.SetLabel("Filter 3-OFF")    
        self.btnf3.Refresh()

    #Load Event Functions
    def l1(self,event):
        if self.btnload1.GetValue():
            self.btnload1.SetLabel("Load 1-ON")
        else:
            self.btnload1.SetLabel("Load 1-OFF") 
        self.btnload1.Refresh()

    def l2(self,event):
        if self.btnload2.GetValue():
            self.btnload2.SetLabel("Load 2-ON")
        else:
            self.btnload2.SetLabel("Load 2-OFF") 
        self.btnload2.Refresh()

    def l3(self,event):
        if self.btnload3.GetValue():
            self.btnload3.SetLabel("Load 3-ON")
        else:
            self.btnload3.SetLabel("Load 3-OFF")    
        self.btnload3.Refresh()      
    
    #Panel Controls
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
        self.SetTitle("Configuration Settings")
    
    def on_kids_mode(self, event):    #kids frame event
        self.panel3.Show()
        self.panel.Hide()
        self.panel2.Hide()
        self.sizer.Layout()
        self.SetTitle("Kids Mode")
        
    #Help Window
    def on_help(self, event):
        helpDlg = help(None)
        helpDlg.Show()
        
    #About Window    
    def on_about(self, event):
        aboutDlg = about(None)
        aboutDlg.Show()
        
    #def OnClose(self, event):
    #    dlg = wx.MessageDialog(self, 
    #        "Do you really want to close this application?",
    #        "Confirm Exit", wx.OK|wx.CANCEL|wx.ICON_QUESTION)
    #    result = dlg.ShowModal()
    #    dlg.Destroy()
    #    if result == wx.ID_OK:
    #        self.Destroy()
        
if __name__=='__main__':
    app = wx.App(False)#wx.PySimpleApp() 
    app.frame= main_frame() #, title='Block Diagram Mode'
    app.frame.Show()
    app.MainLoop()
