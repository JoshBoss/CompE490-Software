import wx
from numpy import arange, sin, pi
import matplotlib
matplotlib.use('WXAgg')

from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.figure import Figure


class mf(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, None, title='AMPS Harmonics Distortion Project', size=(500, 350))
        panel = wx.Panel(self)

        self.SetBackgroundColour('white')
        self.Centre()

        btnbm = wx.Button(panel, label='Block Mode', pos=(0, 0), size=(80, 30))
        btncm = wx.Button(panel, label='Configure', pos=(80, 0), size=(80, 30))
        btnkm = wx.Button(panel, label='Kids Mode', pos=(160, 0), size=(80, 30))

        self.Bind(wx.EVT_BUTTON, self.bm, btnbm)
        self.Bind(wx.EVT_BUTTON, self.cm, btncm)
        self.Bind(wx.EVT_BUTTON, self.km, btnkm)

        self.Bind(wx.EVT_CLOSE, self.closewindow)

    def bm(self, event):
        frame = sf()
        frame.Show()

    def cm(self, event):
        frame2 = tf()
        frame2.Show()

    def km(self, event):
        frame3 = ff()
        frame3.Show()

    def closewindow(self, event):
        self.Destroy()


##############################################################

class CanvasPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self,parent)
        self.figure = Figure()
        self.axes = self.figure.add_subplot(212)
        self.canvas = FigureCanvas(self, -1, self.figure)
        #self.sizer = wx.BoxSizer(wx.VERTICAL)
        #self.sizer.Add(self.canvas, 1, wx.LEFT | wx.TOP | wx.GROW)
        #self.SetSizer(self.sizer)
        self.Fit()

    def draw(self):
        t = arange(0.0, 3.0, 0.01)
        s = sin(2 * pi * t)
        self.axes.plot(t, s)


