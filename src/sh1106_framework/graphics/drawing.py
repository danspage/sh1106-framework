from luma.core.interface.serial import i2c
from luma.oled.device import sh1106

from PIL import Image
import time

from graphics.fonts import Fonts
from graphics.images import Images

class Drawing:
    """
    A drawing class for the SH1106 OLED screen. It handles drawing pixels, text, shapes, and images.
    """
    
    __lcdserial: i2c = None
    __lcddevice: sh1106 = None
    
    __lcdpixels = []
    __image = None
    
    __last_contrast_update_time = 0
    __contrast_update_interval = 0.1
    __prev_contrast = 255
    __current_contrast = 255
    
    __width = 0
    __height = 0
    
    @staticmethod
    def _init(port: int, address: int) -> None:
        Drawing.__lcdserial = i2c(port=port, address=address)
        Drawing.__lcddevice = sh1106(Drawing.__lcdserial)
        
        Drawing.__width = Drawing.__lcddevice.width
        Drawing.__height = Drawing.__lcddevice.height
        
        Drawing.__lcddevice.clear()
        for y in range(Drawing.__height):
            Drawing.__lcdpixels.append([])
            for x in range(Drawing.__width):
                Drawing.__lcdpixels[y].append(0)
        
        Drawing.__image = Image.new('1', (Drawing.__width, Drawing.__height))
    
    @staticmethod
    def __validate_pixel(x: int, y: int) -> bool:
        if x < 0 or x >= Drawing.__width:
            return False
        if y < 0 or y >= Drawing.__height:
            return False
        return True
    
    @staticmethod
    def get_width() -> int:
        """
        Returns the width of the LCD screen in pixels.
        """
        return Drawing.__width
    
    @staticmethod
    def get_height() -> int:
        """
        Returns the height of the LCD screen in pixels.
        """
        return Drawing.__height        
                
    @staticmethod
    def set_contrast(contrast: int) -> None:
        """
        Sets the contrast (a.k.a. brightness) of the SH1106 display.

        Parameters
        ----------
        contrast: int
            The contrast to set the display to, between 0 and 255.
        """
        
        Drawing.__prev_contrast = Drawing.__current_contrast
        Drawing.__current_contrast = contrast
        
    @staticmethod
    def _update_contrast() -> None:
        # Update the contrast if it has changed, but only every __contrast_update_interval seconds
        # This is because updating the contrast too often can cause the screen to lag behind
        
        if Drawing.__current_contrast != Drawing.__prev_contrast:
            current_time = time.time()
            if current_time - Drawing.__last_contrast_update_time >= Drawing.__contrast_update_interval:
                Drawing.__last_contrast_update_time = current_time
                Drawing.__lcddevice.contrast(int(Drawing.__current_contrast*25.5))
        
    @staticmethod
    def clear() -> None:
        """
        Clears the LCD screen.
        """
        for y in range(Drawing.__height):
            for x in range(Drawing.__width):
                Drawing.__lcdpixels[y][x] = 0
                
    @staticmethod
    def set_pixel(x: int, y: int, color: int) -> None:
        """
        Sets a pixel on the LCD screen.
        
        Parameters
        ----------
        x: int
            The x coordinate of the pixel to set.
        y: int
            The y coordinate of the pixel to set.
        color: int
            The color of the pixel to set, either 0 or 1.
        """
        if Drawing.__validate_pixel(x, y):
            Drawing.__lcdpixels[y][x] = color
            
    @staticmethod
    def get_text_width(text: str, font: str = "default", scale: int = 1) -> int:
        """
        Returns the width of a string of text in pixels.
        
        Parameters
        ----------
        text: str
            The string of text to get the width of.
        font: str
            The name of the font to use.
        scale: int
            The scale of the text.
        """
        text_width = 0
        for i in range(len(text)):
            char = text[i]
            text_width += scale * (Fonts._get_char(font, char)[0][0] + 1)
        
        return text_width
                        
    @staticmethod
    def draw_text(text: str, x: int, y: int, color: int = 1, font: str = "default", scale: int = 1, centered: bool = False) -> None:
        """
        Draws a string of text on the LCD screen.
        
        Parameters
        ----------
        text: str
            The string of text to draw.
        x: int
            The x coordinate of the text.
        y: int
            The y coordinate of the text.
        color: int
            The color of the text, either 0 or 1.
        font: str
            The name of the font to use.
        scale: int
            The scale of the text.
        centered: bool
            Whether or not the text should be centered.
        """
        
        if centered:
            start_x = x - Drawing.get_text_width(text, font=font, scale=scale) // 2
            
            for i in range(len(text)):
                char = text[i]
                
                char_bitmap = Fonts._get_char(font, char)[1:]
                for y1 in range(len(char_bitmap)):
                    for x1 in range(len(char_bitmap[y1])):
                        if char_bitmap[y1][x1] == 1:
                            if scale == 1:
                                if Drawing.__validate_pixel(start_x+x1, y+y1):
                                    Drawing.__lcdpixels[y+y1][start_x+x1] = color
                            else:
                                Drawing.draw_rect(start_x + x1*scale, y+ y1 *scale, scale, scale, color)

                start_x += scale * (Fonts._get_char(font, char)[0][0] + 1)
        else:
            start_x = int(x)
            
            for i in range(len(text)):
                char = text[i]
                
                char_bitmap = Fonts._get_char(font, char)[1:]
                for y1 in range(len(char_bitmap)):
                    for x1 in range(len(char_bitmap[y1])):
                        if char_bitmap[y1][x1] == 1:
                            if scale == 1:
                                if Drawing.__validate_pixel(start_x+x1, y+y1):
                                    Drawing.__lcdpixels[y+y1][start_x+x1] = color
                            else:
                                Drawing.draw_rect(start_x + x1*scale, y+ y1 *scale, scale, scale, color)

                start_x += scale * (Fonts._get_char(font, char)[0][0] + 1)
            
    @staticmethod
    def draw_rect(x: int, y: int, width: int, height: int, color: int = 1) -> None:
        """
        Draws a rectangle on the LCD screen.
        
        Parameters
        ----------
        x: int
            The x coordinate of the rectangle.
        y: int
            The y coordinate of the rectangle.
        width: int
            The width of the rectangle.
        height: int
            The height of the rectangle.
        color: int
            The color of the rectangle, either 0 or 1.
        """
        
        # Clip to fit within screen borders
        new_x = max(0, x)
        new_y = max(0, y)
        new_width = min(width, Drawing.__width - new_x)
        new_height = min(height, Drawing.__height - new_y)
        
        for y1 in range(new_height):
            for x1 in range(new_width):
                Drawing.__lcdpixels[new_y+y1][new_x+x1] = color
                
    @staticmethod
    def draw_outlined_rect(x: int, y: int, width: int, height: int, color: int = 1) -> None:
        """
        Draws an outlined rectangle on the LCD screen.
        
        Parameters
        ----------
        x: int
            The x coordinate of the rectangle.
        y: int
            The y coordinate of the rectangle.
        width: int
            The width of the rectangle.
        height: int
            The height of the rectangle.
        color: int
            The color of the rectangle, either 0 or 1.
        """

        for x1 in range(x, x+width): # Top border
            Drawing.set_pixel(x1, y, color)
        for x1 in range(x, x+width): # Bottom border
            Drawing.set_pixel(x1, y+height-1, color)
        for y1 in range(y+1, y+height-1): # Left border
            Drawing.set_pixel(x, y1, color)
        for y1 in range(y+1, y+height-1): # Right border
            Drawing.set_pixel(x+width-1, y1, color)
                    
    @staticmethod
    def draw_line(x0: int, y0: int, x1: int, y1: int, color: int = 1) -> None:
        """
        Draws a line on the LCD screen.
        
        Parameters
        ----------
        x0: int
            The x coordinate of the starting point of the line.
        y0: int
            The y coordinate of the starting point of the line.
        x1: int
            The x coordinate of the ending point of the line.
        y1: int
            The y coordinate of the ending point of the line.
        color: int
            The color of the line, either 0 or 1.
        """
        
        # Optimized bresenham's line algorithm
        # See last code block from https://en.wikipedia.org/wiki/Bresenham%27s_line_algorithm#All_cases
        dx = abs(x1 - x0)
        sx = 1 if x0 < x1 else -1
        dy = -abs(y1 - y0)
        sy = 1 if y0 < y1 else -1
        error = dx + dy
        
        while True:
            Drawing.set_pixel(x0, y0, color)
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * error
            if e2 >= dy:
                if x0 == x1:
                    break
                error = error + dy
                x0 = x0 + sx
            if e2 <= dx:
                if y0 == y1:
                    break
                error = error + dx
                y0 = y0 + sy
                
    @staticmethod
    def draw_image(image: str, x: int, y: int, color: int = 1, scale: int = 1, centered_horizontal: bool = False, centered_vertical: bool = False) -> None:
        """
        Draws an image on the LCD screen.
        
        Parameters
        ----------
        image: str
            The name of the image to draw.
        x: int
            The x coordinate of the image.
        y: int
            The y coordinate of the image.
        color: int
            The color of the image, either 0 or 1.
        scale: int
            The scale of the image.
        centered_horizontal: bool
            Whether or not the image should be centered horizontally.
        centered_vertical: bool
            Whether or not the image should be centered vertically.
        """
        
        Images._draw_image(image, x, y, color, scale, centered_horizontal, centered_vertical)
    
    @staticmethod
    def _render() -> None:
        width = len(Drawing.__lcdpixels[0])
        height = len(Drawing.__lcdpixels)
        
        # Convert the 2D list into a bytes object with bit packing
        packed_data = []
        for row in Drawing.__lcdpixels:
            # Pack 8 pixels into each byte
            for i in range(0, len(row), 8):
                byte = 0
                for bit in row[i:i+8]:
                    byte = (byte << 1) | bit
                packed_data.append(byte)
                
        binary_data = bytes(packed_data)
        
        # Create an image from the byte data
        Drawing.__image = Image.frombytes('1', (width, height), binary_data)
        
        
        Drawing.__lcddevice.display(Drawing.__image)