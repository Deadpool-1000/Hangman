class InvalidInput(Exception):
    pass


class BadInputError(Exception):
    pass


class AlreadyExistsError(Exception):
    pass


class InvalidUsernameOrPasswordError(Exception):
    pass


class OutOfWordsError(Exception):
    pass


class NoSuchWordFoundError(Exception):
    pass


class ApplicationError(Exception):
    def __init__(self, code, message):
        self.code = code
        self.message = message


class DatabaseException(Exception):
    pass

