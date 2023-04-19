class InvalidCommandInput(Exception):
    """Exection raised when an operations is called with invalid values"""

    def __init__(self, message="Invalid input") -> None:
        self.message = message
        super().__init__(self.message)


class RandomStringOperationException(Exception):
    """Exception raised when external service's quota is exceeded"""

    def __init__(self, message="Random String operation error") -> None:
        self.message = message
        super().__init__(self.message)
