import wx

class SetScalingsDialog(wx.Dialog):
    def __init__(self, *args, **kw):
        super(SetScalingsDialog, self).__init__(*args, **kw)
        
        self.InitUI()
        self.SetSize((300, 200))
        self.SetTitle('Adjust Max Load Currents')

    def InitUI(self):
        
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)
        
        sb = wx.StaticBox(panel, label='Max Load Currents')
        sbs = wx.StaticBoxSizer(sb, orient=wx.VERTICAL)

        hboxLoad1 = wx.BoxSizer(wx.HORIZONTAL)
        hboxLoad2 = wx.BoxSizer(wx.HORIZONTAL)
        hboxLoad3 = wx.BoxSizer(wx.HORIZONTAL)
        hboxButtons = wx.BoxSizer(wx.HORIZONTAL)

        
        self.Load1TextCtrl = wx.TextCtrl(panel, value='600')
        self.Load2TextCtrl = wx.TextCtrl(panel, value='600')
        self.Load3TextCtrl = wx.TextCtrl(panel, value='600')

        hboxLoad1.Add(wx.StaticText(panel, label='Load 1 Max Current (mA)'))
        hboxLoad1.Add(self.Load1TextCtrl, flag=wx.LEFT, border=10)
        sbs.Add(hboxLoad1)
        
        hboxLoad2.Add(wx.StaticText(panel, label='Load 2 Max Current (mA)'))
        hboxLoad2.Add(self.Load2TextCtrl, flag=wx.LEFT, border=10)
        sbs.Add(hboxLoad2)
        
        hboxLoad3.Add(wx.StaticText(panel, label='Load 3 Max Current (mA)'))
        hboxLoad3.Add(self.Load3TextCtrl, flag=wx.LEFT, border=10)
        sbs.Add(hboxLoad3)
        
        panel.SetSizer(sbs)

        okButton = wx.Button(self, label='Ok')
        cancelButton = wx.Button(self, label='Cancel')

        hboxButtons.Add(okButton)
        hboxButtons.Add(cancelButton, flag=wx.LEFT, border=5)

        vbox.Add(panel, proportion=1, flag=wx.ALL|wx.EXPAND, border=10)
        vbox.Add(hboxButtons, flag=wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, border=10)
        
        self.SetSizer(vbox)
        
        okButton.Bind(wx.EVT_BUTTON, self.OnOK)
        cancelButton.Bind(wx.EVT_BUTTON, self.OnCancel)

        self.Load1Max = None
        self.Load2Max = None
        self.Load3Max = None

    def OnOK(self, e):
        self.Load1Max = self.Load1TextCtrl.GetValue()
        self.Load2Max = self.Load2TextCtrl.GetValue()
        self.Load3Max = self.Load3TextCtrl.GetValue()
        self.EndModal(wx.ID_OK)
        #self.Destroy()

    def OnCancel(self, e):
        self.EndModal(wx.ID_CANCEL)
        #self.Destroy()
