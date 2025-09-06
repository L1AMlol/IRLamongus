class Player:
    def __init__(self):
        # ********** property name - (setter/getter) ***********
        @property
        def name(self) -> str:
            """ The name property. """
            return self.__name
        
        @name.setter
        def name(self, value: str) -> None:
            self.__name = value

        # ********** property is_ready - (setter/getter) ***********
        @property
        def is_ready(self) -> bool:
            """ The is_ready property. """
            return self.__is_ready
        
        @is_ready.setter
        def is_ready(self, value: bool) -> None:
            self.__is_ready = value
        