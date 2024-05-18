import json
import argparse
import sys

from PIL import Image


def __get_pixel_data(image_path):
    # Open the image
    img = Image.open(image_path)
    
    # Convert the image to RGB (if it's not already in that format)
    img = img.convert('RGB')
    
    # Initialize an empty 2D list for the pixel data
    pixels = []
    
    # Get the size of the image
    width, height = img.size
    
    # Loop through each pixel of the image
    for y in range(height):
        row = []
        for x in range(width):
            # Get the RGB values of the pixel
            pixel = img.getpixel((x, y))
            row.append(pixel)
        pixels.append(row)
    
    return pixels


def main():
    parser = argparse.ArgumentParser(description='Generates an LCD bitmap from an image')
    parser.add_argument('-i', '--image', type=str, help='Path to the image file')
    parser.add_argument('-j', '--json', type=str, help='Path to the JSON file')
    parser.add_argument('-o', '--output', type=str, help='Path to the output file')
    
    args = parser.parse_args()
    
    imagefile = args.image
    if imagefile == None:
        sys.exit('No image file specified')
        
    jsonfile = args.json
    if jsonfile == None:
        sys.exit('No JSON file specified')
        
    outputfile = args.output
    if outputfile == None:
        sys.exit('No output file specified')

    
    print("Image file: {}\JSON file: {}".format(imagefile, jsonfile))

    pixels = __get_pixel_data(imagefile)
        
    bitmap = {}
        
    with open(jsonfile) as f:
        data = json.load(f)
        
        for key in data.keys():
            print("Char: {} | X: {}, Y: {}, Width: {}, Height: {}".format(key, data[key][0], data[key][1], data[key][2], data[key][3]))
            
            x = int(data[key][0])
            y = int(data[key][1])
            w = int(data[key][2])
            h = int(data[key][3])
            
            rows = []
            rows.append([w, h])
            for y1 in range(y, y+h):
                row = []
                for x1 in range(x, x+w):
                    if pixels[y1][x1] == (255, 255, 255):
                        row.append(1)
                    else:
                        row.append(0)
                rows.append(row)
            
            bitmap[key] = rows
        
    # Space character
    bitmap[' '] = [[5,11],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]
    
    with open(outputfile, 'w') as f:
        json.dump(bitmap, f)
        
if __name__ == "__main__":
    main()