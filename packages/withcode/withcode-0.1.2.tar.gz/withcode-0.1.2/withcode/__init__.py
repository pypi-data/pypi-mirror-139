"""
withcode

Offline python module to match visualisation and sound features of create.withcode.uk
"""

__version__ = "0.1.2"
__author__ = 'Pete Dring'

import tkinter

_win = None

class Image:
    def __init__(self):
        self._canvas = None
    
    # draw an image from a 2d list of pixel data
    def draw(self, data, width=200, height=200, drawGrid = True):
        global _win, _canvas
        
        # create window if one doesn't already exist
        if _win == None:
            _win = tkinter.Tk()
            _win.title("Image")
        
        # create canvas for drawing
        if self._canvas == None:
            self._canvas = tkinter.Canvas(_win, width=width, height=height)
            self._canvas.pack()

        # determine number of dimensions (2d list for a B/W or greyscale image or 3d list for RGB colour)
        dimensions = 0
        d = data
        try:
            while dimensions <= 3:
                d = d[0]
                dimensions += 1
        except:
            pass
            
        # create window to display image
        _win.geometry("{}x{}".format(width, height))
        
        # discover image size
        if dimensions < 2:
            return
        img_height = len(data)
        img_width = len(data[0])
        
        # discover colour mode: BW / GREYSCALE / RGB
        mode = "BW"
        if dimensions == 3:
            mode = "RGB"
        else:
            for x in range(img_width):
                for y in range(img_height):
                    if data[y][x] > 1:
                       mode = "GREYSCALE"
                       break
                if mode == "GREYSCALE":
                    break
        
        # draw image
        box_w = width / img_width
        box_h = height / img_height
        for x in range(img_width):
            for y in range(img_height):
                pixel = data[y][x]
                fill = "black"
                if mode == "BW":
                    if pixel > 0:
                        fill = "white"
                elif mode == "GREYSCALE":
                    grey = 0
                    if pixel > 0 and pixel <= 255:
                        grey = hex(pixel)[2:].zfill(2)
                    fill = "#{}{}{}".format(grey, grey, grey)
                elif mode == "RGB":
                    r = hex(pixel[0])[2:].zfill(2)
                    g = hex(pixel[1])[2:].zfill(2)
                    b = hex(pixel[2])[2:].zfill(2)
                    fill = "#{}{}{}".format(r, g, b)
                color = fill
                if drawGrid:
                    color = "black"
                self._canvas.create_rectangle(x * box_w, y * box_h, (x+1) * box_w, (y+1) * box_h, fill=fill, outline=color)
        _win.update()

# test: should draw a 8x8 grid changing the amount of red and green
if __name__ == "__main__":
    data = [[[red * 32, green * 32, 255] for red in range(8)] for green in range(8)]
    print(data)
    i = Image()
    i.draw(data, 500, 500)
        
