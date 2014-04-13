class Lesson(object):

    def __init__(self, sim, viz_window):
        self.sim = sim
        self.viz_window = viz_window
        self.text = None

    def reset_sim(self):
        self.sim.set_defaults()
        self.viz_window.switch_view_north()
