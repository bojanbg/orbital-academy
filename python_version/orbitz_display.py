from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import numpy

import wx
from wx.glcanvas import GLCanvas, GLContext

import vecmath
from body import Body, EARTH_R

class OrbitzGLCanvas(GLCanvas):

    def __init__(self, parent, scene):
        GLCanvas.__init__(self, parent, -1, size=(1024, 1024), 
                          attribList=(wx.glcanvas.WX_GL_RGBA, wx.glcanvas.WX_GL_DOUBLEBUFFER, 0, wx.glcanvas.WX_GL_DEPTH_SIZE, 32, 0))
        self.context = GLContext(self)
        self.SetCurrent(self.context)
        self.context_initialized = False
        
        self.scene = scene
        self.projection_matrix = None

        self.rotate = False
        self.beginx = 0.0; self.beginy = 0.0
        self.camera_up = (0.0, 1.0, 0.0); self.camera_right = (1.0, 0.0, 0.0)
        self.camera_vector = (0.0, 0.0, 6 * EARTH_R)

        wx.EVT_SIZE(self, self.OnSize)
        wx.EVT_PAINT(self, self.OnPaint)
        wx.EVT_RIGHT_DOWN(self, self.OnMouseMDown)
        wx.EVT_RIGHT_UP(self, self.OnMouseMUp)
        wx.EVT_MOUSEWHEEL(self, self.OnMouseWheel)
        wx.EVT_MOTION(self, self.OnMouseMotion)
        wx.EVT_ERASE_BACKGROUND(self, self.OnEraseBackground)

        self.OnSize(None)  #Set up initial viewport size
        glutInit()  #Initialize GLUT

    def OnSize(self, evt):
        self.w, self.h = self.GetClientSize()
        glViewport(0, 0, self.w, self.h) #Change viewport size
        if evt is not None:
            self.Update()
            self.Refresh()

    def OnPaint(self, event):
        dc = wx.PaintDC(self)
        self.SetCurrent(self.context)
        clear_and_setup_scene(self)
        draw_scene(self)
        self.SwapBuffers()  #Works even if we don't have double buffering enabled; does glFlush() automatically

    def OnMouseMDown(self, event):
        self.beginx, self.beginy = event.GetX(), event.GetY()
        self.rotate = True

    def OnMouseMUp(self, event):
        self.rotate = False

    def OnMouseMotion(self, event):
        if self.rotate:
            dx = event.GetX() - self.beginx; dy = event.GetY() - self.beginy
            self.rotate_camera(-dx / 2.0, -dy / 2.0)
            self.beginx, self.beginy = event.GetX(), event.GetY()
            self.Refresh()

    def OnMouseWheel(self, event):
        if event.GetWheelRotation() < 0:
            self.camera_vector = vecmath.scale_vector(self.camera_vector, 1.05)
            self.Refresh()
        else:
            self.camera_vector = vecmath.scale_vector(self.camera_vector, 1.0 / 1.05)
            self.Refresh()

    def OnEraseBackground(self, event):
        """If not defined to do nothing, Wx will cause horrible flickering on Windows as it will erase the area before each OpenGL redraw."""
        pass

    def rotate_camera(self, lr_angle, ud_angle):
        if abs(lr_angle) > 0:
            self.camera_right = vecmath.normalize_vec(vecmath.rotate_vec(self.camera_right, self.camera_up, lr_angle))
            self.camera_vector = vecmath.rotate_vec(self.camera_vector, self.camera_up, lr_angle)
        if abs(ud_angle) > 0:
            self.camera_up = vecmath.normalize_vec(vecmath.rotate_vec(self.camera_up, self.camera_right, ud_angle))
            self.camera_vector = vecmath.rotate_vec(self.camera_vector, self.camera_right, ud_angle)


def load_texture(filename):
    texture_image = wx.Image(filename, wx.BITMAP_TYPE_ANY, -1)
    texture_w, texture_h = texture_image.GetWidth(), texture_image.GetHeight()
    texture_data = texture_image.GetData()
    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    #glPixelStorei(GL_UNPACK_ROW_LENGTH, 0)
    #glPixelStorei(GL_UNPACK_ALIGNMENT, 2)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, texture_w, texture_h, 0, GL_RGB, GL_UNSIGNED_BYTE, texture_data)
    return texture_id


def clear_and_setup_scene(glcanvas):
    #First we clear the color and depth buffer.
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    #Then we set up the projection and view matrices.
    glMatrixMode(GL_PROJECTION); glLoadIdentity()
    camera_distance = vecmath.magnitude(glcanvas.camera_vector)
    gluPerspective(40.0, 1.0 * glcanvas.w / glcanvas.h, camera_distance / 10.0, 2.0 * camera_distance)

    # Save projection matrix for later use with gluProject
    glcanvas.projection_matrix = glGetDoublev(GL_PROJECTION_MATRIX)

    # The view matrix represents a camera looking at origin (our coordinate system is conviniently centered
    # at the planet center) from camera_distance away.
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(glcanvas.camera_vector[0], glcanvas.camera_vector[1], glcanvas.camera_vector[2], 
                  0.0, 0.0, 0.0,
                  glcanvas.camera_up[0], glcanvas.camera_up[1], glcanvas.camera_up[2])


