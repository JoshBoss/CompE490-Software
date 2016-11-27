import wx
import wx.html


class AboutDlg(wx.Frame):
 
    def __init__(self, parent):
 
        wx.Frame.__init__(self, parent, wx.ID_ANY, title="About", size=(400,400))
        html = wxHTML(self)
        
        html.SetPage(
            ''
 
            "<h2>About The User Interface</h2>"
 
            "<p>This User Interface is for demo purposes only. It was created in November 2016.</p>"
 
            "<p> By Abdullah Maarafi, Ben Santacruz, Patrick Gutierrez, Daniel Valencia and Joshua Boss.</p>"
 
            "<p><b>Software used in making this demo:</h3></p>"
 
            '<p><b><a href="https://www.python.org/downloads/release/python-2712/">Python 2.7</a></b></p>'
 
            '<p><b><a href="http://www.wxpython.org">wxPython 3.0.2</a></b></p>'
            )

class wxHTML(wx.html.HtmlWindow):
     def OnLinkClicked(self, link):
         wx.LaunchDefaultBrowser(link.GetHref())