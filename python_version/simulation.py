from body import Body, EARTH_MU


class Simulation(object):

    def __init__(self, num_random_objs):
        self.bodies = []
        self.selected_body = 0

        self.bodies.append(Body.generate_circular_equatorial_orbit(6.0E5, (0.0, 1.0, 1.0, 1.0)))
        self.bodies.append(Body.generate_circular_equatorial_orbit(1.2E6))

        for x in xrange(num_random_objs):
            self.bodies.append(Body.generate_random_orbit())

        self.pos_viz_mode = Body.POSITION_VISUALISATIONS['symbol']
        self.orbit_viz_mode = Body.ORBIT_VISUALISATIONS['all']

        self.set_defaults()

    def set_defaults(self):
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

    def step_time(self):
        if self.time < self.time_barrier:
            self.time += self.time_step
