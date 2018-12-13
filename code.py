import pyscreenshot as ImageGrab
import PIL as Image
from pynput.mouse import Button, Controller, Listener
from connect4 import Board
import os
import time

DEBUG = True

mouse = Controller()


board_width = 7
board_height = 6

enemy = 'x'
player = 'o'
empty = '.'

coordinates = []
board_rgb = (0,0,0)
empty_rgb = (0,0,0)
enemy_rgb = (0,0,0)
player_rgb = (0,0,0)
    
    
# Starts listener thread for click events    
def get_board_coordinates():    
    # Collect click events until on_click returns False
    with Listener(on_click=on_click) as listener:
        listener.join()


# Fills the coordinates list with user's first two clicks
def on_click(x, y, button, pressed):
    if pressed:
        coordinates.append((x,y))
        # if DEBUG:
            # print("Adding to coordinates: " + str((x,y))
    if len(coordinates) == 2:
        if DEBUG:
            print("*Stopping listener*")
            print("Coordinates: " + str(coordinates))
        # Stop listener
        return False
        
# Gets a screenshot from coordinates[0] and coordinates[1]
# Returns: screenshot
def screen_grab_box():
    x1,y1 = coordinates[0]
    x2,y2 = coordinates[1]
    box = (x1, y1, x2, y2)
    im = ImageGrab.grab(box)
    
    if DEBUG:
        print("screen_grab_box() with " + str(box) + "saved as cat.png")
        im.save('cat.png')
        
    return im
    

# Finds the first pixel going down and right until the rbg value changes
# We use this to find the top left spot of the board
# image: image from ImageGrab library
# returns coordinates of the top-left piece
def get_top_left_piece(image):
    global board_rgb, empty_rgb
    x,y = 0,0
    board_rgb = image.getpixel((x,y))
    
    while (image.getpixel((x,y)) == board_rgb):
        x,y = (x+5,y+5)
        
    if DEBUG:
        print("top left piece: " + str((x,y)))

    empty_rgb = image.getpixel((x,y))
    return (x,y)

    
def get_offset(image):
    
    top_left_x, top_left_y = get_top_left_piece(image)
    offset_x = 0
    offset_y = 0
    
    # get to the board again
    while (image.getpixel((top_left_x + offset_x,top_left_y)) == empty_rgb):
        offset_x += 5
        
    # get to the next piece from board
    while (image.getpixel((top_left_x + offset_x,top_left_y)) == board_rgb):
        offset_x += 5
        
    # get to the board again
    while (image.getpixel((top_left_x,top_left_y + offset_y)) == empty_rgb):
        offset_y += 5
        
    # get to the next piece from board
    while (image.getpixel((top_left_x,top_left_y + offset_y)) == board_rgb):
        offset_y += 5
            
    return (offset_x,offset_y)
        
    
# left click at (x,y)
def left_click(x, y):
    if DEBUG:
        print("left clicking @ " + str((x,y)))
    mouse.move(x,y)
    mouse.press(Button.left)
    mouse.release(Button.left)

def get_state(image):
    top_left_x, top_left_y = get_top_left_piece(image)
    offset_x,offset_y = get_offset(image)

    state = {}

    col = 0
    for i in range(0, board_width, offset):
        row = 0
        for j in range(0, board_height, offset):
            print(image.getpixel((top_left_x + i, top_left_y + j)))
            if image.getpixel((top_left_x + i, top_left_y + j)) == enemy_rgb:
                state[(col, row)] = enemy
            elif image.getpixel((top_left_x + i, top_left_y + j)) == player_rgb:
                state[(col, row)] = player
            else:
                state[(col, row)] = empty
            row += 1
        col += 1

    return state

# returns state of the game 
#   image: screenshot of game
#   num_turns: 1 or 2
#       if 1, then IF there is a piece, it's enemy's ELSE the board is empty
#       if 2, 
def get_state(image,num_turns):
    top_left_x, top_left_y = get_top_left_piece(image)
    offset_x,offset_y = get_offset(image)

    state = {}

    if num_turns == 1:
        for col in range(0, board_width):
            # 0 -2 because only need initial two states
            for row in range(4, 6):
                image.putpixel((top_left_x + x_offset * col + 5, top_left_y + y_offset * row + 5),(255,0,0))
                pixel_rgb = image.getpixel(
                    (top_left_x + x_offset * col, top_left_y + y_offset * row))
                if pixel_rgb == empty_rgb:
                    state[(col, row)] = empty
                else:
                    enemy_rgb = pixel_rgb
                    state[(col, row)] = enemy
                        
        # for col in range(board_width):
            # for row in range(board_height):
                # print("Trying " + str((top_left[0]+x_offset*col,top_left[1]+y_offset*row)))
                # print(image.getpixel((top_left[0]+x_offset*col,top_left[1]+y_offset*row)))
                # # image.putpixel((top_left[0]+x_offset*i,top_left[1]),0)

                # image.putpixel((top_left[0]+x_offset*col,top_left[1]+y_offset*row),(0,0,0))
    image.save('fish.png')
    return state

    
if __name__ == '__main__':    
    if DEBUG:
        # image = ImageGrab.Image.open('./c4_enemy_move.png')
        image = ImageGrab.Image.open('./connect4board.png')
        image = image.convert('RGB')
    else:  
        print("Please click top left and bottom right of the Connect 4 Board on your turn.")
        get_board_coordinates()
        image = screen_grab_box()
        
    x_offset,y_offset = get_offset(image)
    init_state = get_state(image,1)
    b = Board()
    b.state = init_state
    if enemy in init_state.values():
        print("enemy did thing")
        # move = MCTS(b.state)
        # left_click(move[0]*x_offset,move[1]*y_offset)
        # time.sleep(1)
        # while 
        # image = screen_grab_box()
        #screenshot
        #player rgb
    else:
        print("nothing did thing")
        #MCTS
        #player rgb
        #poll
        # enemy rgb
    
   
    # if DEBUG:
        
        # top_left = get_top_left_piece(image)
        # print("offset: " + str(x_offset))
        # print("board rgb: " + str(board_rgb))
        # print("empty rgb: " + str(empty_rgb))
        # for col in range(board_width):
            # for row in range(board_height):
                # print("Trying " + str((top_left[0]+x_offset*col,top_left[1]+y_offset*row)))
                # print(image.getpixel((top_left[0]+x_offset*col,top_left[1]+y_offset*row)))
                # # image.putpixel((top_left[0]+x_offset*i,top_left[1]),0)

                # image.putpixel((top_left[0]+x_offset*col,top_left[1]+y_offset*row),(0,0,0))
        # image.save('cat.png')
