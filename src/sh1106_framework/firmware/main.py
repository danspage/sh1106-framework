from graphics.fonts import Fonts
from graphics.drawing import Drawing
from framework.io.input_handler import InputHandler
from framework.states.state_manager import StateManager
from framework.constants import Constants
from data.preset_manager import PresetManager
from graphics.images import Images
from data.database_manager import DatabaseManager

import time

# Seconds per frame
SPF = 1 / Constants.FPS

def __init():
    DatabaseManager.init()
    Fonts.init()
    Drawing.init()
    Images.init()
    InputHandler.begin()
    StateManager._init()
    PresetManager.init()

if __name__ == "__main__":
    __init()
    
    next_frame_time = time.time()

    while True:
        current_time = time.time()
        
        if current_time >= next_frame_time:
            delta_time = current_time - next_frame_time + SPF
            StateManager._update(delta_time)
            StateManager._render()

            # Calculate the next frame's start time
            next_frame_time = current_time + SPF

            # This method controls the loop's execution rate to approximately match the desired FPS,
            # while minimizing CPU usage by not constantly checking the time.