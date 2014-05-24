import simplegui
import math

# define global variables
tick=0
A=0
B=0
time="0:00.0"
reset=True
running=False
stop_total=0
stop_whole=0

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    global A, B
    tmp = t * 0.1	# converts t into seconds
    A = int(tmp) / 60	# mask out the minute portion of sec
    B = tmp % 60	# mask out the second portion of sec
    if A < 0:
        A = 0
    if int(math.ceil(B)) <= 10:
        return str(A)+":0"+str(B)
    else:
        return str(A)+":"+str(B)
    
# define event handlers for buttons; "Start", "Stop", "Reset"
def reset_timer():
    print "Reseting timer"
    global tick, reset, running, stop_total, stop_whole
    tick = 0
    reset = True
    running = False
    stop_total = 0
    stop_whole = 0
    timer.stop()

def start_timer():
    print "Starting timer"
    global reset, running
    reset = False
    running = True
    timer.start()

def stop_timer():
    print "Stopping timer"
    global reset, running, stop_total, stop_whole
    reset = False
    timer.stop()
    if running:
        running = False
        stop_total += 1
        if tick%10==0:
            stop_whole += 1
            print "Stopped on a whole second!"

# define event handler for timer with 0.1 sec interval
def timer_handler():
    global tick
    tick += 1

# helper function to draw the structure of the stopwatch
def draw_stopwatch(canvas):
    # draw shape of the stopwatch
    canvas.draw_circle((225, 250), 2, 10, "Yellow")
    canvas.draw_circle((225, 250), 6, 25, "Yellow")
    canvas.draw_circle((225, 250), 10, 50, "Yellow")
    canvas.draw_circle((225, 250), 70, 75, "Yellow")
    canvas.draw_circle((225, 250), 150, 100, "Yellow")
    # draw start, stop, reset buttons
    canvas.draw_circle((225, 20), 8, 15, "Gray")
    canvas.draw_circle((115, 50), 8, 15, "Gray")
    canvas.draw_circle((335, 50), 8, 15, "Gray")
    canvas.draw_circle((225, 55), 15, 25, "Yellow")
    canvas.draw_circle((125, 80), 15, 25, "Yellow")
    canvas.draw_circle((325, 80), 15, 25, "Yellow")
    canvas.draw_circle((225, 250), 150, 5, "#CC66FF")
    canvas.draw_circle((225, 250), 175, 15, "#990066")
    # draw pane
    canvas.draw_polygon([(125, 200), (325, 200), (325, 300), (125, 300)], 5, "Black", "White")
    
# define draw handler
def draw_handler(canvas):
    # draw stopwatch's UI
    draw_stopwatch(canvas)
            
    global tick, time, stop_total, stop_whole
  
    if timer.is_running():
        time = format(tick)
    
    if not(reset):
        canvas.draw_text(time, (150, 270), 60, "Black")
    else:
        canvas.draw_text("0:00.0", (150, 270), 60, "Black")

    canvas.draw_text("min", (150, 320), 20, "Black")
    canvas.draw_text("sec", (235, 320), 20, "Black")
    
    canvas.draw_text(str(stop_whole)+" / "+str(stop_total), (375, 50), 50, "Black")
    
    
# create frame
frame = simplegui.create_frame("Stopwatch: The Game", 500, 500)
timer = simplegui.create_timer(100, timer_handler)

# register event handlers
frame.set_canvas_background('#CCFFFF')
frame.add_button("Reset", reset_timer, 100)
frame.add_button("Start", start_timer, 100)
frame.add_button("Stop", stop_timer, 100)
frame.set_draw_handler(draw_handler)

# start frame
frame.start()

