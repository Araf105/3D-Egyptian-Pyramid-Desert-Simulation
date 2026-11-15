from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import math



WIDTH = 1000
HEIGHT = 700

paused = False
dragging = False
dragObject = ""
lastMouseX = 0
lastMouseY = 0

sunX = 7.0
sunY = 8.0
camelX = -4.0
camelZ = 2.0

cameraAngle = 0.0
cameraPitch = 15.0
cameraDistance = 24.0

targetAngle = 0.0
targetPitch = 15.0
targetDistance = 24.0

camelDirection = 1
camelSpeed = 0.025
legAngle = 0.0
cloudMove = 0.0




def drawCircle(radius):
    glBegin(GL_TRIANGLE_FAN)
    glVertex3f(0, 0, 0)

    for angle in range(361):
        a = math.radians(angle)
        glVertex3f(radius * math.cos(a), radius * math.sin(a), 0)

    glEnd()


def drawGround():
    
    glColor3f(0.78, 0.61, 0.38)
    glBegin(GL_QUADS)
    glNormal3f(0, 1, 0)
    glVertex3f(-35, 0, -35)
    glVertex3f(35, 0, -35)
    glVertex3f(35, 0, 35)
    glVertex3f(-35, 0, 35)
    glEnd()

    
    glDisable(GL_LIGHTING)
    glColor3f(0.69, 0.51, 0.31)
    glBegin(GL_LINES)
    for i in range(-30, 31, 3):
        glVertex3f(i, 0.015, -28)
        glVertex3f(i + 2, 0.015, 28)
    glEnd()
    glEnable(GL_LIGHTING)


def drawDune(x, z, width, height, depth):
    glPushMatrix()
    glTranslatef(x, 0, z)
    glColor3f(0.86, 0.68, 0.43)

   
    glBegin(GL_TRIANGLES)
    glNormal3f(0, 1, 0)
    glVertex3f(-width, 0, -depth)
    glVertex3f(width, 0, -depth)
    glVertex3f(0, height, 0)

    glVertex3f(width, 0, -depth)
    glVertex3f(width, 0, depth)
    glVertex3f(0, height, 0)

    glVertex3f(width, 0, depth)
    glVertex3f(-width, 0, depth)
    glVertex3f(0, height, 0)

    glVertex3f(-width, 0, depth)
    glVertex3f(-width, 0, -depth)
    glVertex3f(0, height, 0)
    glEnd()
    glPopMatrix()


def drawPyramid(x, z, size):
    glPushMatrix()
    glTranslatef(x, 0, z)

   
    glBegin(GL_TRIANGLES)

    glColor3f(0.91, 0.69, 0.36)
    glNormal3f(0, 0.6, 0.8)
    glVertex3f(-size, 0, size)
    glVertex3f(size, 0, size)
    glVertex3f(0, size * 1.55, 0)

    glColor3f(0.72, 0.48, 0.25)
    glNormal3f(0.8, 0.6, 0)
    glVertex3f(size, 0, size)
    glVertex3f(size, 0, -size)
    glVertex3f(0, size * 1.55, 0)

    glColor3f(0.83, 0.59, 0.30)
    glNormal3f(0, 0.6, -0.8)
    glVertex3f(size, 0, -size)
    glVertex3f(-size, 0, -size)
    glVertex3f(0, size * 1.55, 0)

    glColor3f(0.66, 0.42, 0.22)
    glNormal3f(-0.8, 0.6, 0)
    glVertex3f(-size, 0, -size)
    glVertex3f(-size, 0, size)
    glVertex3f(0, size * 1.55, 0)

    glEnd()
    glPopMatrix()


def drawSun():
    glDisable(GL_LIGHTING)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    glPushMatrix()
    glTranslatef(sunX, sunY, -5)

   
    glColor4f(1.0, 0.10, 0.005, 0.20)
    glPushMatrix()
    glScalef(2.0, 2.0, 2.0)
    glutSolidSphere(1.0, 28, 28)
    glPopMatrix()

   
    glColor4f(1.0, 0.22, 0.005, 0.28)
    glPushMatrix()
    glScalef(1.25, 1.25, 1.25)
    glutSolidSphere(1.0, 28, 28)
    glPopMatrix()

    
    glColor3f(1.0, 0.20, 0.015)
    glutSolidSphere(0.88, 36, 36)

    glPopMatrix()
    glDisable(GL_BLEND)
    glEnable(GL_LIGHTING)

