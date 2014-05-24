# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True
ball_pos = [WIDTH/2, HEIGHT/2]
ball_vel = [0, 0]
paddle1_pos = 0
paddle2_pos = 0
paddle1_vel = 0
paddle2_vel = 0
score1 = 0
score2 = 0

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    vel_x = random.randrange(120, 240) / 60
    vel_y = random.randrange(60, 180) / 60
    if direction == 'RIGHT':
        ball_vel[0] = vel_x
        ball_vel[1] = vel_y
    elif direction == 'LEFT':
        ball_vel[0] = - vel_x
        ball_vel[1] = - vel_y

# check if ball collides with the top and bottom walls
def bounce_ball_vert():
    global ball_pos, ball_vel
    if ball_pos[1] >= (HEIGHT-1)-BALL_RADIUS or ball_pos[1] <= BALL_RADIUS:
        ball_vel[1] *= -1

# check if the ball collides with either of the paddles        
def check_collision():
    global score1, score2, ball_pos, paddle1_pos, paddle2_pos
    if ball_pos[0] >= (WIDTH -1)-PAD_WIDTH-BALL_RADIUS:
        if paddle2_pos-HALF_PAD_HEIGHT <= ball_pos[1]-BALL_RADIUS <= paddle2_pos+HALF_PAD_HEIGHT or paddle2_pos-HALF_PAD_HEIGHT <= ball_pos[1]+BALL_RADIUS <= paddle2_pos+HALF_PAD_HEIGHT:

            increase_ball_vel(10)
            spawn_ball("LEFT")
        else:
            respawn("LEFT")
            score1 += 1
    elif ball_pos[0] <= PAD_WIDTH+BALL_RADIUS:
        if paddle1_pos-HALF_PAD_HEIGHT <= ball_pos[1]-BALL_RADIUS <= paddle1_pos+HALF_PAD_HEIGHT or paddle1_pos-HALF_PAD_HEIGHT <= ball_pos[1]+BALL_RADIUS <= paddle1_pos+HALF_PAD_HEIGHT:
            increase_ball_vel(10)
            spawn_ball("RIGHT")
        else:
            score2 +=1
            respawn("RIGHT")

# set position of the paddles
def set_paddle_pos(paddle_num):
    global paddle1_pos, paddle2_pos
    if paddle_num==1:
        paddle1_pos = random.randrange(0, HEIGHT)
    if paddle_num==2:
        paddle2_pos = random.randrange(0, HEIGHT)

""" returns true if paddle_num is within limits
    paddle_num==1 is the left paddle
    paddle_num==2 is the right paddle """
def check_paddle_limits(paddle_num):
    if paddle_num==1:
        return paddle1_pos+HALF_PAD_HEIGHT <= HEIGHT and paddle1_pos-HALF_PAD_HEIGHT >= 0
    if paddle_num==2:
        return paddle2_pos+HALF_PAD_HEIGHT <= HEIGHT and paddle2_pos-HALF_PAD_HEIGHT >= 0

# respawn ball in the middle 
def respawn(direction):
    global ball_pos
    ball_pos = [WIDTH/2, HEIGHT/2]
    spawn_ball(direction)

# increase ball velocity by percent. 0 <percent <= 100    
def increase_ball_vel(percent):
    global ball_vel
    ball_vel[0] *= (1 + percent*0.01)
    ball_vel[1] *= (1 + percent*0.01)

# launch ball
def launch():
    ran_choice = random.randrange(0, 2)
    if ran_choice == 1:
        respawn("LEFT")
    else:
        respawn("RIGHT")
        
# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    score1 = 0
    score2 = 0
    ball_vel = [0, 0]
    paddle1_vel = 0
    paddle2_vel = 0
    # set vertical positions of paddle1 and paddle2
    while not(check_paddle_limits(1)):
        set_paddle_pos(1)
    while not(check_paddle_limits(2)):
        set_paddle_pos(2)
    launch()

def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel   
        
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")

    # bounce ball of the top and bottom of the wall    
    bounce_ball_vert()
    
    # spawn ball to the right or left if it touches one of the gutters
    check_collision()
    
    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
        
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 1, "White", "White")
    
    # update paddle's vertical position, keep paddle on the screen
    bkup_paddle1_pos = paddle1_pos
    bkup_paddle2_pos = paddle2_pos
    paddle1_pos += paddle1_vel
    paddle2_pos += paddle2_vel
    if not check_paddle_limits(1):
        paddle1_pos = bkup_paddle1_pos	# restore paddle pos if out of canvas
    if not check_paddle_limits(2):
        paddle2_pos = bkup_paddle2_pos	# restore paddle pos if out of canvas
    
    # draw paddles
    canvas.draw_line([HALF_PAD_WIDTH, paddle1_pos-HALF_PAD_HEIGHT], [HALF_PAD_WIDTH, paddle1_pos+HALF_PAD_HEIGHT], PAD_WIDTH, "White")
    canvas.draw_line([WIDTH-HALF_PAD_WIDTH, paddle2_pos-HALF_PAD_HEIGHT], [WIDTH-HALF_PAD_WIDTH, paddle2_pos+HALF_PAD_HEIGHT], PAD_WIDTH, "White")

    # draw scores
    canvas.draw_text(str(score1), [WIDTH/4, HEIGHT/4], 100, "White")
    canvas.draw_text(str(score2), [(WIDTH/4)*3, HEIGHT/4], 100, "White")
        
def keydown(key):
    global paddle1_vel, paddle2_vel
    if key==87:	# w was pressed
        paddle1_vel -= 3
    if key==83:	# s was pressed
        paddle1_vel += 3
    if key==38: # Up arraw was pressed
        paddle2_vel -= 3
    if key==40:	# Down arraw was pressed
        paddle2_vel += 3
        
def keyup(key):
    global paddle1_vel, paddle2_vel
    if key==87:	# w was released
        paddle1_vel = 0
    if key==83:	# s was released
        paddle1_vel = 0
    if key==38: # Up arraw was released
        paddle2_vel = 0
    if key==40:	# Down arraw was released
        paddle2_vel = 0

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("Reset", new_game, 100)


# start frame
new_game()
frame.start()

