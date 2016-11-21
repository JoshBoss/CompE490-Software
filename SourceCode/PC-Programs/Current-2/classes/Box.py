import wx


class BoundControlBox(wx.Panel):
    def __init__(self, parent, ID, label, initval):
        wx.Panel.__init__(self, parent, ID)
        
        self.value = initval
        box = wx.StaticBox(self, -1, label)
        sizer = wx.StaticBoxSizer(box, wx.VERTICAL)
        self.reset_btn = wx.Button(self, -1, label="Reset")
        self.radio_grid = wx.CheckBox(self, -1,
            label="Grid", style=0)
        self.radio_grid.SetValue(True)
        self.slider = wx.Slider(self, -1, 50, 1, 170, size=(100,30))
        self.slider.SetTickFreq(5,1)
        self.slider.SetValue(self.value)
        self.Bind(wx.EVT_SLIDER, self.on_slider, self.slider)
        self.Bind(wx.EVT_CHECKBOX, self.on_grid, self.radio_grid)
        self.Bind(wx.EVT_BUTTON, self.on_click, self.reset_btn)
        
        sizer.Add(self.slider, 0, wx.ALL, 10)
        sizer.Add(self.radio_grid, 0, wx.ALL, 10)
        sizer.Add(self.reset_btn, 0, wx.ALL, 10)
        self.SetSizer(sizer)
        sizer.Fit(self)
        
    def on_grid(self):
        return self.radio_grid.GetValue()
    
    def on_click(self, event):
        pass
        #return self.reset_btn.GetValue()
        
    def on_slider(self,event):
        self.value = self.slider.GetValue()
            
    def update_value(self):
        return self.value