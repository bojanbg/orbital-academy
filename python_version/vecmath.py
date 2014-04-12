import math
import numpy


def rotate_vec(v, r, a):
    """Rotates vector v around vector r a degrees."""
    r = normalize_vec(r)  # Rotation axis vector needs to be normalized
    # The formula seems to be for a left-handed coordinate system, so we negate the angle to get a right-handed rotation
    a_rad = math.radians(-a)
    cosa = math.cos(a_rad); sina = math.sin(a_rad); mincosa = (1.0 - cosa)
    rot_matrix = numpy.array([
        [cosa + r[0] * r[0] * mincosa, r[0] * r[1] * mincosa - r[2] * sina, r[0] * r[2] * mincosa + r[1] * sina],
        [r[1] * r[0] * mincosa + r[2] * sina, cosa + r[1] * r[1] * mincosa, r[1] * r[2] * mincosa - r[0] * sina],
        [r[2] * r[0] * mincosa - r[1] * sina, r[2] * r[1] * mincosa + r[0] * sina, cosa + r[2] * r[2] * mincosa]])
    return numpy.dot(v, rot_matrix)
    

def normalize_vec(v):
    n = numpy.linalg.norm(v)
    return 0.0 if n == 0.0 else v / numpy.linalg.norm(v)


def scale_vector(v, s):
    return v[0] * s, v[1] * s, v[2] * s


def magnitude(v):
    return numpy.linalg.norm(v)
