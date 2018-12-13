from PIL import ImageGrab
from pynput.mouse import Button, Controller, Listener
import os
import time


mouse = Controller()


board_width = 7
board_height = 6


coordinates = []

def on_click(x, y, button, pressed):
    if pressed:
        coordinates.append((x,y))
    if len(coordinates) == 2:
        # Stop listener
        return False

def screen_grab_box():
    box = (x_pad, y_pad,x_pad + x_size, y_pad + y_size)
    im = ImageGrab.grab(box)
    im.save(os.getcwd() + '\\full_snap__' + str(int(time.time())) +
'.png', 'PNG')


def left_click(x, y):
    mouse.move(x,y)
    mouse.press(Button.left)
    mouse.release(Button.left)
    
def get_board_coordinates():    
    # Collect click events until on_click returns False
    with Listener(on_click=on_click) as listener:
        listener.join()
    
# def main():
 
if __name__ == '__main__':
    print("Please click top left and bottom right of the Connect 4 Board on your turn.")

    get_board_coordinates()
    print(coordinates)