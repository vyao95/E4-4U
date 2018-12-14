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
DEBUG_pxl_off = 1 # offset to mark pixels
DEBUG_file = "./empty_board.png"
# DEBUG_file = "./enemy_board.png"

board_width = 7
board_height = 6

enemy = 'x'
player = 'o'
empty = '.'


# [top-left,bottom-right] as according to user clicks
coordinates = [] 
positions = {}

# rgb values of various pieces on the board
board_rgb = (0,0,0)
empty_rgb = (0,0,0)
enemy_rgb = (0,0,0)
player_rgb = (0,0,0)

# distance between pieces
offset_x = 0
offset_y = 0

# x and y pixels of the top-left piece.
# this is essentially our (0,0) => base
base_x = 0
base_y = 0


#*************** MOUSE OPERATIONS ***************

# left click at (x,y)
def left_click(pos):
    mouse = Controller()
    if DEBUG:
        # print("Game box: " + str(coordinates[0]) + ", " + str(coordinates[1]))
        # print("base_x: " + str(base_x))
        # print("base_y: " + str(base_y))
        # print("\toffset_x: " + str(offset_x))
        # print("\toffset_y: " + str(offset_y))
        print("left clicking @ " + str((pos[0],pos[1])))
        print("Currently @ " + str(mouse.position))
    mouse.position = (coordinates[0][0] + pos[0],
                      coordinates[0][1] + pos[1])
    mouse.press(Button.left)
    mouse.release(Button.left)
    print("Pressed @ " + str(mouse.position))
    
# left click at (x,y)
def left_click_test(pos):
    mouse = Controller()
    mouse.position = (pos)
    mouse.press(Button.left)
    mouse.release(Button.left)
    print("Pressed @ " + str(mouse.position))
    

        
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
def translate_move(move):
    global base_x, base_y
    
    move = positions[move]
    GAME_move = (move[0] + base_x, move[1] + base_y)
    
    if DEBUG:
        print("translate_MCTS_move: ")
        print("\tbase_x: " + str(base_x))
        print("\tbase_y: " + str(base_y))
        print("\tBounded: " + str(move))
        print("\tFull: " + str(GAME_move))
    
    return GAME_move

    
# Sets all global variables
# EXCEPT player and enemy rgb values. We must play first two games to get these
def initialize_game():
    if not DEBUG_FILE:
        set_board_coordinates()
    image = get_screenshot()
    set_board_empty_rgb(image)
    set_positions()
    

#*************** SETTERS ***************

   
# Starts listener thread for click events    
def set_board_coordinates():    
    # Collect click events until on_click returns False
    with Listener(on_click=on_click) as listener:
        listener.join()


# Sets positions dict with: 
#   key = MCTS implementation of position
#   value = GAME implementation of where the key is (in image - does not consider outside the game)
def set_positions():
    global positions
    
    game_height_px = coordinates[1][1] - coordinates[0][1]
    game_width_px = coordinates[1][0] - coordinates[0][0]
    
    for col in range(0,board_width):
        for row in range(0,board_height):
            col_px = int((game_width_px/(2*board_width)) * (2*col + 1))
            row_px = int((game_height_px/(2*board_height)) * (2*row + 1))
            positions[(col,(row-5)*-1)] = (col_px, row_px)
            if DEBUG:
                print("pixel[" + str((col,row)) + "] = " + str((col_px,row_px))) 
    
    
    
def set_board_empty_rgb(image):
    global empty_rgb, board_rgb
    
    board_rgb = image.getpixel(((coordinates[0][0] + coordinates[1][0])/2 - coordinates[0][0],
                                (coordinates[0][1] + coordinates[1][1])/2 - coordinates[0][1]))
           
    empty_rgb = ((coordinates[0][0] + coordinates[1][0])/2 - coordinates[0][0],
                 (coordinates[0][1] + coordinates[1][1])/2 - coordinates[0][1])
           
    while image.getpixel(empty_rgb) == board_rgb:
        empty_rgb = (empty_rgb[0],empty_rgb[1]+5)
        
    empty_rgb = image.getpixel(empty_rgb)
    
    if DEBUG:
        print("board_rgb: " + str(board_rgb))
        print("empty_rgb: " + str(empty_rgb))
    
    
# set player_rgb value. To do this, we must play the player's first piece.
# we will always get player rgb by clicking a spot and then getting the pixel there,
# whether we go first or second.
# board: the board with state updated to latest state
def set_player_rgb(board):
    global player_rgb
    
    # move = MCTS(board.state)
    move = (0,0)
    board.do_move(board.state,player,move) # updates board state
    move = translate_move(move)
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
        if not coordinates:
            coordinates.extend([(0,0),im.size])
        print(coordinates)
    else:
        x1,y1 = coordinates[0]
        x2,y2 = coordinates[1]
        box = (x1, y1, x2, y2)
        im = ImageGrab.grab(box)
        
    return im      
                

# returns state of the game for early game using the distance from 
# top left spot to the immediate right and lower spots.
# Note: this also sets enemy_rgb
#   image: screenshot of game
#   num_turns: 1 or 2 - first or second turn in the game
def get_init_state(num_turns):
    global enemy_rgb, empty_rgb, positions
    image = get_screenshot()

    state = {}
    
                
#   IF there is a piece, it's enemy's 
#   ELSE the board is empty
    if num_turns == 1:
        for MCTS_pos,GAME_pos in positions.items():
            pixel_rgb = image.getpixel(GAME_pos)
            
            if pixel_rgb == empty_rgb:
                state[MCTS_pos] = empty 
            else:
                enemy_rgb = pixel_rgb
                state[MCTS_pos] = enemy
                                
                    
            if DEBUG:
                image.putpixel((GAME_pos[0] + DEBUG_pxl_off,
                                GAME_pos[1] + DEBUG_pxl_off),
                                    (255,0,0))
        if DEBUG:
            print("get_init_state_1:")
            print("\tstate: " + str(state))
            image.save("get_init_state_1.png")
            
#   this will only be called if player goes first, so player_rgb is set and we need enemy rgb.
    elif num_turns == 2:
        for MCTS_pos,GAME_pos in positions.items():
            pixel_rgb = image.getpixel(GAME_pos)
            
            if pixel_rgb == empty_rgb:
                state[MCTS_pos] = empty 
            elif pixel_rgb == player_rgb:
                state[MCTS_pos] = player
            else:
                enemy_rgb = pixel_rgb
                state[MCTS_pos] = enemy
                                
                    
            if DEBUG:
                image.putpixel((GAME_pos[0] + DEBUG_pxl_off,
                                GAME_pos[1] + DEBUG_pxl_off),
                                    (255,0,0))
        if DEBUG:
            print("get_init_state_2:")
            print("\tstate: " + str(state))
            image.save("get_init_state_2.png")
            
    return state
    
    
# returns state of the game using spacing of the board.
def get_state():
    global enemy_rgb, empty_rgb, player_rgb
    image = get_screenshot()

    state = {}
                

    for MCTS_pos,GAME_pos in positions.items():
        state[MCTS_pos] =   empty if image.getpixel(GAME_pos) == empty_rgb else \
                            enemy if image.getpixel(GAME_pos) == enemy_rgb else \
                            player
                            
                
        if DEBUG:
            image.putpixel((GAME_pos[0] + DEBUG_pxl_off,
                        GAME_pos[1] + DEBUG_pxl_off),
                            (255,0,0))
                            
    if DEBUG:
        print("get_state:")
        print("\tstate: " + str(state))
        image.save("get_state.png")
    
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
            pass
    # left_click_test((805,650))