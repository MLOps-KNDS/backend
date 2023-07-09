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


class PingLimitReached(Exception):
    def __init__(
        self,
        ping_number: int,
        message="Ping limit reached",
    ) -> None:
        super().__init__(message)
        self.ping_number = ping_number


class ErrImagePull(Exception):
    def __init__(
        self,
        image_tag: str,
        message="Image pull error",
    ) -> None:
        super().__init__(message)
        self.image_tag = image_tag


class EmptyList(Exception):
    def __init__(
        self,
        message="Empty list",
    ) -> None:
        super().__init__(message)


class ErrImageNeverPull(Exception):
    def __init__(
        self,
        message="Image never pulled! Checkout imagePullPolicy or image tag!",
    ) -> None:
        super().__init__(message)
