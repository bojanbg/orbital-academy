from lesson import Lesson
from body import Body, EARTH_R


class Lesson2(Lesson):

    def reset_sim(self):
        self.viz_window.switch_view_north()
        self.sim.draw_atmosphere = False
        self.sim.draw_mountain = True
        self.sim.planet_transparent = False
        self.viz_window.switch_view_north()

    def _newtons_rock(self, speed):
        body = Body((10.0, EARTH_R + self.sim.MOUNTAIN_HEIGHT, 10.0),  (speed, 0.0, 0.0), 0.0, (0.5, 0.5, 0.5, 0.5))
        body.orbit_end = 270
        body.pos_viz_mode = Body.POSITION_VISUALISATIONS['dot']
        body.orbit_viz_mode = Body.ORBIT_VISUALISATIONS['orbit']
        return body

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
        self.sim.time_step = 5.0
        self.sim.time_barrier = 530.0

    def step2(self):
        self.text = """\
    <h3><center>Projectile Motion - 2</center></h3>
    <p>Now let's see what happens when we throw the same rock from the same mountain, but this time with
    more horizontal velocity. We'll keep the previous trajectory on the screen for comparison</p>

    <p>Again, click <b>Start</b> below to see what happens.</p>
"""
        self.sim.__init__(0)
        self.sim.bodies = [Body((10.0, EARTH_R + self.sim.MOUNTAIN_HEIGHT, 10.0),  (2000, 0.0, 0.0), 0.0),
                           self._newtons_rock(1000)]
        self.sim.bodies[0].record_trajectory = True
        self.sim.bodies[0].orbit_viz_mode = Body.ORBIT_VISUALISATIONS['none']
        self.sim.selected_body = 0
        self.sim.time_barrier = 600.0

    def step3(self):
        self.text = """\
    <h3><center>Projectile Motion - 3</center></h3>
    <h4>Progressively faster projectiles</h4>

    <p>Here we see the trajectories of rocks thrown with a horizontal velocity of 1 to 6 km/s. Click <b>Start</b> to
    see what will happen with a one thrown at 7 km/s</p>
"""
        self.sim.__init__(0)
        self.sim.bodies = [Body((10.0, EARTH_R + self.sim.MOUNTAIN_HEIGHT, 10.0),  (7000, 0.0, 0.0), 0.0),
                           self._newtons_rock(6000), self._newtons_rock(5000), self._newtons_rock(4000),
                           self._newtons_rock(3000), self._newtons_rock(2000), self._newtons_rock(1000)]
        self.sim.bodies[0].record_trajectory = True
        self.sim.bodies[0].orbit_viz_mode = Body.ORBIT_VISUALISATIONS['none']
        self.sim.selected_body = 0
        self.sim.time_barrier = 2200

    def step4(self):
        self.text = """\
    <h3><center>Projectile Motion - 4</center></h3>
    <h4>When you fall and miss the Earth</h4>

    <p>One of the rocks previously almost went around the Earth. Finally, let's look at what happens when we
    throw a projectile even faster.</p>

    <p>Well, it travels so fast that it never hits the Earth! Note that the projectile is constantly falling - it's
    just that the Earth's surface is "falling" away from it more quickly. We say that the projectile is in free fall,
    and the trajectory that it draws is called an orbit.</p>

    <p>Also note how our projectile (rock) returns to the <b>exact</b> same place that it started of. If you
    look closer you will notice that it has exactly the same velocity, too. That means it will forever go around
    the Earth!</p>
"""
        self.sim.__init__(0)
        self.sim.bodies = [Body((10.0, EARTH_R + self.sim.MOUNTAIN_HEIGHT, 10.0),  (7200, 0.0, 0.0), 0.0)]
        # self.sim.bodies[0].record_trajectory = True
        # self.sim.bodies[0].orbit_viz_mode = Body.ORBIT_VISUALISATIONS['none']
        self.sim.selected_body = 0


class Demo1(Lesson):
    # As a hack demo is coded as a lesson

    def step1(self):
        self.text = """\
    <h3><center>Demo - 100 orbits at once</center></h3>
    """
        self.sim.__init__(100)
        self.viz_window.Refresh()


class Demo2(Lesson):
    # As a hack demo is coded as a lesson

    def reset_sim(self):
        self.viz_window.switch_view_north(12.0)
        self.sim.selected_body = 1
        self.sim.time_step = 2.0


    def step1(self):
        self.text = """\
    <h3><center>Command Lists</center></h3>
    <p>Demos the use of command lists to perform complicated oribtal manouvers.</p>

    <p>Available commands are (one per line):</p>
    <ul>
        <li>wait(t) - waits for <em>t<em> seconds</li>
        <li>at(t) - waits until time <em>t<em></li>
        <li>prograde() - returns <em>prograde<em> unit vector</li>
        <li>retrograde() - returns <em>retrograde<em> unit vector</li>
        <li>normal() - returns <em>orbit-normal<em> unit vector</li>
        <li>antinormal() - returns <em>orbit-antinormal<em> unit vector</li>
        <li>dv(dv) - applies <em>dv<em> change of velocity</li>
    </ul>
    <p>An example command list:</p>
    <pre>
    wait(10)  # wait 10 seconds
    dv(prograde() * 100)  # prograde burn, 100 m/s
    at(100)  # wait until time=100 seconds
    dv(prograde() * 200)  # prograde burn, 200 m/s
    </pre>
"""
        self.sim.__init__(0)
        self.sim.bodies = [Body.generate_circular_equatorial_orbit(1.0E7),
                           Body.generate_circular_equatorial_orbit(1.0E6, (0.0, 1.0, 1.0, 1.0))]

        self.sim.bodies[0].pos_viz_mode = Body.POSITION_VISUALISATIONS['rv']
        self.sim.bodies[1].pos_viz_mode = Body.POSITION_VISUALISATIONS['rv']

        self.reset_sim()
        self.viz_window.switch_view_north(12.0)
