class LispException(Exception):
    """An exception caused by the Lisp interpreter"""
    def __init__(self, func, msg):
        self.msg, self.func = msg, func

    def __str__(self):
        return self.func + ": " + self.msg


class LispRuntimeException(LispException):
    """Runtime exception within interpreter"""
    def __init__(self, func, msg):
        self.msg, self.func = msg, func

    def __str__(self):
        return self.func + ": " + self.msg

class LispCompilationException(LispException):
    """Exception occuring during the compilation/preprocessing stage"""
    def __init__(self, func, msg):
        self.msg, self.func = msg, func

    def __str__(self):
        return self.func + ": " + self.msg

class LispParsingException(LispException):
    """Exception occuring during the parsing stage"""
    def __init__(self, func, msg):
        self.msg, self.func = msg, func

    def __str__(self):
        return self.func + ": " + self.msg