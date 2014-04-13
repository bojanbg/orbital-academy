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

    def process_command(self, line):
        # Execute line in the context of the selected object

        def wait(t):
            self.sim.forward_time(self.sim.time + t)

        def at(t):
            self.sim.forward_time(t)

        def prograde():
            return self.sim.current_body().prograde()

        def retrograde():
            return self.sim.current_body().retrograde()

        def normal():
            return self.sim.current_body().orbit_normal()

        def antinormal():
            return self.sim.current_body().orbit_antinormal()

        def dv(dv):
            self.sim.current_body().apply_dv(dv, self.sim.time)

        eval(line)  # , globals, locals
        self.viz_window.Refresh()

    def OnExecute(self, event):
        # self.command_box.SetEditable(False)
        for line in self.command_box.GetValue().split('\n'):
            self.process_command(line)

    def OnClose(self, evt):
        self.Destroy()
