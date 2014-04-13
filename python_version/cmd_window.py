import wx
import wx.html


class CommandWindow(wx.Frame):

    def __init__(self, parent, sim, viz_window):
        wx.Frame.__init__(self, None, title="Command List", size=(320, 480))
        self.parent = parent
        self.sim = sim
        self.viz_window = viz_window

        sizer = wx.BoxSizer(wx.VERTICAL)
        self.command_box = wx.TextCtrl(self, style=wx.TE_MULTILINE)
        button_exec = wx.Button(self, -1, 'Execute')
        self.Bind(wx.EVT_BUTTON, self.OnExecute, button_exec)

        sizer.Add(self.command_box, 1, wx.EXPAND)
        sizer.Add(button_exec, 0, wx.EXPAND)

        self.SetSizer(sizer)

        # self.Bind(wx.EVT_CLOSE, self.OnClose)

    def process_command(self, line):
        print line

    def OnExecute(self, event):
        self.command_box.SetEditable(False)
        for line in self.command_box.GetValue().split('\n'):
            self.process_command(line)

    def OnClose(self, evt):
        self.Destroy()
