__all__ = [
    "NotEnoughArgumentError",
]


class CmdBaseException(Exception):
    def __init__(self, message: str, *args):
        self.message = message
        self.args = args
        super().__init__(self.message)

    def __str__(self):
        return self.message


class NotEnoughArgumentError(CmdBaseException):
    def __init__(self, message: str, option: str):
        self.message = message
        self.option = option
        super().__init__(message)
