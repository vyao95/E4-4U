from PIL import ImageGrab
from win32 import win32api, win32con
import os
import time

x_pad = 540
y_pad = 430

x_size = 2280
y_size = 1290

board_x = 7
board_y = 6

def screenGrabBox():
    box = (x_pad,y_pad,x_pad+x_size,y_pad+y_size)
    im = ImageGrab.grab(box)
    im.save(os.getcwd() + '\\full_snap__' + str(int(time.time())) +
'.png', 'PNG')


# Mouse functionality
def leftClick():
	win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
	time.sleep(.1)
	win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
	print("Click.")

def mousePos(cord):
	win32api.SetCursorPos(x_pad + cord[0], y_pad + cord[1])

def get_cords():
	x,y = win32api.GetCursorPos()
	x = x - x_pad
	y = y - y_pad
	print(x,y)

# def startGame():
# 	mousePos(())
 
def main():
    screenGrabBox()
 
if __name__ == '__main__':
    main()