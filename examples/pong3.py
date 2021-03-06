# Copyright 2014, Eric Clack, eric@bn7.net
# This program is distributed under the terms of the GNU General Public License

"""A simple bat and ball game."""

import random, time
from geekclub_packages import *

create_canvas()

bat_img = PhotoImage(file='images/bat.gif')
ball_img = PhotoImage(file='images/ball.gif')
brick_img = PhotoImage(file='images/small_brick.gif')

bat = ImageSprite(bat_img)

ball = ImageSprite(ball_img)
ball.speed_x = random.randint(-4,4) * 2
ball.speed_y = random.randint(-4,4) * 2
ball.max_speed = 10
ball.move_to(CANVAS_WIDTH/2, CANVAS_HEIGHT/2)

bricks = []
for y in range(0, 400, 28):
    for x in range(0, CANVAS_WIDTH, 101):
        brick = ImageSprite(brick_img)
        brick.move_to(x, y)
        bricks.append(brick)

def bat_follows_mouse():
    bat.move_to(mousex(), mousey())

def bounce_ball():
    ball.move_with_speed()
    ball.if_on_edge_bounce()
    if ball.touching(bat):
        ball.bounce_up()
        ball.accelerate(1.05)

    # Has the ball hit the bottom of the screen?
    if ball.y >= CANVAS_HEIGHT - ball.height:
        end_game()

    # Has the ball touched a brick?
    brick = ball.touching_any(bricks)
    if brick:
        if brick.below(ball):
            ball.bounce_up()
        else:
            ball.bounce_down()
        bricks.remove(brick)
        brick.delete()

def move_bricks_down():
    for b in bricks:
        b.move(0, 5)
    
forever(bat_follows_mouse, 20)
forever(bounce_ball, 20)
forever(move_bricks_down, 1000)
mainloop()
