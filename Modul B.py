from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys

# Variabel transformasi
angle_x = 0
angle_y = 0
distance = -7
trans_x = 0
trans_y = 0

# Status objek: 1 = cube, 2 = pyramid
current_object = 1

# Mouse
mouse_down = False
right_mouse_down = False
last_mouse_x = 0
last_mouse_y = 0

# Status tombol keyboard
key_states = {
    b'w': False, b's': False, b'a': False, b'd': False,
    b'z': False, b'x': False,
    b'i': False, b'k': False, b'j': False, b'l': False
}

def init():
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glShadeModel(GL_SMOOTH)

    ambient = [0.2, 0.2, 0.2, 1.0]
    diffuse = [0.7, 0.7, 0.7, 1.0]
    specular = [1.0, 1.0, 1.0, 1.0]
    position = [2.0, 2.0, 2.0, 1.0]

    glLightfv(GL_LIGHT0, GL_AMBIENT, ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, diffuse)
    glLightfv(GL_LIGHT0, GL_SPECULAR, specular)
    glLightfv(GL_LIGHT0, GL_POSITION, position)

    glMaterialfv(GL_FRONT, GL_SPECULAR, specular)
    glMateriali(GL_FRONT, GL_SHININESS, 50)

def draw_cube():
    glutSolidCube(2)

def draw_pyramid():
    glBegin(GL_TRIANGLES)
    # Muka depan
    glNormal3f(0, 0.5, 1)
    glVertex3f(0, 1, 0)
    glVertex3f(-1, -1, 1)
    glVertex3f(1, -1, 1)
    # Kanan
    glNormal3f(1, 0.5, 0)
    glVertex3f(0, 1, 0)
    glVertex3f(1, -1, 1)
    glVertex3f(1, -1, -1)
    # Belakang
    glNormal3f(0, 0.5, -1)
    glVertex3f(0, 1, 0)
    glVertex3f(1, -1, -1)
    glVertex3f(-1, -1, -1)
    # Kiri
    glNormal3f(-1, 0.5, 0)
    glVertex3f(0, 1, 0)
    glVertex3f(-1, -1, -1)
    glVertex3f(-1, -1, 1)
    glEnd()

    glBegin(GL_QUADS)
    glNormal3f(0, -1, 0)
    glVertex3f(-1, -1, 1)
    glVertex3f(1, -1, 1)
    glVertex3f(1, -1, -1)
    glVertex3f(-1, -1, -1)
    glEnd()

def draw_text(x, y, text):
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, 800, 0, 600)

    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glDisable(GL_LIGHTING)
    glColor3f(1, 1, 1)
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(GLUT_BITMAP_8_BY_13, ord(ch))
    glEnable(GL_LIGHTING)

    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def display():
    global angle_x, angle_y, distance, trans_x, trans_y, current_object
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    gluLookAt(0, 0, 5, 0, 0, 0, 0, 1, 0)

    glTranslatef(trans_x, trans_y, distance)
    glRotatef(angle_x, 1, 0, 0)
    glRotatef(angle_y, 0, 1, 0)

    if current_object == 1:
        draw_cube()
    elif current_object == 2:
        draw_pyramid()

    draw_text(10, 580, "Mouse Kiri + Drag : Rotasi")
    draw_text(10, 560, "Mouse Kanan + Drag: Translasi")
    draw_text(10, 540, "Scroll / Z X      : Zoom")
    draw_text(10, 520, "W A S D           : Rotasi Kamera")
    draw_text(10, 500, "I J K L           : Translasi Kamera")
    draw_text(10, 480, "1 / 2             : Ganti Objek (Kubus / Piramida)")
    draw_text(10, 460, "R                 : Reset Transformasi")

    glutSwapBuffers()

def reshape(w, h):
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60.0, float(w) / float(h), 1.0, 100.0)
    glMatrixMode(GL_MODELVIEW)

def keyboard(key, x, y):
    global current_object, angle_x, angle_y, distance, trans_x, trans_y
    if key in key_states:
        key_states[key] = True
    elif key == b'1':
        current_object = 1
    elif key == b'2':
        current_object = 2
    elif key == b'r':
        angle_x = angle_y = 0
        distance = -7
        trans_x = trans_y = 0

def keyboard_up(key, x, y):
    if key in key_states:
        key_states[key] = False

def mouse(button, state, x, y):
    global mouse_down, right_mouse_down, last_mouse_x, last_mouse_y, distance
    last_mouse_x = x
    last_mouse_y = y

    if button == GLUT_LEFT_BUTTON:
        mouse_down = (state == GLUT_DOWN)
    elif button == GLUT_RIGHT_BUTTON:
        right_mouse_down = (state == GLUT_DOWN)

    if state == GLUT_DOWN:
        if button == 3:
            distance += 0.5
        elif button == 4:
            distance -= 0.5
        glutPostRedisplay()

def motion(x, y):
    global angle_x, angle_y, trans_x, trans_y, last_mouse_x, last_mouse_y
    dx = x - last_mouse_x
    dy = y - last_mouse_y

    if mouse_down:
        angle_x += dy * 0.5
        angle_y += dx * 0.5
    elif right_mouse_down:
        trans_x += dx * 0.005
        trans_y -= dy * 0.005

    last_mouse_x = x
    last_mouse_y = y
    glutPostRedisplay()

def update(value):
    global angle_x, angle_y, distance, trans_x, trans_y
    if key_states[b'w']:
        angle_x -= 1
    if key_states[b's']:
        angle_x += 1
    if key_states[b'a']:
        angle_y -= 1
    if key_states[b'd']:
        angle_y += 1
    if key_states[b'z']:
        distance += 0.1
    if key_states[b'x']:
        distance -= 0.1
    if key_states[b'i']:
        trans_y += 0.05
    if key_states[b'k']:
        trans_y -= 0.05
    if key_states[b'j']:
        trans_x -= 0.05
    if key_states[b'l']:
        trans_x += 0.05

    glutPostRedisplay()
    glutTimerFunc(16, update, 0)

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(800, 600)
    glutCreateWindow(b'3Modul B - Grafkom')
    init()
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutKeyboardFunc(keyboard)
    glutKeyboardUpFunc(keyboard_up)
    glutMouseFunc(mouse)
    glutMotionFunc(motion)
    glutTimerFunc(0, update, 0)
    glutMainLoop()

main()
