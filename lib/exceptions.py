

class ErrorMessageDisplayed(BaseException):

    def __init__(self, m):
        self.message = m

    def __str__(self):
        return self.message


class WarningMessageDisplayed(BaseException):

    def __init__(self, m):
        self.message = m

    def __str__(self):
        return self.message

