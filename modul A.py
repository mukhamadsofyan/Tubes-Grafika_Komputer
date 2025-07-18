from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys, math

width, height = 800, 600

objects = []
click_points = []
window_bounds = []
drawing_type = 'point'
last_drawing_type = 'line'
current_color = (1.0, 1.0, 1.0)
current_thickness = 2
selected_object = -1
transform_mode = None
moving = False
last_mouse_pos = (0, 0)
current_mouse_pos = None

mode_geser_window = False
dragging_window = False
snap_to_grid = False
grid_size = 0.05
show_shortcuts = True

def normalize(x, y):
    return (x / width * 2 - 1, -(y / height * 2 - 1))

def snap_point(p):
    if not snap_to_grid: return p
    x = round(p[0] / grid_size) * grid_size
    y = round(p[1] / grid_size) * grid_size
    return (x, y)

def is_inside_window(p):
    if len(window_bounds) < 2: return False
    x1, y1 = window_bounds[0]
    x2, y2 = window_bounds[1]
    return min(x1,x2) <= p[0] <= max(x1,x2) and min(y1,y2) <= p[1] <= max(y1,y2)

def distance(p1, p2):
    return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

def find_nearest_object(p):
    min_dist = float('inf')
    idx = -1
    for i, obj in enumerate(objects):
        center = get_object_center(obj)
        d = distance(p, center)
        if d < min_dist and d < 0.3:
            min_dist = d
            idx = i
    return idx

def get_object_center(obj):
    xs = [p[0] for p in obj['points']]
    ys = [p[1] for p in obj['points']]
    return (sum(xs)/len(xs), sum(ys)/len(ys))

def translate(obj, dx, dy):
    obj['points'] = [(x+dx, y+dy) for x,y in obj['points']]

def rotate(obj, angle):
    cx, cy = get_object_center(obj)
    result = []
    for x,y in obj['points']:
        dx, dy = x-cx, y-cy
        x_new = dx * math.cos(angle) - dy * math.sin(angle)
        y_new = dx * math.sin(angle) + dy * math.cos(angle)
        result.append((cx + x_new, cy + y_new))
    obj['points'] = result

def scale(obj, factor):
    cx, cy = get_object_center(obj)
    obj['points'] = [(cx+(x-cx)*factor, cy+(y-cy)*factor) for x,y in obj['points']]

def draw_text(x, y, text):
    glColor3f(1,1,1)
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_12, ord(ch))

def draw_shortcuts():
    lines = [
        "[1] Point  [2] Line  [3] Square  [4] Ellipse  [W] Set Window  [Q] Back from Window",
        "[T] Translate  [O] Rotate  [S] Scale  [U] Zoom Out  [I] Zoom In",
        "[R] Red  [G] Green  [B] Blue  [+/-] Thickness",
        "[M] Toggle Move Window  [G] Toggle Snap Grid  [X] Reset Window",
        "[Z] Undo  [D] Delete Selected  [H] Toggle Help"
    ]
    for i, line in enumerate(lines):
        draw_text(-0.95, -0.95 + i * 0.06, line)

def cohen_sutherland_clip(p1,p2):
    INSIDE, LEFT, RIGHT, BOTTOM, TOP = 0,1,2,4,8
    def code(x,y):
        c = INSIDE
        x1,x2 = sorted([window_bounds[0][0], window_bounds[1][0]])
        y1,y2 = sorted([window_bounds[0][1], window_bounds[1][1]])
        if x < x1: c |= LEFT
        elif x > x2: c |= RIGHT
        if y < y1: c |= BOTTOM
        elif y > y2: c |= TOP
        return c

    x1,y1 = p1
    x2,y2 = p2
    c1, c2 = code(x1,y1), code(x2,y2)

    while True:
        if not (c1 | c2): return [(x1,y1),(x2,y2)]
        elif c1 & c2: return None
        out = c1 if c1 else c2
        xb, xt = sorted([window_bounds[0][0], window_bounds[1][0]])
        yb, yt = sorted([window_bounds[0][1], window_bounds[1][1]])
        if out & TOP:
            x = x1 + (x2-x1)*(yt-y1)/(y2-y1)
            y = yt
        elif out & BOTTOM:
            x = x1 + (x2-x1)*(yb-y1)/(y2-y1)
            y = yb
        elif out & RIGHT:
            y = y1 + (y2-y1)*(xt-x1)/(x2-x1)
            x = xt
        elif out & LEFT:
            y = y1 + (y2-y1)*(xb-x1)/(x2-x1)
            x = xb
        if out == c1:
            x1, y1 = x, y
            c1 = code(x1,y1)
        else:
            x2, y2 = x, y
            c2 = code(x2,y2)

