from domains.error.lambda_exception import LambdaException


class UserNotFoundException(LambdaException):
    def __init__(self, message, cause):
        super().__init__(message, cause)


class UserAlreadyExistsException(LambdaException):
    def __init__(self, message, cause):
        super().__init__(message, cause)
