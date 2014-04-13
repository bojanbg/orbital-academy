from lesson import Lesson
from simulation import Simulation

class Lesson1(Lesson):

    def step1(self):
        self.text = """\
    <h3><center>Projectile Motion</center></h3>
    <p>For our first lesson, we will travel to a planet very similar to Earth, except that it is perfectly spherical and
    and has no atmosphere. In addition, imagine that this planet has a super tall (1,000 km) mountain with a pure
    vertical drop (basically a BASE jumper's dream).</p>

    <p>If we throw a rock horizontally from the top of the mountain (let's say with a velocity of 1 km/s), it will
     it will trace a parabola and impact a ground at some distance from the base of the mountain.</p>
"""
        self.sim.selected_body = None
        self.sim.bodies = []
        self.sim.draw_atmosphere = False
        self.sim.draw_mountain = True
        self.sim.planet_transparent = False
        self.viz_window.switch_view_north()

    def step2(self):
        pass


class Demo1(Lesson):
    # As a hack demo is coded as a lesson

    def step1(self):
        self.text = """\
    <h3><center>Demo - 100 orbits at once</center></h3>
    """
        self.sim.__init__(100)
        self.viz_window.Refresh()