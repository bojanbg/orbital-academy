class Lesson(object):

    def __init__(self, sim, viz_window):
        self.sim = sim
        self.viz_window = viz_window
        self.text = None

    def reset_view(self):
        self.sim.default_view
        self.viz_window.switch_view_north()
