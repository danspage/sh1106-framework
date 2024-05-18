from graphics.drawing import Drawing
from graphics.fonts import Fonts
from graphics.images import Images
from framework.constants import Constants
from framework.states.state_manager import StateManager, State

from abc import ABC
import time

# Seconds per frame
_SPF = 1 / Constants.FPS

class SH1106Framework(ABC):
    """
    The main class for the SH1106 framework. It handles the registering of fonts, images,
    and routes, and contains the function to start the framework's main loop.
    
    Methods
    -------
    register_routes(default_route: str, routes: dict[str, State])
        Registers page routes for the framework to reference.
        
    register_font(font_name: str, filepath: str)
        Registers a font for the framework to use.
        
    register_images(filepath: str)
        Registers images for the framework to use.
        
    begin(port: int, address: int)
        Starts the framework's main loop.
    """
    
    @staticmethod
    def begin(port: int, address: int) -> None:
        """
        Starts the framework's main loop.

        Parameters
        ----------
        port: int
            The I2C port to use for the SH1106 display.
            
        address: int
            The I2C address to use for the SH1106 display.
        """
        
        Drawing._init(port=port, address=address)
        
        next_frame_time = time.time()

        while True:
            current_time = time.time()
            
            if current_time >= next_frame_time:
                delta_time = current_time - next_frame_time + _SPF
                StateManager._update(delta_time)
                StateManager._render()

                # Calculate the next frame's start time
                next_frame_time = current_time + _SPF

                # This method controls the loop's execution rate to approximately match the desired FPS,
                # while minimizing CPU usage by not constantly checking the time.
        
    @staticmethod
    def register_routes(initial_route: str, routes: dict[str, State]) -> None:
        """
        Registers page routes for the framework to reference.
        
        Parameters
        ----------
        default_route: str
            The initial route when the framework starts.
            
        routes: dict[str, State]
            A dictionary of routes and their corresponding states.
        """
        StateManager._init(initial_route, routes)
    
    @staticmethod
    def register_font(font_name: str, filepath: str) -> None:
        """
        Registers a font for the framework to use.
        
        It takes in a single JSON file created from the font generator utility.

        Parameters
        ----------
        font_name: str
            The name that the font will be referred to in the framework.
        filepath: str
            The path to the font's JSON file.
        """
        
        Fonts._register_font(font_name, filepath)
        
    @staticmethod
    def register_images(filepath: str) -> None:
        """
        Registers images for the framework to use.
        
        It takes in a single JSON file containing one or more images created from the image generator utility.

        Parameters
        ----------
        filepath: str
            The filepath to the JSON file containing the images.
        """
        
        Images._register_images(filepath)