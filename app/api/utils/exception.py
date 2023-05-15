class ModelNotFound(Exception):
    def __init__(self, id: int, message="Model with given id was not found") -> None:
        super().__init__(message)
        self.id = id


class PoolNotFound(Exception):
    def __init__(self, id: int, message="Pool with given id was not found") -> None:
        super().__init__(message)
        self.id = id


class UserNotFound(Exception):
    def __init__(self, id: int, message="User with given id was not found") -> None:
        super().__init__(message)
        self.id = id


class GateNotFound(Exception):
    def __init__(self, id: int, message="Gate with given id was not found") -> None:
        super().__init__(message)
        self.id = id


class TestNotFound(Exception):
    def __init__(self, id: int, message="Test with given id was not found") -> None:
        super().__init__(message)
        self.id = id
