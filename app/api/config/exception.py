class ModelNotFound(Exception):
    def __init__(self, id: int, message="Model with given id was not found") -> None:
        super().__init__(message)

class PoolNotFound(Exception):
    def __init__(self, id: int, message="Pool with given id was not found") -> None:
        super().__init__(message)