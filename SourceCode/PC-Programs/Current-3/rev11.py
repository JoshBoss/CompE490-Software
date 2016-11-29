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
from classes.SetScalingsDialog import SetScalingsDialog as scalingDialog
from classes.SystemSettingsDialog import SystemSettingsDialog as sysSettingsDlg

import thread
import time
import socket


########################################################################
#                           Global Socket and Lists                    #
########################################################################
s = socket.socket()
voltageArray = []
iMain = []

i1Array = []
i2Array = []
i3Array = []
vBattArray = []

ffti1 = []
ffti2 = []
ffti3 = []
fftiMain = []
fftVoltageArray = []

copy_voltageArray = []
copy_iMain = []
copy_i1Array = []
copy_i2Array = []
copy_i3Array = []
copy_vBattArray = []

PlottingGraphs = []
relayString = list('0000000')

#Max Load Currents
Load1MaxCurrent = 600
Load2MaxCurrent = 600
Load3MaxCurrent = 600

#System Settings
IP = '192.168.42.1'
DRR = 0.55
STO = 0.35
########################################################################
########################################################################

    
class main_frame(wx.Frame): #Main frame

    def __init__(self): #inital values
        on_top = wx.DEFAULT_FRAME_STYLE | wx.STAY_ON_TOP
        wx.Frame.__init__(self,None, title = 'SDG&E AMPS', size=(1100,810))#, style=on_top) 		#initialize frame
        self.Centre()   #center frame

        self.init_top = 0
        self.init_bottom = 0
        self.paused = False
        self.fourier = False
	self.choice = '4' 

        self.create_menu()
        self.InitUI()

        self.redraw_timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.on_redraw_timer, self.redraw_timer)
        self.redraw_timer.Start(550)

    def create_menu(self):
        menubar = wx.MenuBar()  #init menu bar
        mode_menu = wx.Menu()    #mode
        settings_menu = wx.Menu()   #graph settings
        help_menu = wx.Menu()
        menubar.Append(mode_menu, '&Mode')   #mode under menu
        menubar.Append(settings_menu, '&Settings')
        menubar.Append(help_menu, '&Help')
        m_main_mode = mode_menu.Append(wx.ID_ANY, 'Main Mode')
        m_config_mode = mode_menu.Append(wx.ID_ANY, 'Configuration Settings') #Configuration and kids mode subsections of mode
	m_scalingSettings = settings_menu.Append(wx.ID_ANY, 'Scaling Settings')
	m_systemSettings = settings_menu.Append(wx.ID_ANY, 'System Settings')
        m_kids_mode = mode_menu.Append(wx.ID_ANY, 'Kids Mode')
        #g_save = settings_menu.Append(wx.ID_ANY, 'Save Data')
        h_about = help_menu.Append(wx.ID_ANY, 'About')
        h_help = help_menu.Append(wx.ID_ANY, 'User Manual')
        
        self.SetMenuBar(menubar)    #function here      
        self.Bind(wx.EVT_MENU, self.on_main_mode, m_main_mode)
        self.Bind(wx.EVT_MENU, self.on_config_mode, m_config_mode)   #binding event to definition
        self.Bind(wx.EVT_MENU, self.on_kids_mode, m_kids_mode)   #...
        #self.Bind(wx.EVT_MENU, self.on_save_data, g_save)
        self.Bind(wx.EVT_MENU, self.on_about, h_about)
        self.Bind(wx.EVT_MENU, self.on_help, h_help)
	self.Bind(wx.EVT_MENU, self.on_scaling, m_scalingSettings)
	self.Bind(wx.EVT_MENU, self.on_sysSettings, m_systemSettings)

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
        self.labeliv= wx.StaticText(self.panel, label='0.00 V', size = (50,20), style=wx.ALIGN_CENTRE) #inverter voltage value label
        self.labelic= wx.StaticText(self.panel, label='0.00 mA', size = (50,20), style=wx.ALIGN_CENTRE) #inverter current ...
        self.labeliv.SetBackgroundColour('white')    #set background color to white
        self.labelic.SetBackgroundColour('white')
        vbtn.Add(self.btni1, flag=wx.BOTTOM, border = 20)    #add inv 1 to vertical sizer, pushes next button down 20 pixels
        vbtn.Add(self.btni2, flag=wx.BOTTOM, border = 5) #goes beneath it
        hlabeli = wx.BoxSizer(wx.HORIZONTAL) #horizontal sizer for put labels under inv buttons (one by the other)
        hlabeli.Add(self.labeliv, flag = wx.RIGHT, border=15)    #add inv voltage label to sizer
        hlabeli.Add(self.labelic)    #add current...
        vbtn.Add(hlabeli)   #add horizontal sizer to row 2 column 1 sizer
        hvtn.Add(vbtn, flag=wx.LEFT, border=30) #add column 1 to row 2
        
        vbtnf = wx.BoxSizer(wx.VERTICAL)    #filter buttons vertical sizer (row 2 column 2)
        self.btnf1=wx.ToggleButton(self.panel, -1, label=('Filter 1 - OFF'))    #intialize filter buttons
        self.btnf2=wx.ToggleButton(self.panel, -1, label=('Filter 2 - OFF'))
        self.btnf3=wx.ToggleButton(self.panel, -1, label=('Filter 3 - OFF'))
        #self.labelfv= wx.StaticText(self.panel, label='0.00V', size = (50,20),  style=wx.ALIGN_CENTRE)    #voltage value label
        #self.labelfc= wx.StaticText(self.panel, label='0.00A', size = (50,20),  style=wx.ALIGN_CENTRE)    #current...
        #self.labelfv.SetBackgroundColour('white')    #set bg color to white
        #self.labelfc.SetBackgroundColour('white')
        vbtnf.Add(self.btnf1, flag = wx.BOTTOM, border=5)    #add filter button to vertical sizer, pushes down 5 pixels
        vbtnf.Add(self.btnf2, flag = wx.BOTTOM, border=5)
        vbtnf.Add(self.btnf3, flag = wx.BOTTOM, border=5)
        hlabelf = wx.BoxSizer(wx.HORIZONTAL)    #horizontal sizer for filter voltage and current labels
        #hlabelf.Add(self.labelfv, flag = wx.RIGHT, border =2)    #add filter values to sizer
        #hlabelf.Add(self.labelfc)
        vbtnf.Add(hlabelf)  #horizontal sizer goes beneath virtical one (row 3 column 2)
        hvtn.Add(vbtnf, flag=wx.LEFT, border=40)    #add it to column 2

        vbtnl = wx.BoxSizer(wx.VERTICAL)    #vertical sizer for load buttons (row 2 column 3)
        self.btnload1=wx.ToggleButton(self.panel, -1, label=('Load 1 - OFF'))   #initialize load buttons
        self.btnload2=wx.ToggleButton(self.panel, -1, label=('Load 2 - OFF'))
        self.btnload3=wx.ToggleButton(self.panel, -1, label=('Load 3 - OFF')) 
        vbtnl.Add(self.btnload1, flag = wx.TOP, border=8) #add buttons to vertical sizer
        vbtnl.Add(self.btnload2, flag = wx.TOP, border=23)
        vbtnl.Add(self.btnload3, flag = wx.TOP, border=23)
        hvtn.Add(vbtnl, flag=wx.LEFT, border=40)    #add vertical sizer to row 2

        vloadval = wx.BoxSizer(wx.VERTICAL) #load value vertical sizer
        #self.labelload1v= wx.StaticText(self.panel, label='0.00V', size = (50,20), style=wx.ALIGN_CENTRE) #init current and voltage labels for all 3 loads
        self.labelload1c= wx.StaticText(self.panel, label='0.00 mA', size = (50,20), style=wx.ALIGN_CENTRE)
        #self.labelload2v= wx.StaticText(self.panel, label='0.00V', size = (50,20), style=wx.ALIGN_CENTRE)
        self.labelload2c= wx.StaticText(self.panel, label='0.00 mA', size = (50,20), style=wx.ALIGN_CENTRE)
        #self.labelload3v= wx.StaticText(self.panel, label='0.00V', size = (50,20), style=wx.ALIGN_CENTRE)
        self.labelload3c= wx.StaticText(self.panel, label='0.00 mA', size = (50,20), style=wx.ALIGN_CENTRE)
        #self.labelload1v.SetBackgroundColour('white')    #set bg color to white
        self.labelload1c.SetBackgroundColour('white')
        #self.labelload2v.SetBackgroundColour('white')
        self.labelload2c.SetBackgroundColour('white')
        #self.labelload3v.SetBackgroundColour('white')
        self.labelload3c.SetBackgroundColour('white')
        #vloadval.Add(self.labelload1v)   #add load value labels to vertical sizer
        vloadval.Add(self.labelload1c, flag=wx.TOP, border=23)
        #vloadval.Add(self.labelload2v, flag=wx.TOP, border=10)
        vloadval.Add(self.labelload2c, flag=wx.TOP, border=23)
        #vloadval.Add(self.labelload3v, flag=wx.TOP, border=10)
        vloadval.Add(self.labelload3c, flag=wx.TOP, border=25)

        hvtn.Add(vloadval, flag=wx.LEFT, border=5)  #add virtical sizer to row 2
        #graph_sizer = wx.BoxSizer(wx.HORIZONTAL)
        #self.radio_2graphs = wx.RadioButton(self.panel, -1, label='2 G', style=wx.RB_GROUP,  size=(20,20)) #style=wx.RB_GROUP,
        #self.radio_4graphs = wx.RadioButton(self.panel, -1, label='4 G', style=wx.RB_GROUP,  size=(20,20)) #
        #graph_sizer.Add(self.radio_2graphs, flag = wx.ALL, border = 5)
        #graph_sizer.Add(self.radio_4graphs, flag = wx.ALL, border = 5)
	#lblList = ['2', '4']
	#self.rbox = wx.RadioBox(self.panel, label = 'Number of Graphs', choices = lblList, majorDimension = 1, style = wx.RA_SPECIFY_ROWS) 
        #self.rbox.Bind(wx.EVT_RADIOBOX,self.onRadioBox)

        vlabelrt = wx.BoxSizer(wx.VERTICAL) #vertical sizer for system, wifi and time labels (delete to have it at far right end of the window
	self.connectButton = wx.Button(self.panel, -1, label='Connect')
        self.labelsys= wx.StaticText(self.panel, label='Disconnected', size = (100,20), style=wx.ALIGN_CENTRE)  #sys on/off label
        #self.labelwifi= wx.StaticText(self.panel, label='Disconnected', size = (100,20), style=wx.ALIGN_CENTRE)  #wifi connected/disconnected label
        #self.labeltime= wx.StaticText(self.panel, label='00:00 xx/xx/xx', size = (100,20), style=wx.ALIGN_CENTRE) #uptime label
        self.labelsys.SetBackgroundColour('green')   #set bg colors
        #self.labelwifi.SetBackgroundColour('green')
        #self.labeltime.SetBackgroundColour('white')
	vlabelrt.Add(self.connectButton, flag = wx.TOP, border=25)
        vlabelrt.Add(self.labelsys, flag = wx.TOP, border=25) #add to vertical sizer
	#vlabelrt.Add(graph_sizer, flag = wx.TOP, border=15)
	#vlabelrt.Add(self.rbox, flag = wx.TOP, border=15)
        #self.init_plot()
	#self.canvas = FigCanvas(self.panel, -1, self.fig)
	
	#Button binding for Connect button
	self.connectButton.Bind(wx.EVT_BUTTON, self.connectButtonEvent)
	
        hvtn.Add(vlabelrt, flag=wx.LEFT, border=20) #add vertical sizer to row 2
        
        
        self.pause_button = wx.Button(self.panel, -1, "pause")
        self.Bind(wx.EVT_BUTTON, self.on_pause_button, self.pause_button)
        self.Bind(wx.EVT_UPDATE_UI, self.on_update_pause_button, self.pause_button)
        
        #self.fft_button = wx.Button(self.panel, -1 , "FFT-OFF")
        #self.Bind(wx.EVT_BUTTON, self.on_fft_button, self.fft_button)
        #self.Bind(wx.EVT_UPDATE_UI, self.on_update_fft_button, self.fft_button)
        
	self.saveButton = wx.Button(self.panel, -1, "Save Data")
	self.saveButton.Bind(wx.EVT_BUTTON, self.saveFunction)
	self.loadButton = wx.Button(self.panel, -1, "Load Data")
	self.loadButton.Bind(wx.EVT_BUTTON, self.loadFunction)
        #box = wx.StaticBox(self.panel, -1, "Number of graphs")

  
        settings_vertical = wx.BoxSizer(wx.VERTICAL)
        settings_vertical.Add(self.pause_button, flag=wx.TOP, border=20)
        #settings_vertical.Add(self.fft_button, flag=wx.TOP, border=10)
	settings_vertical.Add(self.saveButton, flag=wx.TOP, border=10)
	settings_vertical.Add(self.loadButton, flag=wx.TOP, border=10)
        #settings_vertical.Add(graph_sizer, flag=wx.TOP, border=10)
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
	

    def saveFunction(self, e):
	global copy_voltageArray
	global copy_iMain
	global copy_i1Array
	global copy_i2Array
	global copy_i3Array
	global copy_vBattArray

	global voltageArray
	global iMain
	global i1Array
	global i2Array
	global i3Array
	global vBattArray

	copy_voltageArray = voltageArray
	copy_iMain = iMain
	copy_i1Array = i1Array
	copy_i2Array = i2Array
	copy_i3Array = i3Array
	copy_vBattArray = vBattArray

	saveDialog = wx.FileDialog(self, "Save data", os.getcwd(), \
				   "", "*.txt", wx.SAVE | wx.OVERWRITE_PROMPT);
	if saveDialog.ShowModal() == wx.ID_OK:
		print "ID OK"
		#Open a file and write to it
		writingFile = open(saveDialog.GetPath(), 'w')
		writingFile.write('v\n')
		for entry in copy_voltageArray:
			writingFile.write(str(entry) + '\n')
		writingFile.write('i\n')
		for entry in copy_iMain:
			writingFile.write(str(entry) + '\n')
		writingFile.write('i1\n')
		for entry in copy_i1Array:
			writingFile.write(str(entry) + '\n')
		writingFile.write('i2\n')
		for entry in copy_i2Array:
			writingFile.write(str(entry) + '\n')
		writingFile.write('i3\n')
		for entry in copy_i3Array:
			writingFile.write(str(entry) + '\n')
		writingFile.write('vbatt\n')
		for entry in copy_vBattArray:
			writingFile.write(str(entry) + '\n')
		writingFile.close()
		print "File Saved."

    def loadFunction(self, e):
	loadDialog = wx.FileDialog(self, "Load data", os.getcwd(), \
				   "", "*.txt", wx.OPEN)
	if loadDialog.ShowModal() == wx.ID_OK:
		readFilePath = loadDialog.GetPath()
		parseFile2(readFilePath)


    def init_plot(self):
        #self.fig = Figure(tight_layout = True)#,subplotParams(wspace=0, hspace=0)
	self.fig = Figure(tight_layout = True)#,subplotParams(wspace=0, hspace=0)
	#self.fig = Figure(tight_layout = True)#,subplotParams(wspace=0, hspace=0)
	self.axes1 = self.fig.add_subplot(221)
	self.axes2 = self.fig.add_subplot(222)
	self.axes3 = self.fig.add_subplot(223)
	self.axes4 = self.fig.add_subplot(224)

	self.axes1.set_title('Current', size=10)
    	self.axes2.set_title('FFT Loads', size=10)
	self.axes3.set_title('Main Voltage', size=10)
	self.axes4.set_title('FFT Voltage', size=10)

	pylab.setp(self.axes1.get_xticklabels(), fontsize=4)
	pylab.setp(self.axes1.get_yticklabels(), fontsize=4)
	pylab.setp(self.axes2.get_xticklabels(), fontsize=4)
	pylab.setp(self.axes2.get_yticklabels(), fontsize=4)
	pylab.setp(self.axes3.get_xticklabels(), fontsize=4)
	pylab.setp(self.axes3.get_yticklabels(), fontsize=4)
	pylab.setp(self.axes4.get_xticklabels(), fontsize=4)
	pylab.setp(self.axes4.get_yticklabels(), fontsize=4)
            
    def connectButtonEvent(self, e):
	try:
		hostString = connectToPi()
		if(hostString != "ERR"):
			self.connectButton.SetLabel("Disconnect")
			#self.labelwifi.SetLabel('Connected to: ' + hostString)
			#If connection is successful, we change the label accordingly
			#We can also start the timer?
			#Start the receiver thread, that will continously ping the Pi for data
			thread.start_new_thread(receiveFile, ()) #Start the thread
			#First arg is the function to call, the second arg is a tuple containing
			#any arguments passed to the function. () is an empty tuple, no args.
			self.labelsys.SetLabel("Connected:\n" + hostString)
			self.loadButton.Disable()
		else:
			self.connectButton.SetLabel("Connect")
			self.labelsys.SetLabel('Error connecting.\nRetry.')
			self.loadButton.Enable()
	except:
		self.connectButton.SetLabel("Connect")
		self.labelsys.SetLabel('Error connecting.\nRetry.')
		self.loadButton.Enable()


    def draw_plot(self):
	    global voltageArray
	    global iMain
	    global i1Array
	    global i2Array
	    global i3Array
	    global ffti1
	    global ffti2
	    global ffti3
	    global fftVoltageArray
	    fftXAxes = range(0, 601, 60)
	    self.axes1.clear()
    	    self.axes2.clear()
	    self.axes3.clear()
	    self.axes4.clear()

            
	    self.axes1.set_title('Current')
    	    self.axes2.set_title('FFT Loads')
	    self.axes3.set_title('Main Voltage')
	    self.axes4.set_title('FFT Voltage')
	    self.axes1.set_ylabel("milliamps (mA)")
	    self.axes2.set_ylabel("Decibels (dB)")
	    self.axes3.set_ylabel("Volts (V)")
	    self.axes4.set_ylabel("Decibels (dB)")
	    self.axes2.set_xlabel("Hertz (Hz)")
	    self.axes4.set_xlabel("Hertz (Hz)")
	
	    #self.axes2.set_xticklabels(range(0, 601, 60))

	    if self.top_graph.on_grid():
	        self.axes1.grid(True, color='black')
		self.axes2.grid(True, color='black')
	    else:
		self.axes1.grid(False)
		self.axes2.grid(False)

	    if self.bottom_graph.on_grid():
	        self.axes3.grid(True, color='black')
		self.axes4.grid(True, color='black')
	    else:
	        self.axes3.grid(False)
		self.axes4.grid(False)

	    if 'i1' in PlottingGraphs:
	        self.axes1.plot(i1Array, color='blue') #Redraw the plot
		try:
			self.axes2.stem(fftXAxes, np.insert(ffti1[3:60:6], 0, 0))
			#self.axes2.setp(markerline, 'markerfacecolor', 'red')
			#self.axes2.setp(markerlines, color='red')
			for index in range(0, len(np.insert(fftVoltageArray[3:60:6], 0, 0))):
				if index == 0:
					continue
				self.axes2.annotate(str(int(np.insert(ffti1[3:60:6], 0, 0)[index])), (fftXAxes[index], np.insert(ffti1[3:60:6], 0, 0)[index]),\
						    (fftXAxes[index]-15, np.insert(ffti1[3:60:6], 0, 0)[index]+3), bbox = dict(boxstyle = 'round,pad=0.2', fc = 'blue', alpha = 0.5))
			
		except:
			self.axes2.stem(ffti1)
		try:
			self.labelload1c.SetLabel(str(round(max(i1Array), 2)) + " mA ")
		except:
			self.labelload1c.SetLabel("0.00 mA")

	    if 'i2' in PlottingGraphs:
		self.axes1.plot(i2Array, color='green') #Redraw the plot
		try:
			self.axes2.stem(fftXAxes, np.insert(ffti2[3:60:6],0,0))
			for index in range(0, len(np.insert(fftVoltageArray[3:60:6], 0, 0))):
				if index == 0:
					continue
				self.axes2.annotate(str(int(np.insert(ffti2[3:60:6], 0, 0)[index])), (fftXAxes[index], np.insert(ffti2[3:60:6], 0, 0)[index]),\
						    (fftXAxes[index]-15, np.insert(ffti2[3:60:6], 0, 0)[index]+3), bbox = dict(boxstyle = 'round,pad=0.2', fc = 'green', alpha = 0.5))
		except:
			self.axes2.stem(ffti2)
		try:
			self.labelload2c.SetLabel(str(round(max(i2Array), 2)) + " mA ")
		except:
			self.labelload2c.SetLabel("0.00 mA")
		
	    if 'i3' in PlottingGraphs:
		self.axes1.plot(i3Array, color='orange') #Redraw the plot
		try:
			self.axes2.stem(fftXAxes, np.insert(ffti3[3:60:6], 0, 0), color='orange')
			for index in range(0, len(np.insert(fftVoltageArray[3:60:6], 0, 0))):
				if index == 0:
					continue
				self.axes2.annotate(str(int(np.insert(ffti3[3:60:6], 0, 0)[index])), (fftXAxes[index], np.insert(ffti3[3:60:6], 0, 0)[index]),\
						    (fftXAxes[index]-15, np.insert(ffti3[3:60:6], 0, 0)[index]+3), bbox = dict(boxstyle = 'round,pad=0.2', fc = 'orange', alpha = 0.5))
		except:
			self.axes2.stem(ffti3)
		try:
			self.labelload3c.SetLabel(str(round(max(i3Array), 2)) + " mA ")
		except:
			self.labelload3c.SetLabel("0.00 mA")
		
	    self.axes3.plot(voltageArray)
	    try:
	    	self.axes4.stem(fftXAxes, np.insert(fftVoltageArray[3:60:6], 0, 0))
		for index in range(0, len(np.insert(fftVoltageArray[3:60:6], 0, 0))):
			if index == 0:
				continue
			self.axes4.annotate(str(int(np.insert(fftVoltageArray[3:60:6], 0, 0)[index])), (fftXAxes[index], np.insert(fftVoltageArray[3:60:6], 0, 0)[index]),\
					    (fftXAxes[index]-15, np.insert(fftVoltageArray[3:60:6], 0, 0)[index]+3), bbox = dict(boxstyle = 'round,pad=0.2', fc = 'red', alpha = 0.5))
	    except Exception as e:
		print str(e)
		self.axes4.clear()
	    try:
	    	self.labeliv.SetLabel(str(round(max(voltageArray), 2)) + " V")
	    except:
		self.labeliv.SetLabel("0.00 V")


	    self.axes1.set_ylim([getLowerLim2(self.top_graph.update_value()), getUpperLim2(self.top_graph.update_value())])
	    self.axes3.set_ylim([getLowerLim(self.bottom_graph.update_value()), getUpperLim(self.bottom_graph.update_value())])
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
          self.draw_plot()
    

    def i1(self,event):
	#Inverter 1 is the default mode, set MSB of relay string to zero
	relayString[0] = '0'

    def i2(self,event):
	#Inverter 2 is the modified sine wave inverter, set MSB of relay string to one
	relayString[0] = '1'
        
    def f1(self,event):
	#Filter 1 toggle
	if(relayString[1] == '1'):
		relayString[1] = '0'
		self.btnf1.SetLabel("Filter 1 - OFF")
		self.btnf1.Refresh()
	else:
		relayString[1] = '1'
		self.btnf1.SetLabel("Filter 1 - ON")
		self.btnf1.Refresh()

    def f2(self,event):
	#Filter 2 toggle
	if(relayString[2] == '1'):
		relayString[2] = '0'
		self.btnf2.SetLabel("Filter 2 - OFF")
		self.btnf2.Refresh()
	else:
		relayString[2] = '1'
		self.btnf2.SetLabel("Filter 2 - ON")
		self.btnf2.Refresh()

    def f3(self,event):
	#Filter 3 toggle
	if(relayString[3] == '1'):
		relayString[3] = '0'
		self.btnf3.SetLabel("Filter 3 - OFF")
		self.btnf3.Refresh()
	else:
		relayString[3] = '1'
		self.btnf3.SetLabel("Filter 3 - ON")
		self.btnf3.Refresh()

    def l1(self,event):
	global PlottingGraphs
	global i1Array
	if 'i1' in PlottingGraphs:
		PlottingGraphs.remove('i1')
	else:
		PlottingGraphs.append('i1')

	#Load 1 toggle
	if(relayString[4] == '1'):
		relayString[4] = '0'
		self.btnload1.SetLabel("Load 1 - OFF")
		self.labelload1c.SetLabel("0.00 mA")
		self.btnload1.Refresh()
	else:
		relayString[4] = '1'
		self.btnload1.SetLabel("Load 1 - ON")
		#self.labelload1c.SetLabel(str(round(max(i1Array), 2)) + " A ")
		self.btnload1.Refresh()



    def l2(self,event):
        global PlottingGraphs
	if 'i2' in PlottingGraphs:
		PlottingGraphs.remove('i2')
	else:
		PlottingGraphs.append('i2')

	#Load 2 toggle
	if(relayString[5] == '1'):
		relayString[5] = '0'
		self.btnload2.SetLabel("Load 2 - OFF")
		self.labelload2c.SetLabel("0.00 mA")
		self.btnload2.Refresh()
	else:
		relayString[5] = '1'
		self.btnload2.SetLabel("Load 2 - ON")
		self.btnload2.Refresh()

    def l3(self,event):
        global PlottingGraphs
	if 'i3' in PlottingGraphs:
		PlottingGraphs.remove('i3')
	else:
		PlottingGraphs.append('i3')

	#Load 3 toggle
	if(relayString[6] == '1'):
		relayString[6] = '0'
		self.btnload3.SetLabel("Load 3 - OFF")
		self.labelload3c.SetLabel("0.00 mA")
		self.btnload3.Refresh()  
	else:
		relayString[6] = '1'
		self.btnload3.SetLabel("Load 3 - ON")
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
    
    def on_scaling(self, event):
	global Load1MaxCurrent
	global Load2MaxCurrent
	global Load3MaxCurrent
	args = [Load1MaxCurrent, Load2MaxCurrent, Load3MaxCurrent]
	scalingDlg = scalingDialog(None, title='Adjust Max Load Currents')

	result = scalingDlg.ShowModal()
	if result == wx.ID_OK:
		Load1MaxCurrent = int(scalingDlg.Load1Max)
		Load2MaxCurrent = int(scalingDlg.Load2Max)
		Load3MaxCurrent = int(scalingDlg.Load3Max)
	scalingDlg.Destroy()
    
    def on_sysSettings(self, event):
	global DRR
	global STO
	global IP
	settingsDlg = sysSettingsDlg(None, title='System Settings')
	
	result = settingsDlg.ShowModal()
	if(result == wx.ID_OK):
		DRR = float(str(settingsDlg.DRR))
		STO = float(str(settingsDlg.STO))
		IP = settingsDlg.IP
	settingsDlg.Destroy()

    #def OnClose(self, event):
    #    dlg = wx.MessageDialog(self, 
    #        "Do you really want to close this application?",
    #        "Confirm Exit", wx.OK|wx.CANCEL|wx.ICON_QUESTION)
    #    result = dlg.ShowModal()
    #    dlg.Destroy()
    #    if result == wx.ID_OK:
    #        self.Destroy()

