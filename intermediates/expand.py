import os
import math
from PIL import Image
import pandas as pd
import numpy as np
import sys

def expand2square(pil_img, background_color):
    # https://note.nkmk.me/en/python-pillow-add-margin-expand-canvas/
    width, height = pil_img.size
    if width == height:
        return pil_img
    elif width > height:
        result = Image.new(pil_img.mode, (width, width), background_color)
        result.paste(pil_img, (0, (width - height) // 2))
        return result
    else:
        result = Image.new(pil_img.mode, (height, height), background_color)
        result.paste(pil_img, ((height - width) // 2, 0))
        return result

def pad_image(file_path):
    if '.png' in file_path:
        x = "RGBA"
    if '.jpg' in file_path:
        x = "RGB"
    print('Reading file ' + str(file_path))
    file_in = Image.open(file_path).convert(x)
    expanded_img = expand2square(pil_img = file_in, background_color=(0,0,0))
    expanded_img = expanded_img.resize((4000,4000))
    if not os.path.exists('resized'):
        os.makedirs('resized') # https://www.tutorialspoint.com/How-can-I-create-a-directory-if-it-does-not-exist-using-Python
    img_out_path = file_path.replace('segment_cropped', 'segment_uncropped')
    print('Writing file ' + str(img_out_path))
    expanded_img = expanded_img.rotate(180, expand=True)
    ########## WE ARE ROTATING IMAGES 180deg here because NN wants label on bottom and alignment homography matrix currently used wants them on top
    
    expanded_img.save(img_out_path)

def expandloop(wd):
    file_list = os.listdir(wd)
    os.chdir(wd)
    print('Working in directory' + str(wd))
    file_list = [x for x in file_list if 'segment_cropped' in x]
    print('Number of files: ' + str(len(file_list)))
    #print(file_list)
    #return(None)
    for file in file_list:
        pad_image(file)

def main():
    expandloop(sys.argv[1])

if __name__=="__main__":
    main()
