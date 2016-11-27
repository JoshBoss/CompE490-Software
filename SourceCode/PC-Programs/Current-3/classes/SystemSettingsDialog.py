import wx

class SystemSettingsDialog(wx.Dialog):
    def __init__(self, *args, **kw):
        super(SystemSettingsDialog, self).__init__(*args, **kw)
        
        self.InitUI()
        self.SetSize((350, 200))
        self.SetTitle('System Settings')

    def InitUI(self):
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)
        
        staticBox = wx.StaticBox(panel)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, orient=wx.VERTICAL)
        
        hboxIP = wx.BoxSizer(wx.HORIZONTAL)
        hboxDRR = wx.BoxSizer(wx.HORIZONTAL)
        hboxDRRNote = wx.BoxSizer(wx.HORIZONTAL)
        hboxSTO = wx.BoxSizer(wx.HORIZONTAL)
        hboxSTONote = wx.BoxSizer(wx.HORIZONTAL)
        hboxButtons = wx.BoxSizer(wx.HORIZONTAL)

        self.IPTextControl = wx.TextCtrl(panel, value='169.254.215.105')
        self.DRRTextControl = wx.TextCtrl(panel, value='0.85')
        self.STOTextControl = wx.TextCtrl(panel, value='0.35')

        hboxIP.Add(wx.StaticText(panel, label='Raspberry Pi IP Address '))
        hboxIP.Add(self.IPTextControl, flag=wx.LEFT, border=10)        
        staticBoxSizer.Add(hboxIP)
        
        hboxDRR.Add(wx.StaticText(panel, label='Data Request Rate (s)   '))
        hboxDRR.Add(self.DRRTextControl, flag=wx.LEFT, border=10)
        staticBoxSizer.Add(hboxDRR)
        
        hboxDRRNote.Add(wx.StaticText(panel, label='* We recommend a request rate of 0.5 seconds'))
        staticBoxSizer.Add(hboxDRRNote)

        hboxSTO.Add(wx.StaticText(panel, label='Socket Timeout (s)      '))
        hboxSTO.Add(self.STOTextControl, flag=wx.LEFT, border=10)
        staticBoxSizer.Add(hboxSTO)
        
        hboxSTONote.Add(wx.StaticText(panel, label='* We recommend a socket timeout of 0.35 seconds'))
        staticBoxSizer.Add(hboxSTONote)

        panel.SetSizer(staticBoxSizer)
        
        okButton = wx.Button(self, label='Ok')
        cancelButton = wx.Button(self, label='Cancel')

        hboxButtons.Add(okButton)
        hboxButtons.Add(cancelButton, flag=wx.LEFT, border=10)

        vbox.Add(panel, proportion=1, flag=wx.ALL|wx.EXPAND, border=10)
        vbox.Add(hboxButtons, flag=wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, border=10)
        
        self.SetSizer(vbox)

        okButton.Bind(wx.EVT_BUTTON, self.OnOK)
        cancelButton.Bind(wx.EVT_BUTTON, self.OnCancel)

        self.IP = None
        self.DRR = None
        self.STO = None

    def OnOK(self, e):
        self.IP = self.IPTextControl.GetValue()
        self.DRR = self.DRRTextControl.GetValue()
        self.STOP = self.STOTextControl.GetValue()
        self.EndModal(wx.ID_OK)

    def OnCancel(self, e):
        self.EndModal(wx.ID_CANCEL)