#################################################################################
#                                Function to connect to Pi                      #
#################################################################################
def connectToPi():
	global IP
	host = IP
	port = 8890
	global s
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.settimeout(0.15)
		s.connect((host, port))
		s.settimeout(None)
		return host
	except:
		return "ERR"
#################################################################################
#################################################################################

#################################################################################
#                 Function to request data from Pi and parse it                 #
#                Launched as a thread to avoid blocking the GUI                 #
#################################################################################
def receiveFile():
	global s
	global DRR
	global STO
	while True:
		time.sleep(DRR)
		s.settimeout(STO)
		s.sendall("GETDATA")
		#print(''.join(relayString))
		s.sendall(''.join(relayString))
		fileString = "localFile.txt"
		textFile = open(fileString, 'wb')
		s.sendall("OK")
		#startTime = time.time()
		try:
			serverMessage = s.recv(4096)
		except:
			print "Post-OK timeout. Continuing..."
			continue
		while serverMessage:
			textFile.write(serverMessage)
	 		try:
				serverMessage = s.recv(4096)
			except:
					break
		textFile.close()
		s.settimeout(None)
		parseFile()
		zerocross()
		ScaleArrays()
		PerformFFT()
#################################################################################
#################################################################################


#################################################################################
#                 Function to Parse the File into the local arrays              #
#               Called from within a thread to avoid blocking the GUI           #
#################################################################################
def parseFile():
	textFile = open("localFile.txt", 'r')
	currentFile = 'v'
	#Need to clear the lists
	global voltageArray
	global iMain
	global i1Array
	global i2Array
	global i3Array
	global vBattArray

	voltageArray = []
	iMain = []

	i1Array = []
	i2Array = []
	i3Array = []
	vBattArray = []

	for rawLine in textFile:
		line = rawLine.rstrip('\n')
		if((line == 'v') or (line == 'i') or (line == 'i1') or (line == 'i2') or (line == 'i3') or (line == 'vbatt')):
			#If the current line is not a value but an array identifier, switch the currentFile var to it
			currentFile = line
		else:
			#Otherwise, the current line is a value and we add it to the current file
			if currentFile == 'v':
				voltageArray.append(float(line))
			elif currentFile == 'i':
				iMain.append(float(line))
			elif currentFile == 'i1':
				i1Array.append(float(line))
			elif currentFile == 'i2':
				i2Array.append(float(line))
			elif currentFile == 'i3':
				i3Array.append(float(line))
			elif currentFile == 'vbatt':
				vBattArray.append(float(line))
