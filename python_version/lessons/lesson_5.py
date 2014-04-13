from lesson import Lesson
from body import Body


class Lesson5(Lesson):

    def step1(self):
        self.text = """\
    <h3><center>Hohman Transfers</center></h3>
    <p>Hohman transfer orbits are used to transfer between two circular orbits in the same plane.</p>

    <p>Let's start with a circular orbit at altitude of 1,000 km above Earth, and a target orbit that is also circular
    at an altitude of 10,000 km. Both orbits are equatorial.</p>
"""
        self.sim.__init__(0)
        self.sim.bodies = [Body.generate_circular_equatorial_orbit(1.0E6, (0.0, 1.0, 1.0, 1.0)),
                           Body.generate_circular_equatorial_orbit(1.0E7)]
        self.sim.bodies[0].record_trajectory = True
        self.sim.bodies[0].orbit_viz_mode = Body.ORBIT_VISUALISATIONS['none']

        self.reset_sim()
        self.sim.time_barrier = 1000.0
        self.viz_window.switch_view_north(12.0)

    def step2(self):
        self.text = """\
    <p>And it's step 2!</p>
"""
