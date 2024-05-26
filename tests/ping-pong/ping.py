from sh1106_framework import Drawing, State

import time

class PingPage(State):
    def __init__(self, state_manager):
        self.state_manager = state_manager
    
    def init(self):
        pass

    def enter(self):
        self.time_of_start = time.time()
        print("ENTERING THE PING STATE")

    def update(self, dt):
        # if time.time() - self.time_of_start > 1:
        #     self.state_manager.set_route("pong")
        pass

    def render(self):
        Drawing.draw_image("weather-rain", 0, 0)
        Drawing.draw_text("Ping", 14, 0)