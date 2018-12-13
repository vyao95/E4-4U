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
    
def get_board_coordinates():    
    # Collect click events until on_click returns False
    with Listener(on_click=on_click) as listener:
        listener.join()
    
def on_click(x, y, button, pressed):
    if pressed:
        coordinates.append((x,y))
    if len(coordinates) == 2:
        # Stop listener
        return False

def screen_grab_box():
    x1,y1 = coordinates[0]
    x2,y2 = coordinates[1]
    box = (x1, y1, x2, y2)
    im = ImageGrab.grab(box)
    if DEBUG:
        im.save('cat.png')
    return im
    

def get_top_left_piece(image):
    x,y = 0,0
    board_rgb = image.getpixel((x,y))
    while (image.getpixel((x,y)) == board_rgb):
        x,y = (x+5,y+5)
    return (x,y)

def left_click(x, y):
    mouse.move(x,y)
    mouse.press(Button.left)
    mouse.release(Button.left)
# def main():
 
if __name__ == '__main__':
    print("Please click top left and bottom right of the Connect 4 Board on your turn.")
    get_board_coordinates()
    image = screen_grab_box()
    get_top_left_piece(image)
    print(coordinates)