import wx
import wx.html
from wx.lib.wordwrap import wordwrap

class AboutDlg(wx.Frame):
 
    def __init__(self, parent):
 
        wx.Frame.__init__(self, parent, wx.ID_ANY, title="User Manual", size=(400,400))
 
        html = wxHTML(self)
 
        html.SetPage(
            ''
 
            "<h2>Aztec Microgrid Power System GUI user guide.</h2>"
 
            "<h3>Live Mode</h3>"
 
	    "<h4>Connecting to Model</h4>"

            "<p>First, turn the model on by flipping the ON switch on the box.</p>"


	    "<p>Once the 'WiFi-Ready' LED is on, connect to the AMPS access point on the"

	    " computer running the GUI. The password is 'SDSUpower'.</p>"

	    "<p>Launch the GUI by double clicking on AMPSGUI.exe and press the Connect button. </p>"

	    "<h4>GUI Functionality</h4>"
	    "<p>While the system is running, you can control which current waveforms are displayed"
	    " on the upper left plot, while the upper right plot displays the harmonic content"
	    " of the loads, respectively.</p>"
	    "<p>To add the current waveforms for loads 1 - 3, simply click the ""Load 1 - OFF"" buttons. Adding the load will also add the corresponding Fourier transform on the upper right plot.</p>"

	    "<p>The lower left plot will display the mains voltage (120VRMS) and the lower right"
	    " will display the harmonic content of the voltage source.</p>"

 	    "<p>While the system is running, you can save the most recent data to a local text file. This saved file can later be loaded while the system is not connected.</p>"

	    "<h3>Offline Mode</h3>"
	    "<p>By saving data during a connected session, the user can later use the software on it's own. Instead of connecting, simply press the Load Data button and load a previously saved file. Note that the data saved will only include the data from the inverter that was selected at the time and the load data is based off of the filtered/non-filtered outputs.</p>"

	    "<p>Note that all other GUI functionalities, such as selecting which current waveforms to display and viewing harmonic content, are still available.</p>"
	    
            "<p><b>Software used in making this demo:</h3></p>"
 
            '<p><b><a href="http://www.python.org">Python 2.4</a></b></p>'
 
            '<p><b><a href="http://www.wxpython.org">wxPython 2.8</a></b></p>'
            )
 
class wxHTML(wx.html.HtmlWindow):
     def OnLinkClicked(self, link):
         webbrowser.open(link.GetHref())
