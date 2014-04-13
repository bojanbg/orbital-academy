import wx

from viz_window import VizWindow
from simulation import Simulation
from tutor import *


if __name__ == '__main__':

    class OrbitzApp(wx.App):

        def OnInit(self):
            simulation = Simulation(5)
            visualization_window = VizWindow(simulation)
            visualization_window.Show(True)
            self.SetTopWindow(visualization_window)

            lessons_window = LessonsWindow(self, simulation, visualization_window)
            lessons_window.Show(True)
            return True

    app = OrbitzApp(False)
    app.MainLoop()
