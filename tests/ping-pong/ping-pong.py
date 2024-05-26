from sh1106_framework import SH1106Framework, StateManager
from ping import PingPage
from pong import PongPage

def __init():
    SH1106Framework.register_font("default", "assets/default_font.json")
    SH1106Framework.register_images("assets/icons.json")
    
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