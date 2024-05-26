from abc import ABC, abstractmethod

class State(ABC):
    """
    The base class for all states in the framework. All states must inherit from
    this class. The framework will automatically initialize the state upon
    entering it. The user can manually set the state using the set_state function
    in the state manager.
    """
    
    initialized = False
    
    @abstractmethod
    def init(self) -> None:
        """
        A function that gets run once upon initialization of the framework.
        """
        pass

    @abstractmethod
    def enter(self) -> None:
        """
        A function that gets run once each time the state is entered.
        """
        pass

    @abstractmethod
    def update(self, dt: float) -> None:
        """
        A function that gets run each time the state is updated, approximately
        60 times per second. The exact delta time is given in seconds.
        
        Parameters
        ----------
        dt: float
            The delta time in seconds.
        """
        pass

    @abstractmethod
    def render(self) -> None:
        """
        A function that gets run each time the state is rendered, which is
        immediately after every update, approximately 60 times per second.
        """
        pass