#################################################################################
#################################################################################


#################################################################################
#                 Function to Parse the File into the local arrays              #
#                     Called when loading previously saved data                 #
#################################################################################
def parseFile2(readFile):
	textFile = open(readFile, 'r')
	currentFile = 'v'
	#Need to clear the lists
	global voltageArray
	global iMain
	global i1Array
	global i2Array
	global i3Array
	global vBattArray

	voltageArray = []
	iMain = []

	i1Array = []
	i2Array = []
	i3Array = []
	vBattArray = []

	for rawLine in textFile:
		line = rawLine.rstrip('\n')
		if((line == 'v') or (line == 'i') or (line == 'i1') or (line == 'i2') or (line == 'i3') or (line == 'vbatt')):
			#If the current line is not a value but an array identifier, switch the currentFile var to it
			currentFile = line
		else:
			#Otherwise, the current line is a value and we add it to the current file
			if currentFile == 'v':
				voltageArray.append(float(line))
			elif currentFile == 'i':
				iMain.append(float(line))
			elif currentFile == 'i1':
				i1Array.append(float(line))
			elif currentFile == 'i2':
				i2Array.append(float(line))
			elif currentFile == 'i3':
				i3Array.append(float(line))
			elif currentFile == 'vbatt':
				vBattArray.append(float(line))
	#After parsing, perform FFT
	PerformFFT()
