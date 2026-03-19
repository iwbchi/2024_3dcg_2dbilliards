# ネットから引っ張ってきた適当なサンプル
# めっちゃ動く

import math
import random

import pygame

# import numpy as np
# import copy

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (90, 90, 180)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GREY = (50, 50, 255)

SCREEN_WIDTH = 700
SCREEN_HEIGHT = 650

SPEED_COEF = 12.0

start_time = pygame.time.get_ticks()


class Ball:
    """
    Class to keep track of a ball's location and vector.
    """

    def __init__(self):
        # radius
        self.r = 10
        # diameter
        self.d = self.r * 2
        # position
        self.x = 0
        self.y = 0
        # velocity
        self.vx = 0
        self.vy = 0
        # color
        self.color = (0, 255, 0)
        # neighbour
        self.px = False
        self.mx = False
        self.py = False
        self.my = False


def make_ball():
    """
    Function to make a new, random ball.
    """
    ball = Ball()
    # Starting position of the ball.
    # Take into account the ball size so we don't spawn on the edge.
    ball.x = random.randrange(ball.d, SCREEN_WIDTH - ball.d)
    ball.y = random.randrange(ball.d, SCREEN_HEIGHT - ball.d - 200)
    # Speed and direction of rectangle
    ball.vx = float(random.randrange(-2, 2)) * SPEED_COEF
    ball.vy = float(random.randrange(-2, 2)) * SPEED_COEF

    return ball


