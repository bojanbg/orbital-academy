import wx
import wx.html

#from lessons import *  # We use this variant of import because there can be many lessons
import lessons

class TutorHTMLWindow(wx.html.HtmlWindow):
    # We need to subclass to be able to intercept OnLinkClicked event
    def __init__(self, parent):
        wx.html.HtmlWindow.__init__(self, parent)
        self.parent = parent
        if "gtk2" in wx.PlatformInfo:
            self.SetStandardFonts()

    def OnLinkClicked(self, linkinfo):
        self.parent.OnLinkClicked(linkinfo)


class LessonsWindow(wx.Frame):

    INITIAL_CONTENTS = """\
<!DOCTYPE html>
<html>
<head>
    <title>Welcome to Orbital Academy</title>
</head>
<body>
    <h3><center>Welcome to <b>Orbital Academy</b></center></h3>
    <p>Orbital Academy is a place where you can learn orbital mechanics. The curriculum is organized into lessons
    of progressive difficulty. After you completed them all you will have become an expert spacecraft pilot!</p>
    <br>
    <p>The display on the left shows Earth orbital space.</p>
    <p>You can rotate the view by dragging with the right mouse button, and zoom in and out using the mouse wheel.</p>
    <br>
    <p>Click on a lesson to start your journey!</p>
    <ol>
        <li>Conic Sections</li>
        <li><a href="Lesson2">Orbital Motion</a></li>
        <li>Orbital Elements - Equatorial Orbits</li>
        <li>Circular Orbits</li>
        <li><a href="Lesson5">Hohman Transfers</a></li>
        <li>Six Orbital Elements</li>
        <li>Plane Changes</li>
        <li>Orbital Intercept</li>
        <li>Orbital Rendezvous</li>
    </ol>
    <p>Demos</p>
    <ul>
        <li><a href="Demo1">A lot of objects</a></li>
    </ul>
</body>
</html>
"""

    def __init__(self, parent, sim, viz_window):
        wx.Frame.__init__(self, None, title="Instructions", size=(640, 800))
        self.parent = parent
        self.sim = sim
        self.viz_window = viz_window
        self.viz_window.sim_state_change_callback = self  # Set up callback for sim state changes

        self.lesson = None
        self.lesson_step = None

        subbox = wx.BoxSizer(wx.HORIZONTAL)

        button_prev = wx.Button(self, -1, 'Prev')
        self.Bind(wx.EVT_BUTTON, self.OnPrev, button_prev)
        subbox.Add(button_prev, 1, wx.GROW | wx.ALL, 2)

        self.button_start_pause = wx.Button(self, -1, 'Start')
        self.Bind(wx.EVT_BUTTON, self.OnStartPause, self.button_start_pause)
        subbox.Add(self.button_start_pause, 1, wx.GROW | wx.ALL, 2)

        button_next = wx.Button(self, -1, 'Next')
        self.Bind(wx.EVT_BUTTON, self.OnNext, button_next)
        subbox.Add(button_next, 1, wx.GROW | wx.ALL, 2)

        self.html_window = TutorHTMLWindow(self)
        self.html_window.SetPage(self.INITIAL_CONTENTS)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.html_window, 1, wx.EXPAND)
        sizer.Add(subbox, 0, wx.EXPAND)

        self.SetSizer(sizer)

        self.Bind(wx.EVT_CLOSE, self.OnClose)

    def OnLinkClicked(self, linkinfo):
        self.lesson = getattr(lessons, linkinfo.Href)(self.sim, self.viz_window)
        self.lesson_step = 1
        step_method = getattr(self.lesson, 'step%d' % self.lesson_step)
        step_method()
        self.lesson.reset_sim()
        self.html_window.SetPage(getattr(self.lesson, 'text'))

    def OnPrev(self, evt):
        if self.lesson_step > 1:
            self.lesson_step -= 1
            step_method = getattr(self.lesson, 'step%d' % self.lesson_step)
            step_method()
            self.lesson.reset_sim()
            self.html_window.SetPage(getattr(self.lesson, 'text'))
        else:
            self.html_window.SetPage(self.INITIAL_CONTENTS)
        self.OnSimStateChange()

    def OnNext(self, evt):
        try:
            step_method = getattr(self.lesson, 'step%d' % (self.lesson_step + 1))
            self.lesson_step += 1
            step_method()
            self.lesson.reset_sim()
            self.html_window.SetPage(getattr(self.lesson, 'text'))
        except AttributeError:
            pass
        self.OnSimStateChange()

    def OnStartPause(self, evt):
        if self.sim.state == 'running':
            self.viz_window.OnPauseSim(None)
        elif self.sim.state in ('pre-run', 'paused'):
            self.viz_window.OnStartSim(None)
        elif self.sim.state == 'finished':
            # Reset sim
            step_method = getattr(self.lesson, 'step%d' % self.lesson_step)
            step_method()
            self.lesson.reset_sim()
            self.viz_window.OnStartSim(None)

    def OnClose(self, evt):
        self.viz_window.OnClose(None)
        self.Destroy()

    def OnSimStateChange(self):
        if self.sim.state == 'pre-run':
            self.button_start_pause.SetLabel('Start')
        elif self.sim.state == 'running':
            self.button_start_pause.SetLabel('Pause')
        elif self.sim.state == 'paused':
            self.button_start_pause.SetLabel('Resume')
        elif self.sim.state == 'finished':
            self.button_start_pause.SetLabel('Restart')
