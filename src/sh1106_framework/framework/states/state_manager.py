from graphics.drawing import Drawing
from framework.states.state import State

class StateManager:
    """
    The state manager is responsible for managing the state of the application.
    It handles the initialization, entering, updating, and rendering of the
    current state. These are done automatically by the SH1106Framework, however
    the user can manually set the state using the set_state and pop methods.
    """
    
    __states: dict[str, State] = {}
    
    @staticmethod
    def _init(default_route: str, routes: dict[str, State]) -> None:
        # Define routes here
        for page in routes:
            StateManager.__states[page] = routes[page]
        
        StateManager.__current_state = default_route
        StateManager.__previous_state = default_route

        
        # Initializes the default route afterwards
        StateManager.__states[StateManager.__current_state].initialized = True
        StateManager.__states[StateManager.__current_state].init()
        
    @staticmethod
    def set_state(route_name):
        """
        Sets the current state to the given route name.
        
        Parameters
        ----------
        route_name: str
            The name of the route to set the current state to.
        """
        StateManager.__previous_state = StateManager.__current_state
        
        if not StateManager.__states[route_name].initialized:
            StateManager.__states[route_name].initialized = True
            StateManager.__states[route_name].init()
        
        StateManager.__states[route_name].enter()
        
        StateManager.__current_state = route_name
        
    @staticmethod
    def pop():
        """
        Sets the current state to the previous state. Nothing happens if there is
        no previous state.
        """
        StateManager.set_state(StateManager.__previous_state)
    
    @staticmethod
    def _update(dt):
        StateManager.__states[StateManager.__current_state].update(dt)
    
    @staticmethod
    def _render():
        Drawing._update_contrast()
        Drawing.clear()
        StateManager.__states[StateManager.__current_state].render()
        Drawing._render()