def drawCloud(x, y, z, size):
    glDisable(GL_LIGHTING)
    glColor4f(1.0, 0.94, 0.82, 0.65)
    glPushMatrix()
    glTranslatef(x, y, z)
    glScalef(size, size * 0.45, size * 0.35)
    glutSolidSphere(1, 18, 18)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(x + size * 0.65, y + 0.15, z)
    glScalef(size * 0.75, size * 0.38, size * 0.30)
    glutSolidSphere(1, 18, 18)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(x - size * 0.60, y + 0.08, z)
    glScalef(size * 0.70, size * 0.35, size * 0.28)
    glutSolidSphere(1, 18, 18)
    glPopMatrix()
    glEnable(GL_LIGHTING)


def drawPalmTree(x, z, height):
    glPushMatrix()
    glTranslatef(x, 0, z)

   
    glColor3f(0.40, 0.23, 0.12)
    glPushMatrix()
    glTranslatef(0, height / 2, 0)
    glScalef(0.28, height, 0.28)
    glutSolidCube(1)
    glPopMatrix()

    
    glColor3f(0.16, 0.38, 0.17)
    glBegin(GL_TRIANGLES)
    for angle in range(0, 360, 45):
        a = math.radians(angle)
        glVertex3f(0, height, 0)
        glVertex3f(1.35 * math.cos(a), height + 0.35, 1.35 * math.sin(a))
        glVertex3f(0.35 * math.cos(a + 0.5), height - 0.10,
                   0.35 * math.sin(a + 0.5))
    glEnd()

    glPopMatrix()


def drawSphinx():
    glPushMatrix()
    glTranslatef(-8, 0, 1)

    
    glColor3f(0.72, 0.52, 0.31)
    glPushMatrix()
    glTranslatef(0, 0.75, 0)
    glScalef(2.4, 0.75, 0.85)
    glutSolidCube(1)
    glPopMatrix()

    
    glColor3f(0.83, 0.64, 0.41)
    glPushMatrix()
    glTranslatef(1.05, 1.45, 0)
    glutSolidSphere(0.48, 24, 24)
    glPopMatrix()

    
    glColor3f(0.65, 0.45, 0.27)
    for z in (-0.42, 0.42):
        glPushMatrix()
        glTranslatef(0.95, 0.25, z)
        glScalef(1.35, 0.28, 0.25)
        glutSolidCube(1)
        glPopMatrix()

    glPopMatrix()


def drawCamel():
    glPushMatrix()
    glTranslatef(camelX, 0, camelZ)

    
    glColor3f(0.62, 0.36, 0.16)
    glPushMatrix()
    glTranslatef(0, 1.05, 0)
    glScalef(1.65, 0.78, 0.62)
    glutSolidCube(1)
    glPopMatrix()

    
    glColor3f(0.72, 0.44, 0.21)
    glPushMatrix()
    glTranslatef(-0.10, 1.68, 0)
    glScalef(0.48, 0.68, 0.48)
    glutSolidSphere(1, 20, 20)
    glPopMatrix()

    
    glColor3f(0.62, 0.36, 0.16)
    glPushMatrix()
    glTranslatef(0.63, 1.68, 0)
    glRotatef(-18, 0, 0, 1)
    glScalef(0.24, 0.92, 0.24)
    glutSolidCube(1)
    glPopMatrix()

    
    glPushMatrix()
    glTranslatef(0.92, 2.22, 0)
    glutSolidSphere(0.30, 20, 20)
    glPopMatrix()

    
    glColor3f(0.48, 0.27, 0.13)
    for i, x in enumerate((-0.52, 0.52)):
        for j, z in enumerate((-0.25, 0.25)):
            glPushMatrix()
            glTranslatef(x, 0.82, z)
            if (i + j) % 2 == 0:
                glRotatef(legAngle, 1, 0, 0)
            else:
                glRotatef(-legAngle, 1, 0, 0)
            glTranslatef(0, -0.40, 0)
            glScalef(0.17, 0.85, 0.17)
            glutSolidCube(1)
            glPopMatrix()

    glPopMatrix()