class sf(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title='Block Diagram Mode', size=(670, 610))
        panel = wx.Panel(self)
        panel.SetBackgroundColour('GRAY')

        btni1 = wx.ToggleButton(panel, -1, label=('Inverter 1'), pos=(50, 20))
        btni2 = wx.ToggleButton(panel, -1, label=('Inverter 2'), pos=(50, 70))

        btnf1 = wx.ToggleButton(panel, -1, label=('Filter 1'), pos=(180, 20))
        btnf2 = wx.ToggleButton(panel, -1, label=('Filter 2'), pos=(180, 50))
        btnf3 = wx.ToggleButton(panel, -1, label=('Filter 3'), pos=(180, 80))

        btnload1 = wx.ToggleButton(panel, -1, label=('Load 1'), pos=(320, 20))
        btnload2 = wx.ToggleButton(panel, -1, label=('Load 2'), pos=(320, 80))
        btnload3 = wx.ToggleButton(panel, -1, label=('Load 3'), pos=(320, 140))

        btnct1 = wx.Button(panel, -1, label='Time', pos=(550, 220))
        btncf1 = wx.Button(panel, -1, label='Frequency', pos=(550, 270))
        btnct2 = wx.Button(panel, -1, label='Time', pos=(550, 390))
        btncf2 = wx.Button(panel, -1, label='Frequency', pos=(550, 440))
        btnpb = wx.Button(panel, -1, label='Playback', size=(100, 20), pos=(550, 95))

        #fr = wx.Frame(None, title='test')
        panel = CanvasPanel(panel)
        panel.draw()
        #panel.Show()

        self.labelcurrent = wx.StaticText(panel, label='Current', size=(100, 20), pos=(0, 200))
        self.labelvoltage = wx.StaticText(panel, label='Voltage', size=(100, 20), pos=(0, 370))

        self.labeli1 = wx.StaticText(panel, label='1', size=(20, 20), pos=(70, 0), style=wx.ALIGN_CENTRE)
        self.labeli2 = wx.StaticText(panel, label='2', size=(20, 20), pos=(95, 0), style=wx.ALIGN_CENTRE)
        self.labeli1.SetBackgroundColour('green')
        self.labeli2.SetBackgroundColour('green')

        self.labelf1 = wx.StaticText(panel, label='1', size=(20, 20), pos=(190, 0), style=wx.ALIGN_CENTRE)
        self.labelf2 = wx.StaticText(panel, label='2', size=(20, 20), pos=(215, 0), style=wx.ALIGN_CENTRE)
        self.labelf3 = wx.StaticText(panel, label='3', size=(20, 20), pos=(240, 0), style=wx.ALIGN_CENTRE)
        self.labelf1.SetBackgroundColour('green')
        self.labelf2.SetBackgroundColour('green')
        self.labelf3.SetBackgroundColour('green')

        self.labelload1 = wx.StaticText(panel, label='1', size=(20, 20), pos=(420, 25), style=wx.ALIGN_CENTRE)
        self.labelload2 = wx.StaticText(panel, label='2', size=(20, 20), pos=(420, 85), style=wx.ALIGN_CENTRE)
        self.labelload3 = wx.StaticText(panel, label='3', size=(20, 20), pos=(420, 145), style=wx.ALIGN_CENTRE)
        self.labelload1.SetBackgroundColour('green')
        self.labelload2.SetBackgroundColour('green')
        self.labelload3.SetBackgroundColour('green')

        self.labeliv = wx.StaticText(panel, label='0.00V', size=(50, 20), pos=(40, 100), style=wx.ALIGN_CENTRE)
        self.labelic = wx.StaticText(panel, label='0.00A', size=(50, 20), pos=(95, 100), style=wx.ALIGN_CENTRE)
        self.labelfv = wx.StaticText(panel, label='0.00V', size=(50, 20), pos=(170, 110), style=wx.ALIGN_CENTRE)
        self.labelfc = wx.StaticText(panel, label='0.00A', size=(50, 20), pos=(225, 110), style=wx.ALIGN_CENTRE)

        self.labelload1v = wx.StaticText(panel, label='0.00V', size=(50, 20), pos=(450, 15), style=wx.ALIGN_CENTRE)
        self.labelload1c = wx.StaticText(panel, label='0.00A', size=(50, 20), pos=(450, 40), style=wx.ALIGN_CENTRE)
        self.labelload2v = wx.StaticText(panel, label='0.00V', size=(50, 20), pos=(450, 75), style=wx.ALIGN_CENTRE)
        self.labelload2c = wx.StaticText(panel, label='0.00A', size=(50, 20), pos=(450, 100), style=wx.ALIGN_CENTRE)
        self.labelload3v = wx.StaticText(panel, label='0.00V', size=(50, 20), pos=(450, 135), style=wx.ALIGN_CENTRE)
        self.labelload3c = wx.StaticText(panel, label='0.00A', size=(50, 20), pos=(450, 160), style=wx.ALIGN_CENTRE)
        self.labelsys = wx.StaticText(panel, label='ON', size=(100, 20), pos=(550, 20), style=wx.ALIGN_CENTRE)
        self.labelwifi = wx.StaticText(panel, label='Connected', size=(100, 20), pos=(550, 45), style=wx.ALIGN_CENTRE)
        self.labeltime = wx.StaticText(panel, label='00:00 xx/xx/xx', size=(100, 20), pos=(550, 70),
                                       style=wx.ALIGN_CENTRE)

        self.labelload1v.SetBackgroundColour('white')
        self.labelload1c.SetBackgroundColour('white')
        self.labelload2v.SetBackgroundColour('white')
        self.labelload2c.SetBackgroundColour('white')
        self.labelload3v.SetBackgroundColour('white')
        self.labelload3c.SetBackgroundColour('white')

        self.labelsys.SetBackgroundColour('green')
        self.labelwifi.SetBackgroundColour('green')
        self.labeltime.SetBackgroundColour('white')

        self.labeliv.SetBackgroundColour('white')
        self.labelic.SetBackgroundColour('white')
        self.labelfv.SetBackgroundColour('white')
        self.labelfc.SetBackgroundColour('white')

        self.Bind(wx.EVT_TOGGLEBUTTON, self.i1, btni1)
        self.Bind(wx.EVT_TOGGLEBUTTON, self.i2, btni2)
        self.Bind(wx.EVT_TOGGLEBUTTON, self.f1, btnf1)
        self.Bind(wx.EVT_TOGGLEBUTTON, self.f2, btnf2)
        self.Bind(wx.EVT_TOGGLEBUTTON, self.f3, btnf3)
        self.Bind(wx.EVT_TOGGLEBUTTON, self.l1, btnload1)
        self.Bind(wx.EVT_TOGGLEBUTTON, self.l2, btnload2)
        self.Bind(wx.EVT_TOGGLEBUTTON, self.l3, btnload3)

    def i1(self, event):

        obj = event.GetEventObject()
        isPressed = obj.GetValue()

        if isPressed:
            self.labeli1.SetBackgroundColour('red')
            self.labeli1.SetForegroundColour('white')
        else:
            self.labeli1.SetBackgroundColour('green')
            self.labeli1.SetForegroundColour('black')

        self.labeli1.Refresh()

    def i2(self, event):

        obj = event.GetEventObject()
        isPressed = obj.GetValue()

        if isPressed:
            self.labeli2.SetBackgroundColour('red')
            self.labeli2.SetForegroundColour('white')
        else:
            self.labeli2.SetBackgroundColour('green')
            self.labeli2.SetForegroundColour('black')

        self.labeli2.Refresh()

    def f1(self, event):

        obj = event.GetEventObject()
        isPressed = obj.GetValue()

        if isPressed:
            self.labelf1.SetBackgroundColour('red')
            self.labelf1.SetForegroundColour('white')
        else:
            self.labelf1.SetBackgroundColour('green')
            self.labelf1.SetForegroundColour('black')

        self.labelf1.Refresh()

    def f2(self, event):

        obj = event.GetEventObject()
        isPressed = obj.GetValue()

        if isPressed:
            self.labelf2.SetBackgroundColour('red')
            self.labelf2.SetForegroundColour('white')
        else:
            self.labelf2.SetBackgroundColour('green')
            self.labelf2.SetForegroundColour('black')

        self.labelf2.Refresh()

    def f3(self, event):
        obj = event.GetEventObject()
        isPressed = obj.GetValue()

        if isPressed:
            self.labelf3.SetBackgroundColour('red')
            self.labelf3.SetForegroundColour('white')
        else:
            self.labelf3.SetBackgroundColour('green')
            self.labelf3.SetForegroundColour('black')

        self.labelf3.Refresh()

    def l1(self, event):

        obj = event.GetEventObject()
        isPressed = obj.GetValue()

        if isPressed:
            self.labelload1.SetBackgroundColour('yellow')
            self.labelload1.SetForegroundColour('black')
        else:
            self.labelload1.SetBackgroundColour('green')
            self.labelload1.SetForegroundColour('white')

        self.labelload1.Refresh()

    def l2(self, event):

        obj = event.GetEventObject()
        isPressed = obj.GetValue()

        if isPressed:
            self.labelload2.SetBackgroundColour('yellow')
            self.labelload2.SetForegroundColour('black')
        else:
            self.labelload2.SetBackgroundColour('green')
            self.labelload2.SetForegroundColour('white')

        self.labelload2.Refresh()

    def l3(self, event):

        obj = event.GetEventObject()
        isPressed = obj.GetValue()

        if isPressed:
            self.labelload3.SetBackgroundColour('yellow')
            self.labelload3.SetForegroundColour('black')
        else:
            self.labelload3.SetBackgroundColour('green')
            self.labelload3.SetForegroundColour('white')

        self.labelload3.Refresh()


##############################################################
class tf(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title='Configuration Mode', size=(500, 350))
        panel = wx.Panel(self)


#############################################################
class ff(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title='Kids Mode', size=(500, 350))
        panel = wx.Panel(self)


if __name__ == '__main__':
    app = wx.App(False)
    frame = mf(None, title='AMPS Harmonics Distortion Project')
    frame.Show()
app.MainLoop()