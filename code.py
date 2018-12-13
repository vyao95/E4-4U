from MCTS import MCTS
from connect4 import Board
import pyscreenshot as ImageGrab
import PIL as Image
from pynput.mouse import Button, Controller, Listener
import sys
import os
import time


DEBUG = True
DEBUG_FILE = False
DEBUG_file = "./empty_board.png"
# DEBUG_file = "./enemy_board.png"

board_width = 7
board_height = 6

enemy = 'x'
player = 'o'
empty = '.'


# [top-left,bottom-right] as according to user clicks
coordinates = [] 

# rgb values of various pieces on the board
board_rgb = (0,0,0)
empty_rgb = (0,0,0)
enemy_rgb = (0,0,0)
player_rgb = (0,0,0)

# distance between pieces
x_offset = 0
y_offset = 0

# x and y pixels of the top-left piece.
# this is essentially our (0,0) => base
base_x = 0
base_y = 0


#*************** MOUSE OPERATIONS ***************

# left click at (x,y)
def left_click(pos):
    mouse = Controller()
    if DEBUG:
        print("left clicking @ " + str((pos[0],pos[1])))
    mouse.position = (pos[0],pos[1])
    mouse.press(Button.left)
    mouse.release(Button.left)
    

        
# Fills the coordinates list with user's first two clicks
def on_click(x, y, button, pressed):
    global coordinates
    if pressed:
        coordinates.append((x,y))
        if DEBUG:
            print("Adding to coordinates: " + str((x,y)))
    if len(coordinates) == 2:
        if DEBUG:
            print("*Stopping listener*")
            print("Coordinates: " + str(coordinates))
        # Stop listener
        return False
  

#*************** MISC HELPERS ***************


# translates a move from MCTS implementation to the actual game implementation
# move: MCTS move
# returns: GAME move
def translate_MCTS_move(move):
    m_x,m_y = move
    m_y = (m_y - 5) * -1
    GAME_move = (base_x + m_x * x_offset, base_y + m_y * y_offset)
    
    return GAME_move

    
# Sets all global variables
# EXCEPT player and enemy rgb values. We must play first two games to get these
def initialize_game():
    if not DEBUG_FILE:
        set_board_coordinates()
    image = get_screenshot()
    set_top_left_piece(image)
    set_offsets(image)
    

#*************** SETTERS ***************

   
# Starts listener thread for click events    
def set_board_coordinates():    
    # Collect click events until on_click returns False
    with Listener(on_click=on_click) as listener:
        listener.join()
        
        
# Finds the first pixel going down and right until the rgb value changes (empty spot)
# Then sets board_rgb, empty_rgb, base_x, base_y
# image: image from ImageGrab library
def set_top_left_piece(image):
    global board_rgb, empty_rgb, base_x, base_y
    
    try:
        board_rgb = image.getpixel((base_x,base_y))
        # go down and right from the top left of the board until we reach an empty spot
        while (image.getpixel((base_x,base_y)) == board_rgb):
            base_x,base_y = (base_x+5,base_y+5)
            
        empty_rgb = image.getpixel((base_x,base_y))
            
        if DEBUG:
            print("top left piece (base): " + str((base_x,base_y)))
            print("board_rgb: " + str(board_rgb))
            print("empty_rgb: " + str(empty_rgb))

    except IndexError:
        print("ERROR in set_top_left_piece: Not able to find first piece. Aborting...")
        sys.exit(1)
    

#sets x and y offsets (how far the pieces are from each other)
# image: image from ImageGrab library
def set_offsets(image):
    global x_offset, y_offset
    
    try:
        if DEBUG:
            print("set offsets: ")
        # get to the board again going right
        while (image.getpixel((base_x + x_offset,base_y)) == empty_rgb):
            if DEBUG:
                pixel_rgb = image.getpixel((base_x + x_offset,base_y))
                print("\tFound: " + str(pixel_rgb))
                print("\tGoing right 5 from " + str((base_x + x_offset,base_y)))
                
            x_offset += 5
            
        # get to the next piece going right
        while (image.getpixel((base_x + x_offset,base_y)) == board_rgb):
            if DEBUG:
                pixel_rgb = image.getpixel((base_x + x_offset,base_y))
                print("\tFound: " + str(pixel_rgb))
                print("\tGoing right 5 from " + str((base_x + x_offset,base_y)))
                
            x_offset += 5
            
            
        # get to the board again going down
        while (image.getpixel((base_x,base_y + y_offset)) == empty_rgb):
            if DEBUG:
                pixel_rgb = image.getpixel((base_x,base_y + y_offset))
                print("\tFound: " + str(pixel_rgb))
                print("\tGoing right 5 from " + str((base_x + x_offset,base_y)))
                
            y_offset += 5
            
        # get to the next piece going down
        while (image.getpixel((base_x,base_y + y_offset)) == board_rgb):
            if DEBUG:
                pixel_rgb = image.getpixel((base_x,base_y + y_offset))
                print("\tFound: " + str(pixel_rgb))
                print("\tGoing down 5 from " + str((base_x + x_offset,base_y)))
                
            y_offset += 5
            
    except IndexError:
        print("ERROR in set_offsets: Not able to find the offsets")
        sys.exit(1)
    
    
    
