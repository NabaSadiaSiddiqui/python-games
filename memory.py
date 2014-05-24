# implementation of card game - Memory

import simplegui
import random

# global variables
cardValues = {}
exposed = []
state = 0
turnCounter = 0
""" idx is a list which stores the indices of the last 2 cards which were exposed """
idx = []

# helper function to initialize globals
def new_game():
    global cardValues, exposed, turnCounter
    
    # model the deck of cards and store the result in tmpList
    tmpList = range(8)
    tmpList1 = range(8)
    random.shuffle(tmpList)
    random.shuffle(tmpList1)
    tmpList.extend(tmpList1)
    i = 0
    for num in tmpList:
        cardValues[i] = num
        i = i+1
    
    """ initialize the list exposed
        each element of the list corresponds to one of the cards on the canvas
        exposed[i] = True means the card is face up
        exposed[i] = False means the card is face down
        initially, all cards are face down """
    exposed = []
    num = range(16)
    for n in num:
        exposed.append(False)
        
    turnCounter = 0
    label.set_text("Turns = " + str(turnCounter))
     
# define event handlers
def mouseclick(pos):
    # add game state logic here
    global exposed, state, idx, turnCounter
    point = list(pos)
    x = point[0]//50
    if state == 0:
        if not exposed[x]:
            exposed[x] = True
            idx.append(x)
            state = 1
    if state == 1:
        if not exposed[x]:
            turnCounter = turnCounter + 1
            exposed[x] = True
            idx.append(x)
            state = 2
            label.set_text("Turns = " + str(turnCounter))
    if state == 2:
        # indices of the last 2 exposed cards
        idx_1 = idx[-1]
        idx_2 = idx[-2]
        if not exposed[x]:
            if cardValues[idx_1] != cardValues[idx_2]:
                exposed[idx_1] = False
                exposed[idx_2] = False
            exposed[x] = True
            state = 1
            idx.append(x)
    print turnCounter
                        
# cards are logically 50x100 pixels in size    
def draw(canvas):
    global cardValues, exposed
    
    # draw numbers associated with each card on the canvas
    x = 25
    y = 75
    for key, value in cardValues.items():
        point = [x, y]        
        if exposed[key]: # draw the number only if the card is exposed (face-up)
            canvas.draw_text(str(value), point, 25, "White")
        else: # draw a blank green rectangle
            canvas.draw_polygon([(x-25,0), (x+25, 0), (x+25, 100), (x-25, 100)], 5, "White", "Green")
        x += 50    


# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()