def draw_object(obj):
    is_selected = selected_object != -1 and objects[selected_object] == obj
    glColor3f(*(1,1,0) if is_selected else obj['color'])
    glLineWidth(obj['thickness']*2 if is_selected else obj['thickness'])

    if obj['type'] == 'point':
        p = obj['points'][0]
        if len(window_bounds)==2 and not is_inside_window(p): return
        if is_inside_window(p): glColor3f(0,1,0)
        glPointSize(obj['thickness'] * 2)
        glBegin(GL_POINTS); glVertex2f(*p); glEnd()

    elif obj['type'] == 'line':
        p1, p2 = obj['points']
        if len(window_bounds)==2:
            clipped = cohen_sutherland_clip(p1, p2)
            if clipped:
                if is_inside_window(clipped[0]) and is_inside_window(clipped[1]):
                    glColor3f(0,1,0)
                glBegin(GL_LINES)
                glVertex2f(*clipped[0]); glVertex2f(*clipped[1])
                glEnd()
        else:
            glBegin(GL_LINES)
            glVertex2f(*p1); glVertex2f(*p2)
            glEnd()

    elif obj['type'] == 'square':
        p1, p2 = obj['points']
        corners = [(p1[0],p1[1]), (p2[0],p1[1]), (p2[0],p2[1]), (p1[0],p2[1])]
        for i in range(4):
            a, b = corners[i], corners[(i+1)%4]
            if len(window_bounds)==2:
                clipped = cohen_sutherland_clip(a,b)
                if not clipped: continue
                if is_inside_window(clipped[0]) and is_inside_window(clipped[1]):
                    glColor3f(0,1,0)
                glBegin(GL_LINES); glVertex2f(*clipped[0]); glVertex2f(*clipped[1]); glEnd()
            else:
                glBegin(GL_LINES); glVertex2f(*a); glVertex2f(*b); glEnd()

    elif obj['type'] == 'ellipse':
        c, e = obj['points']
        rx = abs(e[0] - c[0])
        ry = abs(e[1] - c[1])
        seg = 100
        pts = [(c[0]+rx*math.cos(t), c[1]+ry*math.sin(t)) for t in [2*math.pi*i/seg for i in range(seg+1)]]
        for i in range(len(pts)-1):
            a, b = pts[i], pts[i+1]
            if len(window_bounds)==2:
                clipped = cohen_sutherland_clip(a,b)
                if not clipped: continue
                if is_inside_window(clipped[0]) and is_inside_window(clipped[1]):
                    glColor3f(0,1,0)
                glBegin(GL_LINES); glVertex2f(*clipped[0]); glVertex2f(*clipped[1]); glEnd()
            else:
                glBegin(GL_LINES); glVertex2f(*a); glVertex2f(*b); glEnd()

def display():
    glClear(GL_COLOR_BUFFER_BIT)
    for obj in objects:
        draw_object(obj)

    if len(click_points)==1 and current_mouse_pos and drawing_type in ['line','square','ellipse']:
        preview = {
            'type': drawing_type,
            'points': [click_points[0], current_mouse_pos],
            'color': (0.5,0.5,0.5),
            'thickness': current_thickness
        }
        draw_object(preview)

    if len(window_bounds) == 2:
        glColor3f(1,1,0)
        glLineWidth(1)
        x1,y1 = window_bounds[0]
        x2,y2 = window_bounds[1]
        glBegin(GL_LINE_LOOP)
        glVertex2f(x1,y1); glVertex2f(x2,y1); glVertex2f(x2,y2); glVertex2f(x1,y2)
        glEnd()
        draw_text(-0.95, 0.74, f"Window: ({min(x1,x2):.2f},{min(y1,y2):.2f}) → ({max(x1,x2):.2f},{max(y1,y2):.2f})")

    draw_text(-0.95, 0.92, f"Mode: {drawing_type.upper()} | Transform: {transform_mode or '-'}")
    draw_text(-0.95, 0.86, "[H] Show/Hide Shortcut")

    if mode_geser_window: draw_text(-0.95, 0.80, "MoveWin: ON")
    if snap_to_grid: draw_text(-0.95, 0.68, "Snap Grid: ON")
    if show_shortcuts: draw_shortcuts()
    glutSwapBuffers()

