class SystemEvent:
    """
    Represents a generic event with a type and optional custom attributes.

    Attributes:
        type (str): The type or name of the event.
        Other attributes are dynamically added via keyword arguments.
    """

    def __init__(self, type, **kwargs):
        """
        Initialize a new Event object.

        Args:
            type (str): The type or name of the event.
            **kwargs: Arbitrary keyword arguments that will be set as attributes of the event.

        """
        self.type = type 
        for kwarg in kwargs:
            setattr(self, kwarg, kwargs[kwarg])