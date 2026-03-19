# ボールを配置してたまにランダムな初速を与える
# ボール同士が重なり荒ぶる

import pygame
import random
import math
import numpy as np

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Billiards Simulation")
clock = pygame.time.Clock()


# Ball class
class Ball:
    def __init__(self, x, y, radius, color, velocity, is_cue_ball=False):
        self.pos = np.array([x, y])
        self.radius = radius
        self.color = color
        self.vel = np.array(velocity, dtype=np.float64)
        self.elasticity = 0.9  # Coefficient of restitution
        self.is_cue_ball = is_cue_ball

    def move(self):
        self.pos += self.vel.astype(np.int64)

        # Friction simulation (slows down over time)
        self.vel *= 0.99

        # Wall collision
        # if self.x - self.radius <= 0 or self.x + self.radius >= WIDTH:
        #     self.vx *= -1
        # if self.y - self.radius <= 0 or self.y + self.radius >= HEIGHT:
        #     self.vy *= -1
        if (
            self.pos[0] - self.radius <= 0
            or self.pos[0] + self.radius >= WIDTH
        ):
            self.vel[0] *= -1
        if (
            self.pos[1] - self.radius <= 0
            or self.pos[1] + self.radius >= HEIGHT
        ):
            self.vel[1] *= -1

    def draw(self, screen):
        pygame.draw.circle(
            screen, self.color, self.pos.astype(np.int64), self.radius
        )

    def collide(self, other):
        diff = self.pos - other.pos
        distance = np.linalg.norm(diff)
        n = diff / distance  # Normalized difference

        gap = distance - (self.radius + other.radius)

        if gap < 0:
            self.pos += (n * gap / 2).astype(np.int64)
            other.pos -= (n * gap / 2).astype(np.int64)

            self_s = np.dot(self.vel, n)
            other_s = np.dot(other.vel, n)

            self_v_x = self_s * n
            self_v_y = self.vel - self_v_x

            other_v_x = other_s * n
            other_v_y = other.vel - other_v_x

            tmp = self.elasticity * (self_s - other_s)
            self_s2 = (self_s + other_s - tmp) / 2
            other_s2 = (self_s + other_s + tmp) / 2

            self_v_x_2 = self_s2 * n
            other_v_x_2 = other_s2 * n

            self.vel = self_v_x_2 + self_v_y
            other.vel = other_v_x_2 + other_v_y


# Generate billiard balls (1 ball with random velocity)
velocity_multiplier = 10
ball_radius = 20
balls = [
    Ball(
        150,
        HEIGHT // 2,
        ball_radius,
        (255, 255, 255),
        (velocity_multiplier * 1, 0),
        is_cue_ball=True,
    )
]

route3 = math.sqrt(3)
start_x = 500
x_dif = route3 * ball_radius + 1
y_dif = route3 * ball_radius + 1
center = HEIGHT // 2


triangle_positions = [
    (start_x + x_dif * 0, center),
    (start_x + x_dif * 1, center - y_dif),
    (start_x + x_dif * 1, center + y_dif),
    (start_x + x_dif * 2, center - 2 * y_dif),
    (start_x + x_dif * 2, center),
    (start_x + x_dif * 2, center + 2 * y_dif),
    (start_x + x_dif * 3, center - 3 * y_dif),
    (start_x + x_dif * 3, center - y_dif),
    (start_x + x_dif * 3, center + y_dif),
    (start_x + x_dif * 3, center + 3 * y_dif),
]

for pos in triangle_positions:
    balls.append(
        Ball(
            pos[0],
            pos[1],
            ball_radius,
            (
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255),
            ),
            (0, 0),
        )
    )

# Main loop
running = True
while running:
    screen.fill((0, 128, 0))  # Green table background

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move and draw balls
    for ball in balls:
        ball.move()
        ball.draw(screen)

    # Check for collisions
    for i in range(len(balls)):
        for j in range(i + 1, len(balls)):
            balls[i].collide(balls[j])

    if np.linalg.norm(balls[0].vel) < 0.1:
        balls[0].vel = velocity_multiplier * np.random.uniform(-1, 1, 2)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
