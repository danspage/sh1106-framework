
# SH1106 OLED Screen Framework Package

A state manager, graphics, image, and custom font drawing package for the SH1106 OLED screen based on the luma.oled package. It works with Raspberry Pi and other Linux-based single-board computers.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Tools](#tools)
  - [Image utility](#image-utility)
  - [Font utility](#font-utility)

- [Usage](#usage)
  - [Basic Usage](#basic-usage)
  - [State Management](#state-management)
  - [Drawing Graphics](#drawing-graphics)

- [License](#license)

## Introduction

This package provides a comprehensive solution for managing states, drawing graphics, images, and custom fonts on the SH1106 OLED screen. It leverages the capabilities of the luma.oled package to offer an easy-to-use interface for Raspberry Pi and other Linux-based single-board computers.

## Features

- State management for different application screens
- Drawing basic shapes (lines, rectangles)
- Rendering images on the OLED screen
- Custom font support for text rendering

## Installation

To install the package, use pip:

```bash
pip install sh1106-framework
```

## Tools

The package doesn't directly load image files for images and fonts, but instead uses custom JSON bitmap files.

This package comes with two tools: an image utility and a font utility. These take user-supplied image files containing bitmaps, and convert them to json files which the framework can load. This process is split apart from the framework itself in order to reduce load time.

#### Image Utility:

The image utility can be accessed with the `sh1106_image_generator` command. It takes in a reference image, which contains one or more bitmaps within itself, and a JSON reference file, containing information about the names of the images for the framework to reference, along with their coordinates and sizes in the reference image.

The reference image can be of any size. Since the SH1106 display is monochromatic, each pixel only has a state of being on or off. In the reference image, an opaque white pixel represents a pixel being on, and any other color represents the pixel being off.

An example image can be found [here](https://github.com/danspage/sh1106-framework/blob/main/useful-assets/example-images.png), and its corresponding JSON file can be found [here](https://github.com/danspage/sh1106-framework/blob/main/useful-assets/example-images.json).

In the example image, the important color is the white, which represents the image's filled in pixels. The black and pink are simply for the sake of keeping track where each individual sub-image is.

In the JSON file, you'll see a list of entries, with arrays of four integers as the values. Bear in mind a single image loaded into the utility can contain multiple images within itself for the framework to use. The key of each entry is the name that the framework will use to reference the image after it's loaded. The four integers in the values represent the X coordinate, Y coordinate, width, and height of the image. The coordinate origin is at the top-left, with the top-left most pixel being 0,0.

If an entry looks like this: `"smiley-face": [10,10,20,15]` the framework will refer to it be the name "smiley-face". It will be 20 pixels wide and 15 pixels tall, and in the reference image provided, it will be at the 11th pixel from the left, and 11th pixel from the top.

To generate an output JSON file for the images, use the following terminal command:
```bash
sh1006_terminal_generator -i/--image <path to reference image> -j/--json <path to reference JSON> -o/--output <path to output file>
```

Then you'll use the output JSON file for initializing images when the framework is loading.

#### Font Utility:

The font utility works the exact same as the image utility, except with the `sh1106_font_generator` command instead. Instead of using names for each entry, use the character that you want to assign to the sub-image. The name of the font will be set manually via code upon initialization. The default font that you'll most likely want to include can be found here: [Image](https://github.com/danspage/sh1106-framework/blob/main/useful-assets/default-font.png), [JSON](https://github.com/danspage/sh1106-framework/blob/main/useful-assets/default-font.json)

## Usage

### Basic Usage

Here is a simple ping-pong page that displays an image, draws some text, and switches between the two pages every second. It can be found in the tests folder of the package.

<u>ping-pong.py</u>

```python
from sh1106_framework import SH1106Framework, StateManager
from ping import PingPage
from pong import PongPage

def __init():
    SH1106Framework.register_font("default", "assets/default-font.json")
    SH1106Framework.register_images("assets/example-images.json")
    
    SH1106Framework.register_routes(
        initial_route="ping",
        routes={
            "ping": PingPage(StateManager),
            "pong": PongPage(StateManager),
        }
    )
    
    SH1106Framework.begin(port=1, address=0x3C)
    pass
    
if __name__ == "__main__":
    __init()
```

<u>ping.py</u>

```python
from sh1106_framework import Drawing, State

import time

class PingPage(State):
    def __init__(self, state_manager):
        self.state_manager = state_manager
    
    def init(self):
        pass

    def enter(self):
        self.time_of_start = time.time()

    def update(self, dt):
        if time.time() - self.time_of_start > 1:
            self.state_manager.set_route("pong")

    def render(self):
        Drawing.draw_image("weather-rain", 0, 0)
        Drawing.draw_text("Ping", 14, 0)
```

<u>pong.py</u>

```python
from sh1106_framework import Drawing, State

import time

class PongPage(State):
    def __init__(self, state_manager):
        self.state_manager = state_manager
    
    def init(self):
        pass

    def enter(self):
        self.time_of_start = time.time()

    def update(self, dt):
        if time.time() - self.time_of_start > 1:
            self.state_manager.set_route("ping")

    def render(self):
        Drawing.draw_image("weather-storm", 0, 0)
        Drawing.draw_text("Pong", 14, 0)
```

### State Management

The state manager handles various states (which can be thought of as pages) that are referred to with strings (called routes) that they've been associated with. In the example above, "ping" has been assigned to a "PingPage" state and "pong" has been assigned to a "PongPage" state.

Notice in the example how they're set up in the main file:

```python
SH1106Framework.register_routes(
      default_route="splash",
      routes={
          "ping": PingPage(StateManager),
          "pong": PongPage(StateManager)
      }
  )
```



User-created states should follow this template, extending the State class:

```python
from sh1106_framework import State

class MyCustomState(State):
    def __init__(self, state_manager):
     		# This line is required
        self.state_manager = state_manager
    
    def init(self):
        # Initialization code

    def enter(self):
        # State entered code

    def update(self, dt):
        # Update code, runs approximately 60 times per second

    def render(self):
        # Render code
```

Within the states, you can use the methods `self.state_manager.set_route(route name)` and `self.state_manager.pop()` to set the current state or to go to the previous state.

### Drawing Graphics

You can draw various graphics like lines, images, rectangles, and strings, as well as set individual pixels. This should be done within the render method of a state. Note that where color is mentioned, it should be either 0 or 1, with 0 representing an unlit pixel and 1 representing a lit pixel.

The screen will be automatically cleared before each render method is run.

```python
from sh1106_framework import Drawing

# Draw rectangle
Drawing.draw_rect(x, y, width, height, color=1)

# Draw outlined rectangle
Drawing.draw_outlined_rect(x, y, width, height, color=1)

# Draw line
Drawing.draw_line(x0, y0, x1, y1, color=1)

# Set pixel
Drawing.set_pixel(x, y, color)

# Draw text (using font names defined in the main file)
Drawing.draw_text(text, x, y, color=1, font="default", scale=1, centered=False)

# Draw image (using image names defined in the reference JSON files)
Drawing.draw_image(image_name, x, y, color=1, scale=1, centered_horizontal=False, centered_vertical=False)
```

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](https://github.com/danspage/sh1106-framework/blob/main/LICENSE) file for details.
