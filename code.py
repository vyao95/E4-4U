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

def on_move(x, y):
    print('Pointer moved to {0}'.format(
        (x, y)))

        
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

    
def get_x_offset(image):
    top_left_x, top_left_y = get_top_left_piece(image)
    x_offset = 0
    
    # get to the board again
    while (image.getpixel((top_left_x + x_offset,top_left_y)) == empty_rgb):
        x_offset += 5
        
    # get to the next piece from board
    while (image.getpixel((top_left_x + x_offset,top_left_y)) == board_rgb):
        x_offset += 5
        
    return x_offset
        
    
# left click at (x,y)
def left_click(x, y):
    if DEBUG:
        print("left clicking @ " + str((x,y)))
    mouse.move(x,y)
    mouse.press(Button.left)
    mouse.release(Button.left)

def populateState(topLeft, offset):
    top_left_x, top_left_y = topLeft
    image = screen_grab_box()

    state = {}
    for col in range(board_width):
        for row in range(board_height):
            state[(col,row)] = empty

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

    
if __name__ == '__main__':    
    if DEBUG:
        image = ImageGrab.Image.open('./connect4board.png')
        image = image.convert('RGB')
    else:  
        print("Please click top left and bottom right of the Connect 4 Board on your turn.")
        get_board_coordinates()
        image = screen_grab_box()
        
        
    top_left = get_top_left_piece(image)
    x_offset = get_x_offset(image)
    print("offset: " + str(x_offset))
    
   
    if DEBUG:
        print("board rgb: " + str(board_rgb))
        print("empty rgb: " + str(empty_rgb))
        for col in range(board_width):
            for row in range(board_height):
                print("Trying " + str((top_left[0]+x_offset*col,top_left[1]+x_offset*row)))
                print(image.getpixel((top_left[0]+x_offset*col,top_left[1]+x_offset*row)))
                # image.putpixel((top_left[0]+x_offset*i,top_left[1]),0)
                image.putpixel((top_left[0]+x_offset*col,top_left[1]+x_offset*row),(0,0,0))
        image.save('cat.png')
