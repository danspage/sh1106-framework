import json

class Fonts:
    __bitmaps = {}
    
    char_list = " abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!?<>,./:;\"'@#$%^&*()_-+="
    
    @staticmethod
    def _register_font(font_name: str, filepath: str):
        with open(filepath) as f:
            Fonts.__bitmaps[font_name] = json.load(f)
            print("Loaded font \"{}\" from {}".format(font_name, filepath))
    
    @staticmethod
    def _get_char(font, char):
        return Fonts.__bitmaps[font][str(char)]