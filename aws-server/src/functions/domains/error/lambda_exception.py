import string


class LambdaException(Exception):
    def __init__(self, message: string, cause: Exception):
        super().__init__(message)
        self.cause = cause


class InvalidParameterError(LambdaException):
    def __init__(self, cause):
        self.message = 'Parameter validation failed.'
        super().__init__(message=self.message, cause=cause)


class UnknownTopicNameException(LambdaException):
    def __init__(self, cause, source_topic):
        self.message = source_topic
        super().__init__(message=self.message, cause=cause)
