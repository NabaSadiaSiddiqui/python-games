# Blackjack

import simplegui
import random

# load card sprite - 949x392 - source: jfitz.com
CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)
card_images = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")

CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)
card_back = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0

deck = []
hand_player = []
hand_dealer = []

title = "Blackjack"

msgPlayer = "Hit or stand?"
msgDealer = ""

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)

# define hand class        
class Hand:
    def __init__(self):	# create Hand object
        self.hand = []

    def __str__(self):	# return a string representation of a hand
        strHand = "Hand contains"
        for card in self.hand:
            strHand += " " + str(card)
        return strHand

    def add_card(self, card):	# add a card object to a hand
        self.hand.append(card)

    def get_value(self):	# compute the value of the hand
        vHand = 0
        aceTrue = 0
        for card in self.hand:
            rank = card.get_rank()
            value = VALUES[rank]
            vHand += value
            
            if rank == 'A':
                aceTrue = 1
        
        if aceTrue:
            if vHand+10 <= 21:
                vHand += 10
         
        return vHand
   
    def draw(self, canvas, pos):	# draw a hand on the canvas
        for card in self.hand:
            x = pos[0] + (self.hand.index(card)*CARD_SIZE[0])
            y = pos[1]
            _pos = (x, y)
            card.draw(canvas, _pos)
        
# define deck class 
class Deck:
    def __init__(self):	# create a Deck object
        self.deck = []
        for suit in SUITS:
            for rank in RANKS:
                self.deck.append(Card(suit, rank))

    def shuffle(self):	# shuffle the deck
        random.shuffle(self.deck)

    def deal_card(self):	# deal a card object from the deck
        return self.deck.pop()
    
    def __str__(self): # return a string representing the deck
        strDeck = "Deck contains"
        for card in self.deck:
            strDeck += " " + str(card)
        return strDeck

#define event handlers for buttons
def deal():
    global outcome, in_play
    
    global deck, hand_player, hand_dealer, msgPlayer, msgDealer, score
    
    msgPlayer = "Hit or stand?"
    msgDealer = ""
 
    if in_play == True:
        msgPlayer = "You lost the round"
        msgDealer = ""
        score += 1
    
    # create a deck  and shuffle it
    deck = Deck()
    deck.shuffle()
    in_play = True
        
    hand_player = Hand()	# create a new player hand and add 2 cards to it
    hand_player.add_card(deck.deal_card())
    hand_player.add_card(deck.deal_card())
  
    hand_dealer = Hand()    # create a new dealer hand and add 2 cards to it
    hand_dealer.add_card(deck.deal_card())
    hand_dealer.add_card(deck.deal_card())
  
def hit():
    global hand_player, deck, msgPlayer, msgDealer, score, in_play

    if in_play == True:    
        # if the hand is in play, hit the player
        if hand_player.get_value() <= 21:
            deck.shuffle()
            hand_player.add_card(deck.deal_card())
        
        # if busted, assign a message to outcome, update in_play and score
        if hand_player.get_value() > 21:
            msgPlayer = "New deal?"
            msgDealer = "Player busted."
            score += 1
            in_play = False
    
def stand():
    global hand_player, hand_dealer, deck, in_play, msgPlayer, msgDealer, score

    if in_play == True:    
        if hand_player.get_value()>21:
            msgPlayer = "New deal?"
            msgDealer = "Player busted"
            score += 1
        else:    
            # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
            while hand_dealer.get_value() <= 17:
                deck.shuffle()
                hand_dealer.add_card(deck.deal_card())
    
            if hand_dealer.get_value() > 17:
                msgDealer = "You busted"
                msgPlayer = "New deal?"
                score -= 1
            else:	# assign a message to outcome, update in_play and score
                if hand_dealer.get_value() >= hand_player.get_value():
                    msgDealer = "You win"
                    msgPlayer = "New deal?"
                    score += 1
                else:
                    msgDealer = "Player wins"
                    msgPlayer = "New deal?"
                    score -= 1
                   
        in_play = False            

# draw handler    
def draw(canvas):
    
    # draw dealer's hand
    posDlr = (100, 250)
    hand_dealer.draw(canvas, posDlr)
    # hide first card if in_play is true
    if in_play == True:
        dest_pos = [posDlr[0] + CARD_BACK_SIZE[0]*0.5, posDlr[1] + CARD_BACK_SIZE[1]*0.5]
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, dest_pos, CARD_BACK_SIZE)

        
    # draw player's hand
    posPlyr = (100, 450)    
    hand_player.draw(canvas, posPlyr)
    
    # draw related text/messages
    canvas.draw_text(title, [60, 75], 40, "#00FFFF")
    canvas.draw_text("Dealer", [50, 200], 30, "Black")
    canvas.draw_text(msgDealer, [200, 200], 30, "Black")
    canvas.draw_text("Player", [50, 400], 30, "Black")
    canvas.draw_text(msgPlayer, [200, 400], 30, "Black")
    
    # draw score
    canvas.draw_text("Score", [400 ,75], 40, "Black")
    canvas.draw_text(str(score), [550, 75], 40, "Black")


# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()