def drawShadow(x, z, sx, sz):
    
    glDisable(GL_LIGHTING)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glColor4f(0.18, 0.12, 0.08, 0.30)

    glPushMatrix()
    glTranslatef(x, 0.035, z)
    glRotatef(-90, 1, 0, 0)
    glScalef(sx, sz, 1)
    drawCircle(1)
    glPopMatrix()

    glDisable(GL_BLEND)
    glEnable(GL_LIGHTING)




def main():
    drawGround()

    
    drawDune(-15, -9, 8, 2.2, 5)
    drawDune(14, -10, 9, 2.6, 6)

    
    drawPyramid(-5, -7, 3.2)
    drawPyramid(2, -10, 4.3)
    drawPyramid(10, -7, 2.7)

    
    drawPalmTree(-13, 0, 3.4)
    drawPalmTree(13, 1, 3.0)
    drawSphinx()

    
    drawCloud(-7 + cloudMove, 10, -8, 1.4)
    drawCloud(4 + cloudMove, 11, -10, 1.1)

    
    drawShadow(-5, -7, 3.2, 1.6)
    drawShadow(2, -10, 4.3, 2.1)
    drawShadow(10, -7, 2.7, 1.4)
    drawShadow(camelX, camelZ, 1.25, 0.60)

    drawCamel()
    drawSun()


def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(55, WIDTH / HEIGHT, 0.1, 100)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    
    angle = math.radians(cameraAngle)
    pitch = math.radians(cameraPitch)
    horizontalDistance = cameraDistance * math.cos(pitch)

    eyeX = math.sin(angle) * horizontalDistance
    eyeY = 2.0 + cameraDistance * math.sin(pitch)
    eyeZ = -3.0 + math.cos(angle) * horizontalDistance

    gluLookAt(eyeX, eyeY, eyeZ,
              0, 2.0, -3.0,
              0, 1, 0)

    
    lightPosition = [5.0, 10.0, 5.0, 1.0]
    glLightfv(GL_LIGHT0, GL_POSITION, lightPosition)

    main()
    glutSwapBuffers()




def update(value):
    global camelX, camelDirection, legAngle, cloudMove
    global cameraAngle, cameraPitch, cameraDistance

    
    cameraAngle += (targetAngle - cameraAngle) * 0.12
    cameraPitch += (targetPitch - cameraPitch) * 0.12
    cameraDistance += (targetDistance - cameraDistance) * 0.12

    if not paused and not dragging:
        camelX += camelSpeed * camelDirection

        if camelX > 6:
            camelDirection = -1
        elif camelX < -6:
            camelDirection = 1

        legAngle = math.sin(math.radians(glutGet(GLUT_ELAPSED_TIME) * 0.25)) * 22

        cloudMove += 0.008
        if cloudMove > 4:
            cloudMove = -4

    glutPostRedisplay()
    glutTimerFunc(16, update, 0)




def normalKey(key, x, y):
    global paused, targetAngle, targetPitch, targetDistance

    if key == b' ':
        paused = not paused
    elif key in (b'r', b'R'):
        resetScene()
    elif key in (b'a', b'A'):
        targetAngle -= 8
    elif key in (b'd', b'D'):
        targetAngle += 8
    elif key in (b'w', b'W'):
        targetDistance = max(10, targetDistance - 2)
    elif key in (b's', b'S'):
        targetDistance = min(40, targetDistance + 2)
    elif key in (b'q', b'Q'):
        targetPitch = min(82, targetPitch + 6)
    elif key in (b'e', b'E'):
        targetPitch = max(-5, targetPitch - 6)
    elif key in (b't', b'T'):
        targetPitch = 78
    elif key in (b'g', b'G'):
        targetPitch = 15

    glutPostRedisplay()