def main():
    """
    main program.
    """
    pygame.init()
    xval = 0
    bcount = 0
    # redcount = 0
    # Set the height and width of the screen
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("OverShoot")
    # Loop until the user clicks the close button.
    done = False
    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()
    # dictionary
    results = {}
    cell_size = 40
    ball_amount = 10
    # Spawn many balls
    for i in range(ball_amount):
        ball = make_ball()
        results.setdefault(
            (int(ball.x / cell_size), int(ball.y / cell_size)), []
        ).append(ball)

    print(len(results.keys()))
    # print(results)
    screen.fill(
        (20, 20, 20),
        rect=(0, SCREEN_HEIGHT - 250, SCREEN_WIDTH, SCREEN_HEIGHT),
    )
    # -------- Main Program Loop -----------
    while not done:
        # --- Event Processing
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                # Space bar! Spawn a new ball.
                if event.key == pygame.K_SPACE:
                    ball = make_ball()
                    ball.color = RED
                    results.setdefault(
                        (int(ball.x / cell_size), int(ball.y / cell_size)), []
                    ).append(ball)
                    #
                if event.key == pygame.K_g:
                    ball = make_ball()
                    ball.color = (255, 0, 255)
                    results.setdefault(
                        (int(ball.x / cell_size), int(ball.y / cell_size)), []
                    ).append(ball)

        # --- Drawing
        # Set the screen background
        screen.fill(
            GREY, rect=(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT - 200 + ball.d)
        )

        # Draw the balls
        cresults = {}
        for ky in results:
            blist = results[ky]
            blist2 = blist.copy()
            #
            for bl in blist:

                blist2.remove(bl)
                if bl.px:
                    k = (ky[0] + 1, ky[1])
                    if k in results:
                        ek = results[k]
                        blist2.extend(ek)
                if bl.mx:
                    k = (ky[0] - 1, ky[1])
                    if k in results:
                        ek = results[k]
                        blist2.extend(ek)
                if bl.py:
                    k = (ky[0], ky[1] + 1)
                    if k in results:
                        ek = results[k]
                        blist2.extend(ek)
                if bl.my:
                    k = (ky[0], ky[1] - 1)
                    if k in results:
                        ek = results[k]
                        blist2.extend(ek)
                if bl.px and bl.py:
                    k = (ky[0] + 1, ky[1] + 1)
                    if k in results:
                        ek = results[k]
                        blist2.extend(ek)
                if bl.mx and bl.py:
                    k = (ky[0] - 1, ky[1] + 1)
                    if k in results:
                        ek = results[k]
                        blist2.extend(ek)
                if bl.px and bl.my:
                    k = (ky[0] + 1, ky[1] - 1)
                    if k in results:
                        ek = results[k]
                        blist2.extend(ek)
                if bl.mx and bl.my:
                    k = (ky[0] - 1, ky[1] - 1)
                    if k in results:
                        ek = results[k]
                        blist2.extend(ek)
                #
                for bl2 in blist2:
                    # if bl == bl2:
                    #    continue
                    # Circle Intersect
                    sqDist = (bl2.x - bl.x) * (bl2.x - bl.x) + (
                        bl2.y - bl.y
                    ) * (bl2.y - bl.y)
                    # if sqDist > 0 and sqDist <= ((BALL_SIZE)+(BALL_SIZE)):
                    # print(sqDist, math.sqrt(sqDist))
                    if sqDist > 0 and sqDist <= (bl.d * bl.d):
                        # detect collision
                        dist = math.sqrt(sqDist)
                        # vCollison
                        vc = [bl2.x - bl.x, bl2.y - bl.y]
                        # vCollisonNorm
                        vcn = [vc[0] / dist, vc[1] / dist]
                        # vRelativeVelocity
                        vrv = [bl.vx - bl2.vx, bl.vy - bl2.vy]
                        speed = vrv[0] * vcn[0] + vrv[1] * vcn[1]
                        # print(speed)
                        if speed > 0:
                            bl.vx -= speed * vcn[0]
                            bl.vy -= speed * vcn[1]
                            bl2.vx += speed * vcn[0]
                            bl2.vy += speed * vcn[1]
                            #
                            # infection
                            if bl.color == RED and bl2.color != RED:
                                bl2.color = RED
                                bcount += 1
                            if bl2.color == RED and bl.color != RED:
                                bl.color = RED
                                bcount += 1
                #
                col = bl.color
                pygame.draw.circle(
                    screen, col, [round(bl.x), round(bl.y)], bl.r
                )
                bl.x += bl.vx
                bl.y += bl.vy
                # avoid line y
                if bl.y > SCREEN_HEIGHT - 200 + bl.r:
                    bl.y = SCREEN_HEIGHT - 200
                    bl.vy = -bl.vy

                if bl.y < bl.r:
                    bl.y = bl.r
                    bl.vy = -bl.vy

                if bl.x < bl.r:
                    bl.x = bl.r
                    bl.vx = -bl.vx

                if bl.x <= 0:
                    bl.vx = 0.1

                if bl.x > SCREEN_WIDTH - bl.r:
                    bl.x = SCREEN_WIDTH - bl.r
                    bl.vx = -bl.vx
                #
                # Bounce the ball if needed
                if bl.y > SCREEN_HEIGHT - 200 or bl.y < bl.r:
                    bl.vy *= -1
                if bl.x > SCREEN_WIDTH - bl.r or bl.x < bl.r:
                    bl.vx *= -1

                # set key and get hash and append
                cresults.setdefault(
                    (int(bl.x / cell_size), int(bl.y / cell_size)), []
                ).append(bl)
                #
                # check neighbour with new key
                bl.px = int((bl.x + bl.r) / cell_size) > int(bl.x / cell_size)
                bl.mx = int((bl.x - bl.r) / cell_size) < int(bl.x / cell_size)
                bl.py = int((bl.y + bl.r) / cell_size) > int(bl.y / cell_size)
                bl.my = int((bl.y - bl.r) / cell_size) < int(bl.y / cell_size)

        results.clear()
        results.update(cresults)
        # show stat
        timepassed = pygame.time.get_ticks() - start_time
        if timepassed % 12 == 0:

            if bcount > 0 and bcount < ball_amount:
                pygame.draw.line(
                    screen,
                    (200, 0, 0),
                    (xval * 2, SCREEN_HEIGHT - 10),
                    (xval * 2, SCREEN_HEIGHT - int(bcount / 5) - 10),
                    2,
                )
                xval += 1

        # for res in results:
        #     a = results[res]
        #     for bl in a:
        #         pygame.draw.circle(screen, WHITE, [round(bl.x), round(bl.y)], BALL_SIZE)
        #     break
        # Go ahead and update the screen with what we've drawn.
        clock.tick(60)
        pygame.display.flip()

    # Close everything down
    pygame.quit()


if __name__ == "__main__":
    main()
