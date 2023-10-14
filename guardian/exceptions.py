class ValidationError(Exception):
    def __init__(self, message="A validation error occured", data = None) -> None:
        self.message=message
        self.data=data
        super().__init__(self.message)
        
class InitializationError(Exception):
    def __init__(self, message="A initialization error occured") -> None:
        self.message=message
        super().__init__(self.message)