def specialKey(key, x, y):
    global targetAngle, targetPitch

    if key == GLUT_KEY_LEFT:
        targetAngle -= 8
    elif key == GLUT_KEY_RIGHT:
        targetAngle += 8
    elif key == GLUT_KEY_UP:
        targetPitch = min(82, targetPitch + 6)
    elif key == GLUT_KEY_DOWN:
        targetPitch = max(-5, targetPitch - 6)

    glutPostRedisplay()



def mouseClick(button, state, x, y):
    global dragging, dragObject, lastMouseX, lastMouseY

    if button == GLUT_LEFT_BUTTON:
        if state == GLUT_DOWN:
            mouseY = HEIGHT - y

            
            if x > WIDTH * 0.58 and mouseY > HEIGHT * 0.55:
                dragObject = "sun"
            else:
                dragObject = "camel"

            dragging = True
            lastMouseX = x
            lastMouseY = y

        elif state == GLUT_UP:
            dragging = False
            dragObject = ""

    glutPostRedisplay()


def mouseDrag(x, y):
    global sunX, sunY, camelX, camelZ, lastMouseX, lastMouseY

    if dragging:
        dx = x - lastMouseX
        dy = y - lastMouseY

        
        if dragObject == "sun":
            sunX += dx * 0.025
            sunY -= dy * 0.025
            sunX = max(-12, min(12, sunX))
            sunY = max(3, min(13, sunY))

        elif dragObject == "camel":
            camelX += dx * 0.025
            camelZ += dy * 0.018
            camelX = max(-8, min(8, camelX))
            camelZ = max(-3, min(9, camelZ))

        lastMouseX = x
        lastMouseY = y
        glutPostRedisplay()



def resetScene():
    global paused, sunX, sunY, camelX, camelZ
    global cameraAngle, cameraPitch, cameraDistance
    global targetAngle, targetPitch, targetDistance, camelDirection
    global legAngle, cloudMove, dragging, dragObject

    paused = False
    sunX = 7.0
    sunY = 8.0
    camelX = -4.0
    camelZ = 2.0

    cameraAngle = 0.0
    cameraPitch = 15.0
    cameraDistance = 24.0
    targetAngle = 0.0
    targetPitch = 15.0
    targetDistance = 24.0

    camelDirection = 1
    legAngle = 0.0
    cloudMove = 0.0
    dragging = False
    dragObject = ""

    glutPostRedisplay()




glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
glutInitWindowSize(WIDTH, HEIGHT)
glutInitWindowPosition(100, 50)
glutCreateWindow(b"3D Egyptian Pyramid and Desert Environment Simulation")

glEnable(GL_DEPTH_TEST)
glEnable(GL_NORMALIZE)


glShadeModel(GL_SMOOTH)


glEnable(GL_LIGHTING)
glEnable(GL_LIGHT0)
glEnable(GL_COLOR_MATERIAL)
glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

glLightfv(GL_LIGHT0, GL_AMBIENT, [0.35, 0.30, 0.24, 1.0])
glLightfv(GL_LIGHT0, GL_DIFFUSE, [0.95, 0.86, 0.72, 1.0])
glLightfv(GL_LIGHT0, GL_SPECULAR, [0.35, 0.35, 0.35, 1.0])


glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)


glEnable(GL_FOG)
fogColor = [0.72, 0.78, 0.78, 1.0]
glFogfv(GL_FOG_COLOR, fogColor)
glFogi(GL_FOG_MODE, GL_LINEAR)
glFogf(GL_FOG_START, 14.0)
glFogf(GL_FOG_END, 42.0)

glClearColor(0.48, 0.72, 0.88, 1.0)

glutDisplayFunc(showScreen)
glutKeyboardFunc(normalKey)
glutSpecialFunc(specialKey)
glutMouseFunc(mouseClick)
glutMotionFunc(mouseDrag)

glutTimerFunc(16, update, 0)

glutMainLoop()