def draw_scene(glcanvas):
    glEnable(GL_CULL_FACE)
    glEnable(GL_DEPTH_TEST)

    draw_orbits(glcanvas)
    draw_orbit_symbology(glcanvas)
    draw_planet(glcanvas, True)
    draw_info(glcanvas)


def draw_orbits(glcanvas):

    def draw_orbit(glcanvas, body):
        """Orbital parameters:
        a = semi-major axis
        e = eccentricity [0, +inf)
        w = argument of periapsis [0 deg, 360 deg)
        i = inclination [0 deg, 180 deg)
        o = longitude of ascending node [0 deg, 360 deg)
        """
        squash = numpy.sqrt(1.0 - body.e**2) #b/a = 1-flattening = sqrt(1-ec^2) b = a * sqrt(1-e^2)

        glPushMatrix()
        glRotatef(body.o, 0.0, 0.0, 1.0) #Rotate the ascening node
        glRotatef(body.i, 1.0, 0.0, 0.0) #Rotate to the right inclination
        glRotatef(body.w, 0.0, 0.0, 1.0) #Rotate the periapsis point
        glTranslatef(-body.a * body.e, 0.0, 0.0) #Set orbited body in focus
        glScalef(1.0, squash, 1.0) #Set eccentricity

        quadric = gluNewQuadric()
        gluQuadricDrawStyle(quadric, GLU_LINE)

        #Draw the orbit as an ellipse of the given color
        glColor4f(*body.orbit_color)
        if body.stipple is not None:
            glEnable(GL_LINE_STIPPLE)
            glLineStipple(1, body.stipple)
        else:
            glDisable(GL_LINE_STIPPLE)
        gluDisk(quadric, body.a, body.a, 360, 1)
        gluDeleteQuadric(quadric)
        glDisable(GL_LINE_STIPPLE)

        #Save modelview matrix for drawign orbital symbology via gluProject
        body.modelview_matrix = glGetDoublev(GL_MODELVIEW_MATRIX)

        glPopMatrix()

    def draw_radius_vector(glcanvas, body):
        glColor4f(*body.orbit_color)
        glBegin(GL_LINES)
        glVertex3f(0.0, 0.0, 0.0)
        glVertex3f(*body.r)
        glEnd()

    for body in glcanvas.scene.bodies:
        if body.orbit_viz_mode != Body.ORBIT_VISUALISATIONS['none']:
            draw_orbit(glcanvas, body)
        if body.pos_viz_mode == Body.POSITION_VISUALISATIONS['rv']:
            draw_radius_vector(glcanvas, body)


def draw_orbit_symbology(glcanvas):

    def draw_symbology(glcanvas, world_matrix, body):
        #Draw body orbital position (rhombus)
        x, y, z =  gluProject(body.r[0], body.r[1], body.r[2], world_matrix, glcanvas.projection_matrix)
        x  = int(x); y = int(y)
        if body.pos_viz_mode == Body.POSITION_VISUALISATIONS['symbol']:
            glColor4f(0.0, 1.0, 0.0, 1.0)
            glPushMatrix()
            glTranslate(x + 0.5, y + 0.5, z * (1.0 - 1.0E-12))
            #Position (rhombus with central point)
            glBegin(GL_POINTS); glVertex(0, 0); glEnd()
            glBegin(GL_LINE_LOOP)
            glVertex(3, 0); glVertex(0, 3); glVertex(-3, 0); glVertex(0, -3)
            glEnd()
            glPopMatrix()
        elif body.pos_viz_mode == Body.POSITION_VISUALISATIONS['dot']:
            glColor4f(*body.orbit_color)
            glPushMatrix()
            glTranslate(x + 0.5, y + 0.5, z * (1.0 - 1.0E-12))
            glBegin(GL_POINTS); glVertex(0, 0); glEnd()
            glPopMatrix()

        if body.orbit_viz_mode == Body.ORBIT_VISUALISATIONS['all']:
            #Draw apsides (full circle for periapsis, empty circle for apoapsis)
            xp, yp, zp =  gluProject(body.a, 0.0, 0.0, body.modelview_matrix, glcanvas.projection_matrix)
            xa, ya, za =  gluProject(-body.a, 0.0, 0.0, body.modelview_matrix, glcanvas.projection_matrix)
            xp = int(xp); yp = int(yp); xa = int(xa); ya = int(ya)
            quadric = gluNewQuadric()
            glColor4f(0.0, 1.0, 0.0, 1.0)
            glPushMatrix()
            glTranslate(xp + 0.5, yp + 0.5, zp * (1.0 - 1.0E-12))
            gluQuadricDrawStyle(quadric, GLU_LINE)
            gluDisk(quadric, 2.0, 2.0, 8, 1)
            glPopMatrix()
            glPushMatrix()
            glTranslate(xa + 0.5, ya + 0.5, za * (1.0 - 1.0E-12))
            gluQuadricDrawStyle(quadric, GLU_FILL)
            gluDisk(quadric, 0.0, 2.5, 8, 1)
            glPopMatrix()
            gluDeleteQuadric(quadric)

    #Save world matrix for drawing orbital positions (as they are defined in world space)
    world_matrix = glGetDoublev(GL_MODELVIEW_MATRIX)
    #Set up 2D projection for drawing symbology
    glMatrixMode(GL_PROJECTION); glPushMatrix(); glLoadIdentity()
    glOrtho(0.0, glcanvas.w, 0.0, glcanvas.h, 0.0, -1.0)  #Stupid @#$%! far plane value needs to be negated!
    glMatrixMode(GL_MODELVIEW); glPushMatrix(); glLoadIdentity()

    #Draw symbology
    for body in glcanvas.scene.bodies:
        draw_symbology(glcanvas, world_matrix, body)

    #Restore matrices to previous 3D projection (as we still need to draw some objects in 3D space)
    glMatrixMode(GL_PROJECTION); glPopMatrix()
    glMatrixMode(GL_MODELVIEW); glPopMatrix()


