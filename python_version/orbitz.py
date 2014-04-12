import wx

from main_window import VizWindow
from scene import Scene
from lesson import *


if __name__ == '__main__':

    class OrbitzApp(wx.App):

        def OnInit(self):
            scene = Scene(4)
            visualization_window = VizWindow(scene)
            visualization_window.Show(True)
            self.SetTopWindow(visualization_window)

            lessons_window = LessonsWindow(scene)
            lessons_window.Show(True)
            return True

    app = OrbitzApp(False)
    app.MainLoop()
