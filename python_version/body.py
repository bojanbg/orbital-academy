import numpy

EARTH_R = 6.371E6
EARTH_MU = 3.986004418E14  # G * M_EARTH
SQRT_EARTH_MU = numpy.sqrt(EARTH_MU)


class Body(object):
    POSITION_VISUALISATIONS = {'symbol': 0, 'rv': 1, 'dot': 2}
    ORBIT_VISUALISATIONS = {'all': 0, 'orbit': 1, 'none': 2}

    def __init__(self, r, v, t0, orbit_color=(1.0, 1.0, 0.0, 1.0), stipple=None, record_trajectory=False):
        if isinstance(r, tuple):
            r = numpy.array(r)
        if isinstance(v, tuple):
            v = numpy.array(v)
        self.r = r
        self.v = v
        self.t0 = t0
        self.orbit_color = orbit_color
        self.stipple = stipple
        self.record_trajectory = record_trajectory
        self.trajectory = []
        self.collided_time = None  # If a collision with the planet happens at any point in time, this will be set

        self.r0 = r
        self.r0_ = numpy.linalg.norm(self.r0)
        self.v0 = v
        self.calc_orbital_params()

        self.pos_viz_mode = Body.POSITION_VISUALISATIONS['symbol']
        self.orbit_viz_mode = Body.ORBIT_VISUALISATIONS['all']

        # For drawing partial orbits, these would change to the angles required
        self.orbit_start, self.orbit_end = 0.0, 360.0

    def clone(self):
        new_body = Body(self.r, self.v, self.t0, self.orbit_color, self.stipple, self.record_trajectory)
        self.pos_viz_mode = Body.POSITION_VISUALISATIONS['dot']
        self.orbit_viz_mode = Body.ORBIT_VISUALISATIONS['orbit']
        return new_body

    def calc_orbital_params(self):
        #Calculates Keplerian orbital parameters based on the state vectors
        #This method should be called after each change to velocity vector

        #a = - mu / (v^2 - 2 * mu/r)
        v_2 = numpy.vdot(self.v, self.v)
        r_ = numpy.linalg.norm(self.r)
        # TODO: this won't work for parabolic trajectories (as the denominator is 0)!
        self.a = -EARTH_MU / (v_2 - 2 * EARTH_MU / r_)

        #T = 2*Pi*sqrt(a^3/ni)
        # TODO: again, orbital period is not defined for non-bound orbits
        self.T = 2.0 * numpy.pi * numpy.sqrt(self.a**3 / EARTH_MU)

        #Calculate specific relative angular momentum h = r X v
        h = numpy.cross(self.r, self.v)
        h_2 = numpy.vdot(h, h)
        h_ = numpy.sqrt(h_2)

        #Calculate eccentricity vector e = (v X h) / EARTH_MU - r/|r|
        e = numpy.cross(self.v, h) / EARTH_MU - self.r/r_
        self.e = numpy.linalg.norm(e)

        i_rad = numpy.arccos(h[2] / h_) #h[2] = hz
        self.i = numpy.degrees(i_rad)
        #However, some soruces state that if hz < 0 then inclination is 180 deg - i; should check this
        #n is the vector pointing to the ascending node
        n = numpy.array((-h[1], h[0], 0))
        n_ = numpy.linalg.norm(n)
        if i_rad == 0.0:
            o_rad = 0.0
        else:
            if n[1] >= 0.0: #ie. if h[0] >= 0
                o_rad = numpy.arccos(n[0] / n_)
            else:
                o_rad = 2 * numpy.pi - numpy.arccos(n[0] / n_)
        self.o = numpy.degrees(o_rad)

        #Calculate ni (true anomaly)
        q = numpy.vdot(self.r, self.v) #What the hell is q?
        ni_x = h_2 / (r_ * EARTH_MU) - 1.0
        ni_y = h_ * q / (r_ * EARTH_MU)
        self.ni = numpy.degrees(numpy.arctan2(ni_y, ni_x))

        if self.e == 0.0:
            #For circular orbit w is 0 by convention
            self.w = 0.0
        else:
            if n_ == 0.0:
                #For equatorial orbit
                self.w = numpy.degrees(numpy.arctan2(e[1], e[0]))
            else:
                self.w = numpy.degrees(numpy.arccos(numpy.vdot(n, e) / (n_ * self.e)))
        if e[2] < 0.0:
            self.w = 360.0 - self.w
        if self.w < 0.0:
            self.w = 360.0 + self.w

        self.rp = self.a * (1.0 - self.e) #Periapsis distance
        self.ra = self.a * (1.0 + self.e) #Apoapsis distance

    def apply_dv(self, dv, t):
        self.v += dv
        self.v0 = self.v
        self.r0 = self.r
        self.r0_ = numpy.linalg.norm(self.r0)
        self.t0 = t
        self.calc_orbital_params()

    def calc_state_vectors(self, t):
        # Based on Keplerian orbital parameters calculates state vectors at time t0 + t
        # Algorithm from "Fundamentals of astrodynamics" by Roger R. Bate, Donald D. Mueller and Jerry E. White

        def evaluate_t_dt(x):
            # Evaluates t(x) and dt(x)/dx and returns them as a tuple.
            # We use these to find x via Newton's numerical approximation method.
            # Both values are evaluated in one function (as opposed to evaluate_t and evaluate_dt)
            # to avoid calculating z, sqrt(z), C, S twice.
            z = x**2 / self.a
            sqrt_z = numpy.sqrt(z)
            C = (1.0 - numpy.cos(sqrt_z)) / z
            S = (sqrt_z - numpy.sin(sqrt_z)) / numpy.sqrt(z**3)
            t = (numpy.vdot(self.r0, self.v0) / SQRT_EARTH_MU * x**2 * C + (1.0 - self.r0_ / self.a) * x**3 * S + self.r0_ * x) / SQRT_EARTH_MU
            dt = (x**2 * C + numpy.vdot(self.r0, self.v0) / SQRT_EARTH_MU * x * (1.0 - z * S) + self.r0_ * (1.0 - z * C)) / SQRT_EARTH_MU
            return (t, dt)

        # Don't move object once it has collided with the surface
        if self.collided_time and t > self.collided_time:
            return

        # First we find x using Newton's method. It converges remarkably quickly.
        # For elliptical orbits (including circular), we use sqrt(mu)*(t-t0)/a as the first approximation
        # NOTE: Parabolic and hyperbolic orbits are not supported at the moment!

        # We simplfy by setting t0 to be 0 and solving for delta_t, instead of solving for t with some non-zero t0
        # (which is more complicated)
        delta_t = t - self.t0
        x_guess = SQRT_EARTH_MU * delta_t / self.a #Initial guess
        t_guess, slope = evaluate_t_dt(x_guess)
        while abs(delta_t - t_guess) > 1.0E-10:
            x_guess = x_guess + (delta_t - t_guess) / slope
            t_guess, slope = evaluate_t_dt(x_guess)
        x = x_guess
        #TODO: rewrite above into a for loop with a break so that the loop is guaranteed to exit as opposed to now

        # x is now the value we've been looking for
        # Next, we calculate f, g, f_dot and g_dot and from these r and v
        z = x**2 / self.a
        sqrt_z = numpy.sqrt(z)
        C = (1.0 - numpy.cos(sqrt_z)) / z
        S = (sqrt_z - numpy.sin(sqrt_z)) / numpy.sqrt(z**3)
        f = 1.0 - (x**2 / self.r0_) * C
        g = delta_t - x**3 / SQRT_EARTH_MU * S
        self.r = f * self.r0 + g * self.v0
        r_ = numpy.linalg.norm(self.r)
        g_dot = 1.0 - x**2 / r_ * C
        f_dot = SQRT_EARTH_MU / (self.r0_ * r_) * x * (z * S - 1.0)
        self.v = f_dot * self.r0 + g_dot * self.v0

        if self.record_trajectory:
            self.trajectory.append(self.r)

        if numpy.linalg.norm(self.r) < EARTH_R:
            self.v = numpy.array((0.0, 0.0, 0.0))
            self.collided_time = t

    def prograde(self):
        """Returns a unit vector in the prograde direction, ie. normalize(self.v)."""
        return self.v / numpy.linalg.norm(self.v)

    def retrograde(self):
        """Returns a unit vector in the retrograde direction, ie. normalize(-self.v)."""
        return -self.prograde()

    def orbit_normal(self):
        """Returns a unit vector in the orbit normal direction, ie. normalize(self.r x self.v)."""
        rxv = numpy.cross(self.r, self.v)
        return rxv / numpy.linalg.norm(rxv)

    def orbit_antinormal(self):
        return -self.orbit_normal()

    @staticmethod
    def generate_circular_equatorial_orbit(alt, orbit_color=(1.0, 1.0, 0.0, 1.0)):
        # Generates a circular equatorial orbit at the given altitude.
        # For circular orbits, v = sqrt(gamma/r)
        r = (EARTH_R + alt, 0.0, 0.0)
        r_ = numpy.linalg.norm(r)
        v = (0.0, numpy.sqrt(EARTH_MU / r_), 0.0)
        body = Body(r, v, 0.0, orbit_color)
        return Body(body.r, body.v, 0.0, orbit_color)

    @staticmethod
    def generate_random_orbit():
        import random
        rho = random.uniform(EARTH_R + 200.0, 2 * EARTH_R + 200)
        azimuth = random.uniform(0.0, 2.0 * numpy.pi)
        # We don't want orbits with more than 45 degrees inclination
        elevation = random.uniform(-numpy.pi / 4.0, numpy.pi / 4.0)
        x = rho * numpy.cos(elevation) * numpy.cos(azimuth)
        y = rho * numpy.cos(elevation) * numpy.sin(azimuth)
        z = rho * numpy.sin(elevation)

        r = numpy.array((x, y, z))
        z_axis = numpy.array((0.0, 0.0, -rho))
        v_unit = numpy.cross(r, z_axis)
        v_unit /= numpy.linalg.norm(v_unit)
        circular_velocity = numpy.sqrt(EARTH_MU / rho)
        velocity = random.uniform(1.0, 1.2) * circular_velocity
        v = v_unit * velocity

        def random_color():
            return 0.50 + random.randint(0, 2) * 0.25
        color = (random_color(), random_color(), random_color(), 1.0)
        stipple = random.choice((None, 0b0101010101010101, 0b0110011001100110))
        body = Body(r, v, 0.0, color, stipple)
        body.calc_state_vectors(random.uniform(-3600.0, 3600.0))
        return Body(body.r, body.v, 0.0, color, stipple)