#################################################################################
#################################################################################

#################################################################################
#                               Perform FFT to data                             #
#################################################################################
def PerformFFT():
	global voltageAray
	global iMain
	global i1Array
	global i2Array
	global i3Array
	global fftVoltageArray
	global ffti1
	global ffti2
	global ffti3

	fftiMain = np.fft.fft(iMain)
	ffti1 = 20*np.log10(abs(np.fft.fftshift(np.fft.fft(i1Array))))[100:200]
	ffti2 = 20*np.log10(abs(np.fft.fftshift(np.fft.fft(i2Array))))[100:200]
	ffti3 = 20*np.log10(abs(np.fft.fftshift(np.fft.fft(i3Array))))[100:200]
	fftVoltageArray = 20*np.log10(abs(np.fft.fftshift(np.fft.fft(voltageArray))))[100:200]
#################################################################################
#################################################################################

#################################################################################
#                            Perform scaling to the data                        #
#################################################################################	
def ScaleArrays():
	global voltageArray
	global iMain
	global i1Array
	global i2Array
	global i3Array

	global Load1MaxCurrent
	global Load2MaxCurrent
	global Load3MaxCurrent

	voltageArray[:] = [(x-512) * (0.3326810176126547) for x in voltageArray]
	iMain[:] = [(x-512) * (0.3326810176126547) for x in iMain]
	i1Array[:] = [((3.3*x) - 1599)/1.555092 for x in i1Array]
	#i1Array[:] = [((x-512) / (1023.0/(2*Load1MaxCurrent)))*1.075 for x in i1Array]
	i2Array[:] = [(x-512) / (1023.0/(2*Load2MaxCurrent)) for x in i2Array]
	i3Array[:] = [(x-512) / (1023.0/(2*Load3MaxCurrent)) for x in i3Array]
