from lesson import Lesson
from body import Body, EARTH_R


class Lesson2(Lesson):

    def reset_sim(self):
        self.sim.set_defaults()
        self.viz_window.switch_view_north()
        self.sim.time_step = 5.0
        self.sim.draw_atmosphere = False
        self.sim.draw_mountain = True
        self.sim.planet_transparent = False
        self.viz_window.switch_view_north()


    def step1(self):
        self.text = """\
    <h3><center>Projectile Motion</center></h3>
    <p>For our first lesson, we will travel to a planet very similar to Earth, except that it is perfectly spherical and
    and has no atmosphere. In addition, imagine that this planet has a super tall (1,000 km) mountain with a pure
    vertical drop (basically a BASE jumper's dream).</p>

    <p>If we throw a rock horizontally from the top of the mountain (let's say with a velocity of 1 km/s), it will
     it will trace a parabola and impact a ground at some distance from the base of the mountain.</p>

    <p>Click <b>Start</b> below to see what happens. Click <b>Next</b> after the simulation is done to
    go to the next step in the lesson.</p>
"""
        self.sim.__init__(0)
        self.sim.bodies = [Body((0.0, EARTH_R + self.sim.MOUNTAIN_HEIGHT, 0.0),  (1000, 0.0, 0.0), 0.0)]
        self.sim.bodies[0].record_trajectory = True
        self.sim.bodies[0].orbit_viz_mode = Body.ORBIT_VISUALISATIONS['none']
        self.sim.selected_body = 0
        self.sim.time_barrier = 530.0

    def step2(self):
        self.text = """\
    <h3><center>Projectile Motion - 2</center></h3>
    <p>Now let's see what happens when we throw the same rock from the same mountain, but this time with
    more horizontal velocity. We'll keep the previous trajectory on the screen for comparison</p>

    <p>Again, click <b>Start</b> below to see what happens.</p>
"""
        self.sim.__init__(0)
        self.sim.bodies = [Body((0.0, EARTH_R + self.sim.MOUNTAIN_HEIGHT, 0.0),  (2000, 0.0, 0.0), 0.0),
                           Body((0.0, EARTH_R + self.sim.MOUNTAIN_HEIGHT, 0.0),  (6500, 0.0, 0.0), 0.0)]
        self.sim.bodies[0].record_trajectory = True
        self.sim.bodies[0].orbit_viz_mode = Body.ORBIT_VISUALISATIONS['none']
        self.sim.selected_body = 0
        self.sim.bodies[1].orbit_end = 45
        self.sim.bodies[1].orbit_viz_mode = Body.ORBIT_VISUALISATIONS['orbit']


class Demo1(Lesson):
    # As a hack demo is coded as a lesson

    def step1(self):
        self.text = """\
    <h3><center>Demo - 100 orbits at once</center></h3>
    """
        self.sim.__init__(100)
        self.viz_window.Refresh()
