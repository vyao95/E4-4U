from PIL import ImageGrab
import os
import time

x_pad = 540
y_pad = 430

x_size = 2280
y_size = 1290

def screenGrab():
    box = (x_pad,y_pad,x_pad+x_size,y_pad+y_size)
    im = ImageGrab.grab(box)
    im.save(os.getcwd() + '\\full_snap__' + str(int(time.time())) +
'.png', 'PNG')
 
def main():
    screenGrab()
 
if __name__ == '__main__':
    main()