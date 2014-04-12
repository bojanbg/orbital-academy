import numpy

from body import Body, EARTH_R, EARTH_MU


class Simulation(object):

    def __init__(self, num_random_objs):
        self.switch_view_north()

        self.bodies = []
        self.selected_body = 0
        # For circular orbits, v = sqrt(gamma/r)
        self.bodies.append(Body((7.0E6, 0.0, 0.0), (0.0, numpy.sqrt(EARTH_MU / 7.0E6), 0.0), 0.0, (0.0, 1.0, 1.0, 1.0)))
        self.bodies.append(Body((-7.5E6, 0.0, 0.0), (0.0, -numpy.sqrt(EARTH_MU / 7.5E6), 0.0), 0.0))

        for x in xrange(num_random_objs):
            self.bodies.append(Body.generate_random_orbit())

        self.pos_viz_mode = Body.POSITION_VISUALISATIONS['symbol']
        self.orbit_viz_mode = Body.ORBIT_VISUALISATIONS['all']

        self.time = 0.0
        self.time_step = 1.0

    def current_body(self):
        return self.bodies[self.selected_body]

    def switch_view_north(self):
        """Switches the view to a North top-down view from the default distance."""
        self.camera_up = (0.0, 1.0, 0.0); self.camera_right = (1.0, 0.0, 0.0)
        self.camera_vector = (0.0, 0.0, 6 * EARTH_R)
