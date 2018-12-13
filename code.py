from PIL import ImageGrab
from pynput.mouse import Button, Controller, Listener
import os
import time

DEBUG = True

mouse = Controller()


board_width = 7
board_height = 6


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
    print("GTLP board rgb: " + str(board_rgb))
    while (image.getpixel((x,y)) == board_rgb):
        x,y = (x+10,y+10)
    if DEBUG:
        print("top left piece: " + str((x,y)))
    empty_rgb = image.getpixel((x,y))
    print("GTLP empty rgb: " + str(empty_rgb))
    return (x,y)

    
def get_right_offset(image):
    top_left_x, top_left_y = get_top_left_piece(image)
    print("GRO board rgb: " + str(board_rgb))
    print("GRO empty rgb: " + str(empty_rgb))
    x_offset = 0
    print("empty: " + str(empty_rgb))
    print("init" + str(image.getpixel((top_left_x + x_offset,top_left_y))))
    # get to the board again
    while (image.getpixel((top_left_x + x_offset,top_left_y)) == empty_rgb):
        print("going right.. empty")
        x_offset += 10
        
    print("board: " + str(board_rgb))
    print("should be board: " + str(image.getpixel((top_left_x + x_offset,top_left_y))))
    # get to the next piece from board
    while (image.getpixel((top_left_x + x_offset,top_left_y)) == board_rgb):
        print("going right.. board")
        x_offset += 10
        
    return x_offset
        
    
# left click at (x,y)
def left_click(x, y):
    if DEBUG:
        print("left clicking @ " + str((x,y)))
    mouse.move(x,y)
    mouse.press(Button.left)
    mouse.release(Button.left)
    
    
if __name__ == '__main__':
    print("Please click top left and bottom right of the Connect 4 Board on your turn.")
    get_board_coordinates()
    image = screen_grab_box()
    print(get_right_offset(image))
    print(coordinates)