import os
import json
from pathlib import Path

from graphics.drawing import Drawing

class Images:
    __images = {}
    
    @staticmethod
    def _register_images(filepath: str) -> None:
        filename = Path(filepath).stem
        
        with open(filepath) as f:
            temp_images = json.load(f)
            print("Reading images from " + filepath)
            for key in temp_images.keys():
                Images.__images[key] = temp_images[key]
                print("Loaded image \"{}\" from {}".format(key, filepath))
                
    @staticmethod
    def _draw_image(image: str, x: int, y: int, color: int = 1, scale: int = 1, centered_horizontal: bool = False, centered_vertical: bool = False) -> None:
        image_pixels = Images.__images[image]
        
        if centered_horizontal:
            offset_x = int((-image_pixels[0][0]*scale) / 2)
        else:
            offset_x = 0
            
        if centered_vertical:
            offset_y = int((-image_pixels[0][1]*scale) / 2)
        else:
            offset_y = 0
        
        for y1 in range(image_pixels[0][1]):
            for x1 in range(image_pixels[0][0]):
                if image_pixels[y1+1][x1] == 1:
                    if scale == 1:
                        Drawing.set_pixel(x+x1+offset_x, y+y1+offset_y, color)
                    else:
                        Drawing.draw_rect(int(x+x1*scale+offset_x), int(y+y1*scale+offset_y), scale, scale, color)