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
    def __init__(self, parent, sim, viz_window):
        wx.Frame.__init__(self, None, title="Instructions", size=(640, 1024))
        self.parent = parent
        self.sim = sim
        self.viz_window = viz_window

        subbox = wx.BoxSizer(wx.HORIZONTAL)

        button_prev = wx.Button(self, -1, 'Prev')
        self.Bind(wx.EVT_BUTTON, self.OnPrev, button_prev)
        subbox.Add(button_prev, 1, wx.GROW | wx.ALL, 2)

        button_play_pause = wx.Button(self, -1, 'Run/Puase')
        self.Bind(wx.EVT_BUTTON, self.OnRunPause, button_play_pause)
        subbox.Add(button_play_pause, 1, wx.GROW | wx.ALL, 2)

        button_next = wx.Button(self, -1, 'Next')
        self.Bind(wx.EVT_BUTTON, self.OnNext, button_next)
        subbox.Add(button_next, 1, wx.GROW | wx.ALL, 2)

        self.html_window = TutorHTMLWindow(self)
        contents = """\
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
        <li><a href="Lesson1">Orbital Motion</a></li>
        <li>Orbital Elements - Equatorial Orbits</li>
        <li>Circular Orbits</li>
        <li>Hoffman Transfers</li>
        <li>Six Orbital Elements</li>
        <li>Plane Changes</li>
        <li>Orbital Intercept</li>
        <li>Orbital Rendezvous</li>
    </ol>
</body>
</html>
"""
        self.html_window.SetPage(contents)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.html_window, 1, wx.EXPAND)
        sizer.Add(subbox, 0, wx.EXPAND)

        self.SetSizer(sizer)

        self.Bind(wx.EVT_CLOSE, self.OnClose)

    def OnLinkClicked(self, linkinfo):
        lesson = getattr(lessons, linkinfo.Href)(self.sim, self.viz_window)
        step = getattr(lesson, 'step1')
        step()
        self.html_window.SetPage(getattr(lesson, 'text'))

    def OnPrev(self, evt):
        pass

    def OnNext(self, evt):
        pass

    def OnRunPause(self, evt):
        pass

    def OnClose(self, evt):
        self.Destroy()
