import wx
from wx.lib.buttons import GenBitmapTextButton
import os


class mf(wx.Frame):
    def __init__(self,parent, title):
        wx.Frame.__init__(self,None,title = 'AMPS Harmonics Distortion Project', size=(500,350))
        panel=wx.Panel(self)
        
        self.SetBackgroundColour('white')
        self.Centre()
        
        
        btnbm=wx.Button(panel,label='Block Mode', pos=(0,0), size=(80,30))
        btncm=wx.Button(panel,label='Configure', pos=(80,0), size=(80,30))
        btnkm=wx.Button(panel,label='Kids Mode', pos=(160,0), size=(80,30))
        
        self.Bind(wx.EVT_BUTTON, self.bm, btnbm)
        self.Bind(wx.EVT_BUTTON, self.cm, btncm)
        self.Bind(wx.EVT_BUTTON, self.km, btnkm)

        self.Bind(wx.EVT_CLOSE, self.closewindow)
        
    def bm(self,event):
        frame = sf()
        frame.Show()

    def cm(self,event):
        frame2 = tf()
        frame2.Show()

    def km(self,event):
        frame3 = ff()
        frame3.Show()

    def closewindow(self,event):
        self.Destroy()

##############################################################

class sf(wx.Frame):

    
    def __init__(self):
        wx.Frame.__init__(self,None, title = 'Block Diagram Mode', size=(500,400))
        panel = wx.Panel(self)
        panel.SetBackgroundColour('GRAY')

        
        btni1=wx.BitmapButton(panel, -1, wx.Bitmap('inverter_r.jpg'), style=wx.NO_BORDER, pos=(50,60))
        btni2=wx.BitmapButton(panel, -1, wx.Bitmap('inverter_r.jpg'), style=wx.NO_BORDER, pos=(50,140))

        btnr1=wx.BitmapButton(panel, -1, wx.Bitmap('relay.png'), style=wx.NO_BORDER, pos=(140,60))
        btnr2=wx.BitmapButton(panel, -1, wx.Bitmap('relay.png'), style=wx.NO_BORDER, pos=(140,120))
        btnr3=wx.BitmapButton(panel, -1, wx.Bitmap('relay.png'), style=wx.NO_BORDER, pos=(140, 180))


        #btnload1=wx.BitmapButton(panel, -1, wx.Bitmap('rsz_fan.png'), style=wx.NO_BORDER, pos=(320, 75))
        btnload2=wx.BitmapButton(panel, -1, wx.Bitmap('rsz_lb_off.jpg'), style=wx.NO_BORDER, pos=(320, 125))
        #btnload3=wx.BitmapButton(panel, -1, wx.Bitmap('rsz_led.png'), style=wx.NO_BORDER, pos=(320, 175))

        btnt=wx.Button(panel, -1, label='Time', pos=(350,250))
        btnf=wx.Button(panel, -1, label='Frequency', pos=(350,300))
        btnpb=wx.Button(panel, -1, label='Playback', pos=(400,100))
        

        self.labeli1= wx.StaticText(panel, label='1', size = (20,20), pos = (60, 40))
        self.labeli2= wx.StaticText(panel, label='2', size = (20,20), pos = (90,40))

        self.labelr1= wx.StaticText(panel, label='1', size = (10,20), pos = (170,40))
        self.labelr2= wx.StaticText(panel, label='2', size = (10,20), pos = (190,40))
        self.labelr3= wx.StaticText(panel, label='3', size = (10,20), pos = (210,40))
        
        self.labeli1.SetForegroundColour('green')
        self.labeli2.SetForegroundColour('green')
        self.labelr1.SetForegroundColour('green')
        self.labelr2.SetForegroundColour('green')
        self.labelr3.SetForegroundColour('green')
        
        self.Bind(wx.EVT_BUTTON, self.i1, btni1)
        self.Bind(wx.EVT_BUTTON, self.i2, btni2)
        self.Bind(wx.EVT_BUTTON, self.r1, btnr1)
        self.Bind(wx.EVT_BUTTON, self.r2, btnr2)
        self.Bind(wx.EVT_BUTTON, self.r3, btnr3)
        
        self.count=0
        self.count2=0
        self.countr=0
        self.countr2=0
        self.countr3=0
        
    def r1(self,event):
        self.countr += 1
        if self.countr == 1:
            self.labelr1.SetForegroundColour('red')
            
            
        elif self.countr == 2:
            self.labelr1.SetForegroundColour('green')
            self.countr = 0
            
        self.labelr1.Refresh()

    def r2(self,event):
        self.countr2 += 1
        if self.countr2 == 1:
            self.labelr2.SetForegroundColour('red')
            
            
        elif self.countr2 == 2:
            self.labelr2.SetForegroundColour('green')
            self.countr2 = 0
            
        self.labelr2.Refresh()

    def r3(self,event):
        self.countr3 += 1
        if self.countr3 == 1:
            self.labelr3.SetForegroundColour('red')
            
            
        elif self.countr3 == 2:
            self.labelr3.SetForegroundColour('green')
            self.countr3 = 0
            
        self.labelr3.Refresh()

    def i1(self,event):
        self.count += 1
        
        if self.count == 1:
            self.labeli1.SetForegroundColour('red')
            
            
        elif self.count == 2:
            self.labeli1.SetForegroundColour('green')
            self.count = 0
            
        self.labeli1.Refresh()
        

    def i2(self,event):
        self.count2 += 1
        if self.count2 == 1:
            self.labeli2.SetForegroundColour('red')
            
            
        elif self.count2 == 2:
            self.labeli2.SetForegroundColour('green')
            self.count2 = 0
            
        self.labeli2.Refresh()

    
        
        

   # if boli1 == False:
    #        self.labeli1.SetForegroundColour('green')
     #       self.Refresh()
    #else:
     #       self.labeli1.SetForegroundColour('red')
      #      self.Refresh()
     
    #if boli2 == False:
     #       self.labeli2.SetForegroundColour('green')
      #      self.Refresh()
    #else:
     #       labeli2.SetForegroundColour('red')
      #      self.Refresh()        

##############################################################
class tf(wx.Frame):

    def __init__(self):
        wx.Frame.__init__(self,None, title = 'Configuration Mode', size=(500,350))
        panel = wx.Panel(self)

#############################################################
class ff(wx.Frame):

    def __init__(self):
        wx.Frame.__init__(self,None, title = 'Kids Mode', size=(500,350))
        panel = wx.Panel(self)
        
        
        
if __name__=='__main__':
    app = wx.App(False)
    frame= mf(None, title='AMPS Harmonics Distortion Project')
    frame.Show()
    app.MainLoop()