def draw_planet(glcanvas, atmosphere=True):
    glBegin(GL_LINES)
    #North vector
    glColor4f(1.0, 0.0, 0.0, 1.0)
    glVertex3f(0.0, 0.0, EARTH_R)
    glVertex3f(0.0, 0.0, 1.25 * EARTH_R)
    #vernal equinox
    glColor4f(0.0, 0.5, 0.0, 1.0)
    glVertex3f(EARTH_R, 0.0, 0.0)
    glVertex3f(1.25 * EARTH_R, 0.0, 0.0)
    glEnd()

    #We can only load textures after GLContext has been initialized, ie. here
    if not glcanvas.context_initialized:
        glcanvas.context_initialized = True
        load_texture('earth.png')

    #We temporarily change OpenGL state as we are drawing a transparent object
    glPushAttrib(GL_ENABLE_BIT)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glDepthMask(False)
    glEnable(GL_TEXTURE_2D)
    #glBindTexture(GL_TEXTURE_2D, 0) #Should be using texture_id but for now we only have one texture
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
    glColor(1.0, 1.0, 1.0, 0.85)
    quad = gluNewQuadric()
    gluQuadricTexture(quad, GLU_TRUE)
    gluSphere(quad, EARTH_R, 128, 128)
    glDisable(GL_TEXTURE_2D)
    gluDeleteQuadric(quad)    

    if atmosphere:
        glColor4f(0.5, 0.5, 0.8, 0.25)
        quad = gluNewQuadric()
        gluSphere(quad, EARTH_R * 1.02, 128, 128)
        gluDeleteQuadric(quad)

    glPopAttrib()
    glDepthMask(True)


def draw_info(glcanvas):

    def gl_print(x, row, text):
        glRasterPos(x, glcanvas.h - 13 * (row + 1))
        for char in text:
            glutBitmapCharacter(GLUT_BITMAP_8_BY_13, ord(char))

    #Reset projection and modelview matrices to a simple 2D projection
    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    gluOrtho2D(0.0, glcanvas.w, 0.0, glcanvas.h);
    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();
    current_body =  glcanvas.scene.current_body()
    glColor4f(*current_body.orbit_color) #N.B. glRasterPos fixes the currently active color so text color must be set BEFORE calling it

    #Orbital parameters
    gl_print(4, 0, 'Body: %i' % glcanvas.scene.selected_body)
    gl_print(4, 1, 'a: %f m' % current_body.a)
    gl_print(4, 2, 'e: %f' % current_body.e)
    gl_print(4, 3, 'w: %f deg' % current_body.w)
    gl_print(4, 4, 'i: %f deg' % current_body.i)
    gl_print(4, 5, 'o: %f deg' % current_body.o)
    gl_print(4, 6, 'ni: %f deg' % current_body.ni)
    gl_print(4, 7, 'T: %f s' % current_body.T)
    gl_print(4, 8, 'Pr: %f m' % current_body.rp)
    gl_print(4, 9, 'Ar: %f m' % current_body.ra)
    gl_print(4, 10, 'Ph: %f m' % (current_body.rp - EARTH_R))
    gl_print(4, 11, 'Ah: %f m' % (current_body.ra - EARTH_R))
    gl_print(4, 12, 't_step: %f' % glcanvas.scene.time_step)
    gl_print(4, 13, 't: %f s' % glcanvas.scene.time)

    #Instantaneous parameters
    xright = glcanvas.w - 200
    gl_print(xright, 0, 'x: %f m' % current_body.r[0])
    gl_print(xright, 1, 'y: %f m' % current_body.r[1])
    gl_print(xright, 2, 'z: %f m' % current_body.r[2])
    gl_print(xright, 3, 'r: %f m' % numpy.sqrt(numpy.vdot(current_body.r, current_body.r)))
    gl_print(xright, 4, 'vx: %f m/s' % current_body.v[0])
    gl_print(xright, 5, 'vy: %f m/s' % current_body.v[1])
    gl_print(xright, 6, 'vz: %f m/s' % current_body.v[2])
    gl_print(xright, 7, 'v: %f m/s' % numpy.sqrt(numpy.vdot(current_body.v, current_body.v)))