#################################################################################
#################################################################################


#################################################################################
#                            Find the Zero Crossing                             #
#################################################################################
def zerocross(): 
        global voltageArray
	global iMain
	global i1Array
	global i2Array
	global i3Array
	global vBattArray
	lowPoint = 0
	tempArray = []
	startIndex = 0
	for index in range(0, 267):
		if voltageArray[index] < 200 and lowPoint == 0:
			lowPoint = 1
		elif lowPoint == 1 and voltageArray[index] > 500:
			startIndex = index
			break
	voltageArray = voltageArray[startIndex:startIndex + 199]
	iMain = iMain[startIndex:startIndex + 199]
	i1Array = i1Array[startIndex:startIndex + 199]
	i2Array = i2Array[startIndex:startIndex + 199]
	i3Array = i3Array[startIndex:startIndex + 199]
	vBattArray = vBattArray[startIndex:startIndex + 199]
#################################################################################
#################################################################################

#################################################################################
#     Functions to Return the y axis limit based on current slider value        #
#################################################################################
def getUpperLim(num):
	return (200 - num)
def getLowerLim(num):
	return -1*(200 - num)
#################################################################################
#################################################################################

#################################################################################
#     Functions to Return the y axis limit based on current slider value        #
#################################################################################
def getUpperLim2(num):
	if(num < 42):
		return 1000
	elif(num >= 42 and num < 84):
		return 500
	elif(num >= 84 and num < 125):
		return 250
	else:
		return 125
def getLowerLim2(num):
	if(num < 42):
		return -1000
	elif(num >= 42 and num < 84):
		return -500
	elif(num >= 84 and num < 125):
		return -250
	else:
		return -125
#################################################################################
#################################################################################
        
if __name__=='__main__':
    app = wx.App(False)#wx.PySimpleApp() 
    app.frame= main_frame() #, title='Block Diagram Mode'
    app.frame.Show()
    app.MainLoop()
