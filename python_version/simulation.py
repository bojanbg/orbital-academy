from body import Body


class Simulation(object):
    MOUNTAIN_HEIGHT = 1E06  # 1000 km

    def __init__(self, num_random_objs):
        self.bodies = []
        self.selected_body = None

        if num_random_objs > 0:
            self.selected_body = 0
            self.bodies.append(Body.generate_circular_equatorial_orbit(6.0E5, (0.0, 1.0, 1.0, 1.0)))
            self.bodies.append(Body.generate_circular_equatorial_orbit(1.2E6))
            for x in xrange(num_random_objs - 2):
                self.bodies.append(Body.generate_random_orbit())

        self.pos_viz_mode = Body.POSITION_VISUALISATIONS['symbol']
        self.orbit_viz_mode = Body.ORBIT_VISUALISATIONS['all']

        self.set_defaults()

    def set_defaults(self):
        self.state = 'pre-run'
        self.time = 0.0
        self.time_step = 10.0
        self.time_barrier = 1.0E15

        self.draw_atmosphere = True
        self.draw_mountain = False
        self.planet_transparent = True

    def current_body(self):
        if self.selected_body is not None:
            return self.bodies[self.selected_body]
        else:
            return None

    def start(self):
        if self.state in ('pre-run', 'paused'):
            self.state = 'running'

    def pause(self):
        if self.state == 'running':
            self.state = 'paused'

    def step_time(self):
        if self.state != 'finished':
            if self.state == 'running' and self.time < self.time_barrier:
                self.time += self.time_step
            else:
                self.state = 'finished'

    def forward_time(self, t):
        self.time = t
        for body in self.bodies:
            body.calc_state_vectors(t)