def mouse(button, state, x, y):
    global click_points, selected_object, moving, last_mouse_pos
    global dragging_window, current_mouse_pos

    norm = normalize(x,y)
    point = snap_point(norm)

    if button == GLUT_LEFT_BUTTON:
        if state == GLUT_DOWN:
            if mode_geser_window and len(window_bounds)==2:
                x1,y1 = window_bounds[0]
                x2,y2 = window_bounds[1]
                if min(x1,x2)<=point[0]<=max(x1,x2) and min(y1,y2)<=point[1]<=max(y1,y2):
                    dragging_window = True
                    last_mouse_pos = point
                    return
            if transform_mode == 'translate':
                idx = find_nearest_object(point)
                if idx != -1:
                    selected_object = idx
                    moving = True
                    last_mouse_pos = point
            else:
                click_points.append(point)
                if drawing_type == 'window' and len(click_points) == 2:
                    window_bounds.clear()
                    window_bounds.extend(click_points)
                    click_points.clear()
                elif drawing_type == 'point':
                    objects.append({'type': 'point', 'points':[point], 'color': current_color, 'thickness': current_thickness})
                elif drawing_type in ['line','square','ellipse'] and len(click_points)==2:
                    objects.append({'type': drawing_type, 'points': click_points[:], 'color': current_color, 'thickness': current_thickness})
                    click_points.clear()
                    current_mouse_pos = None
        elif state == GLUT_UP:
            moving = False
            dragging_window = False
    glutPostRedisplay()

def motion(x,y):
    global last_mouse_pos, current_mouse_pos
    norm = normalize(x,y)
    current_mouse_pos = snap_point(norm)

    if dragging_window and len(window_bounds)==2:
        dx = norm[0] - last_mouse_pos[0]
        dy = norm[1] - last_mouse_pos[1]
        window_bounds[0] = (window_bounds[0][0]+dx, window_bounds[0][1]+dy)
        window_bounds[1] = (window_bounds[1][0]+dx, window_bounds[1][1]+dy)
        last_mouse_pos = norm
    elif moving and selected_object != -1:
        dx = norm[0] - last_mouse_pos[0]
        dy = norm[1] - last_mouse_pos[1]
        translate(objects[selected_object], dx, dy)
        last_mouse_pos = norm
    glutPostRedisplay()

def keyboard(key, x, y):
    global drawing_type, current_color, current_thickness, transform_mode
    global selected_object, click_points, mode_geser_window, snap_to_grid, last_drawing_type, show_shortcuts

    if key == b'1': drawing_type = last_drawing_type = 'point'
    elif key == b'2': drawing_type = last_drawing_type = 'line'
    elif key == b'3': drawing_type = last_drawing_type = 'square'
    elif key == b'4': drawing_type = last_drawing_type = 'ellipse'
    elif key == b'w': last_drawing_type = drawing_type; drawing_type = 'window'
    elif key == b'q': drawing_type = last_drawing_type; window_bounds.clear()
    elif key == b'r': current_color = (1,0,0)
    elif key == b'g': current_color = (0,1,0)
    elif key == b'b': current_color = (0,0,1)
    elif key in [b'+', b'=']: current_thickness += 1
    elif key in [b'-', b'_']: current_thickness = max(1, current_thickness - 1)
    elif key == b't': transform_mode = 'translate'
    elif key == b'o': transform_mode = 'rotate'
    elif key == b's': transform_mode = 'scale'
    elif key == b'u' and objects:  # Zoom Out
        target = objects[selected_object] if selected_object != -1 else objects[-1]
        if transform_mode == 'translate': translate(target, 0.1, 0.1)
        elif transform_mode == 'rotate': rotate(target, math.radians(15))
        elif transform_mode == 'scale': scale(target, 1.2)
    elif key == b'i' and objects:  # Zoom In
        target = objects[selected_object] if selected_object != -1 else objects[-1]
        scale(target, 0.8)
    elif key == b'd' and selected_object != -1: del objects[selected_object]; selected_object = -1
    elif key == b'z' and objects: objects.pop(); selected_object = -1
    elif key == b'm': mode_geser_window = not mode_geser_window
    elif key == b'G': snap_to_grid = not snap_to_grid
    elif key == b'x': window_bounds.clear()
    elif key == b'h': show_shortcuts = not show_shortcuts
    if key in [b'1',b'2',b'3',b'4',b'w',b'q']: click_points.clear()
    glutPostRedisplay()

def reshape(w, h):
    global width, height
    width, height = w, h
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(-1, 1, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def init():
    glClearColor(0,0,0,1)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(-1,1,-1,1)

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(width, height)
    glutInitWindowPosition(100,100)
    glutCreateWindow(b'Grafkom - Final Program Modul A')
    init()
    glutDisplayFunc(display)
    glutMouseFunc(mouse)
    glutMotionFunc(motion)
    glutKeyboardFunc(keyboard)
    glutReshapeFunc(reshape)
    glutMainLoop()

main()
