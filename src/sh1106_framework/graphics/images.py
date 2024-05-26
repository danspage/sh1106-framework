import json
from pathlib import Path

class Images:
    _images = {}
    
    @staticmethod
    def _register_images(filepath: str) -> None:
        with open(filepath) as f:
            temp_images = json.load(f)
            print("Reading images from " + filepath)
            for key in temp_images.keys():
                Images._images[key] = temp_images[key]
                print("Loaded image \"{}\" from {}".format(key, filepath))