# set player_rgb value. To do this, we must play the player's first piece.
# we will always get player rgb by clicking a spot and then getting the pixel there,
# whether we go first or second.
# board: the board with state updated to latest state
def set_player_rgb(board):
    global player_rgb
    
    move = MCTS(board.state)
    board.do_move(board.state,player,move) # updates board state
    move = translate_MCTS_move(move)
    left_click(move) # updates actual game (clicks in game)
    time.sleep(1)
    # here we know what our move is, so wait until our piece lands, then get the rgb value
    image = get_screenshot()
    player_rgb = image.getpixel(move)
    if DEBUG:
        print("set_player_rgb: ")
        print("\tplayer_rgb: " + str(player_rgb))
    
    
#*************** GETTERS ***************    
    
    
# Gets a screenshot from coordinates[0] and coordinates[1]
# Returns: screenshot
def get_screenshot():
    if DEBUG_FILE:
        im = ImageGrab.Image.open(DEBUG_file)
        im = im.convert('RGB')
    else:
        x1,y1 = coordinates[0]
        x2,y2 = coordinates[1]
        box = (x1, y1, x2, y2)
        im = ImageGrab.grab(box)
        
    return im      


# returns state of the game for early game.
# Note: this also sets enemy_rgb
#   image: screenshot of game
#   num_turns: 1 or 2 - first or second turn in the game
def get_init_state(num_turns):
    global enemy_rgb
    image = get_screenshot()

    state = {}

#   IF there is a piece, it's enemy's 
#   ELSE the board is empty
    if num_turns == 1:
        for col in range(0, board_width):
            mcts_piece = (col,0)
            game_piece = translate_MCTS_move(mcts_piece)
            pixel_rgb = image.getpixel(game_piece)
                
            if pixel_rgb == empty_rgb:
                state[mcts_piece] = empty
            else:
                enemy_rgb = pixel_rgb
                state[mcts_piece] = enemy
                
            if DEBUG:
                image.putpixel(game_piece,(255,0,0))
        if DEBUG:
            print("get_init_state_1:")
            print("\tstate: " + str(state))
            image.save("get_init_state_1.png")
     
#   this will only be called if player goes first, so player_rgb is set and we need enemy rgb.
    elif num_turns == 2:
        for col in range(0, board_width):
            # only need first two rows
            for row in range(0,2):
                mcts_piece = (col,row)
                game_piece = translate_MCTS_move(mcts_piece)
                pixel_rgb = image.getpixel(game_piece)
                
                if pixel_rgb == empty_rgb:
                    state[mcts_piece] = empty
                elif pixel_rgb == player_rgb:
                    state[mcts_piece] = player
                else: 
                    enemy_rgb = pixel_rgb
                    state[mcts_piece] = enemy
                    
                if DEBUG:
                    image.putpixel(game_piece,(255,0,0))
        if DEBUG:
            print("get_init_state_2:")
            print("\tstate: " + str(state))
            image.save("get_init_state_2.png")
                    
    return state
    
    
#*************** MAIN ***************
    
if __name__ == '__main__':   
    print("Please click top left and bottom right of the Connect 4 Board on your turn.")
    initialize_game()
    
    b = Board()
    b.state.update(get_init_state(1))
    
    if DEBUG:
        print("\nStarting game...")
        b.print_board(b.state)
    
    # ========= FOR THE FIRST TWO MOVES WE MUST SET PLAYER AND ENEMY RGB'S=====
    # enemy did a move, enemy_rgb is set. Must figure out player_rgb value
    if enemy in b.state.values(): 
        if DEBUG:
            print("Initial game is enemy turn")
        set_player_rgb(b)
        
    # nothing on the board
    # figure out player_rgb value, then poll until state changes to get enemy_rgb
    else: 
        if DEBUG:
            print("Initial game is player turn")
        set_player_rgb(b)
        while b.state == get_init_state(2):
            time.sleep(5)