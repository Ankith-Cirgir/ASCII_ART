import sys, random, argparse 
import numpy as np 
import math
import PIL
import PIL.ImageFont
import PIL.ImageOps
import PIL.ImageDraw 

from subprocess import call

PIXEL_ON = 0 
PIXEL_OFF = 255  
  
from PIL import Image 

gscale1 = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "
  
gscale2 = '@%#*+=-:. '


banner =  r"""
   ________                           ____        __ 
  / ____/ /_  ______ ___  _______  __/ __ \____ _/ /_
 / /   / / / / / __ `__ \/ ___/ / / / /_/ / __ `/ __/
/ /___/ / /_/ / / / / / (__  ) /_/ / _, _/ /_/ / /_  
\____/_/\__,_/_/ /_/ /_/____/\__, /_/ |_|\__,_/\__/  
                            /____/                   """


try:
    call('cls', shell=True) 
    call('color 0a', shell=True)
except:
    pass


print(banner)


def text_image(text_path, font_path=None):

    grayscale = 'L'

    with open(text_path) as text_file:  
        lines = tuple(l.rstrip() for l in text_file.readlines())

    large_font = 20  
    font_path = font_path or 'cour.ttf'  
    try:
        font = PIL.ImageFont.truetype(font_path, size=large_font)
    except IOError:
        font = PIL.ImageFont.load_default()
        print('Could not use chosen font. Using default.')


    pt2px = lambda pt: int(round(pt * 96.0 / 72))
    max_width_line = max(lines, key=lambda s: font.getsize(s)[0])

    test_string = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    max_height = pt2px(font.getsize(test_string)[1])
    max_width = pt2px(font.getsize(max_width_line)[0])
    height = max_height * len(lines)  
    width = int(round(max_width + 40)) 
    image = PIL.Image.new(grayscale, (width, height), color=PIXEL_OFF)
    draw = PIL.ImageDraw.Draw(image)

    vertical_position = 5
    horizontal_position = 5
    line_spacing = int(round(max_height * 0.8)) 
    for line in lines:
        draw.text((horizontal_position, vertical_position),
                  line, fill=PIXEL_ON, font=font)
        vertical_position += line_spacing

    c_box = PIL.ImageOps.invert(image).getbbox()
    image = image.crop(c_box)
    return image



  
def getAverageL(image): 
    im = np.array(image) 
    w,h = im.shape 
    return np.average(im.reshape(w*h)) 
  
def covertImageToAscii(fileName, cols, scale, moreLevels): 

    global gscale1, gscale2 
    try:
        image = Image.open(fileName).convert('L')
    except:
        try:
            call('cls', shell=True) 
            call('color 0a', shell=True)
            print("File not found ... :(\n\nCheck you file and try again :)")
            sys.exit()
        except:
            sys.exit()
            
    W, H = image.size[0], image.size[1] 
  
    w = W/cols 
  
    h = w/scale 
  
    rows = int(H/h) 
      
  
    if cols > W or rows > H: 
        print("Image too small for specified cols!") 
        exit(0) 
  
    aimg = [] 
    for j in range(rows): 
        y1 = int(j*h) 
        y2 = int((j+1)*h) 
  
        if j == rows-1: 
            y2 = H 
  
        aimg.append("") 
  
        for i in range(cols): 
  
            x1 = int(i*w) 
            x2 = int((i+1)*w) 
  
            if i == cols-1: 
                x2 = W 
  
            img = image.crop((x1, y1, x2, y2)) 
  
            avg = int(getAverageL(img)) 
  
            if moreLevels: 
                gsval = gscale1[int((avg*69)/255)] 
            else: 
                gsval = gscale2[int((avg*9)/255)] 
  
            aimg[j] += gsval 
      
    return aimg 
  
def main(): 
    descStr = "ClumsyRat"
    parser = argparse.ArgumentParser(description=descStr) 
    parser.add_argument('--file', dest='imgFile', required=True) 
    parser.add_argument('--scale', dest='scale', required=False) 
    parser.add_argument('--out', dest='outFile', required=False) 
    parser.add_argument('--cols', dest='cols', required=False) 
    parser.add_argument('--morelevels',dest='moreLevels',action='store_true') 
  
    args = parser.parse_args() 
    
    imgFile = args.imgFile 
  
    outFile = 'out.txt'
    if args.outFile: 
        outFile = args.outFile 

    scale = 0.43
    if args.scale: 
        scale = float(args.scale) 
  
    cols = 80
    if args.cols: 
        cols = int(args.cols) 
  
    print('generating ASCII art...') 
    aimg = covertImageToAscii(imgFile, cols, scale, args.moreLevels) 
  
    f = open(outFile, 'w') 
  
    for row in aimg: 
        f.write(row + '\n') 
  
    f.close() 
    print("ASCII art written to %s" % outFile) 
    print("\nConverting into png file...")
    image = text_image(outFile)
    #image.show()
    image.save('out.png')
    print("\nDONE !!! --check the folder for .txt file and .png file :)")
  
if __name__ == '__main__': 
    main() 