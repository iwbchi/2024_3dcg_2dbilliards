import pygame
from OpenGL.GL import (
    glColor3f,
    glPushMatrix,
    glTranslatef,
    glPopMatrix,
    glClearColor,
    glLoadIdentity,
    glMatrixMode,
    GL_PROJECTION,
    GL_MODELVIEW,
    glClear,
    GL_COLOR_BUFFER_BIT,
)

from OpenGL.GLUT import glutSolidSphere, glutInit

from OpenGL.GLU import gluOrtho2D
import random

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
TABLE_WIDTH = 6.0
TABLE_HEIGHT = 3.0
BALL_RADIUS = 0.1
FPS = 60


# Ball class
class Ball:
    def __init__(self, x, y, vx, vy, color):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color

    def update(self, dt):
        # Update position
        self.x += self.vx * dt
        self.y += self.vy * dt

        # Reflect off walls
        if (
            self.x - BALL_RADIUS < -TABLE_WIDTH / 2
            or self.x + BALL_RADIUS > TABLE_WIDTH / 2
        ):
            self.vx = -self.vx
        if (
            self.y - BALL_RADIUS < -TABLE_HEIGHT / 2
            or self.y + BALL_RADIUS > TABLE_HEIGHT / 2
        ):
            self.vy = -self.vy

    def draw(self):
        glColor3f(*self.color)
        glPushMatrix()
        glTranslatef(self.x, self.y, 0)
        glutSolidSphere(BALL_RADIUS, 32, 32)
        glPopMatrix()


# Initialize OpenGL
def init_opengl():
    glutInit()
    glClearColor(0.0, 0.5, 0.0, 1.0)  # Green background (table color)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(
        -TABLE_WIDTH / 20, TABLE_WIDTH / 2, -TABLE_HEIGHT / 2, TABLE_HEIGHT / 2
    )
    glMatrixMode(GL_MODELVIEW)


# Main simulation
def main():
    pygame.init()
    pygame.display.set_mode(
        (WINDOW_WIDTH, WINDOW_HEIGHT), pygame.OPENGL | pygame.DOUBLEBUF
    )
    init_opengl()

    # Create a ball with random initial velocity
    ball = Ball(
        x=0.0,
        y=0.0,
        vx=random.uniform(-1.0, 1.0),
        vy=random.uniform(-1.0, 1.0),
        color=(1.0, 0.0, 0.0),  # Red color
    )

    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        glClear(GL_COLOR_BUFFER_BIT)

        # Update and draw the ball
        dt = clock.get_time() / 1000.0
        ball.update(dt)
        ball.draw()

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
