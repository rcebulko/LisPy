from abc import ABCMeta, abstractmethod
from numbers import Number

'''
Possible final result values of a Lisp expression
'''

class Val:
    """Lisp value type"""
    __metaclass__ = ABCMeta

    @abstractmethod
    def unwrap(self):
        pass

    def normalize(self):
        if issubclass(type(self), PrimFunV) or issubclass(type(self), FunV):
            return str(self)
        else:
            return self.unwrap()

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    @staticmethod
    def wrap(prim):
        if issubclass(type(prim), Val):
            # Anything that's already a valid type
            return prim
        elif type(prim) is bool:
            # Boolean values
            return BoolV(prim)
        if issubclass(type(prim), Number):
            # Numeric types
            return NumV(prim)
        elif type(prim) is list:
            # Cons list
            if len(prim) == 0:
                return BoolV(False)
            else:
                return ConsV(Val.wrap(prim[0]), Val.wrap(prim[1:]))
        else:
            # Lambda functions
            return PrimFunV(prim)

class BoolV(Val):
    """Boolean value"""
    def __init__(self, state):
        self.state = state

    def __str__(self):
        return "BoolV(" + str(self.state) + ")"
    def __repr__(self):
        return "t" if self.state else "nil"

    def unwrap(self):
        return self.state

class NumV(Val):
    """Number value"""
    def __init__(self, num):
        self.num = num

    def __str__(self):
        return "NumV(" + str(self.num) + ")"
    def __repr__(self):
        return str(self.num)

    def unwrap(self):
        return self.num

class ConsV(Val):
    """Pair of values"""
    def __init__(self, head, tail):
        self.head, self.tail = head, tail

    def __str__(self):
        return "ConsV(" + str(self.head) + ", " + str(self.tail) + ")"
    def __repr__(self):
        return "(cons " + repr(self.head) + " "  + repr(self.tail) + ")"

    def unwrap(self):
        if self.tail.unwrap():
            return [self.head] + self.tail.unwrap()
        else:
            return [self.head]

    def normalize(self):
        return [
            v.normalize() if issubclass(type(v), Val) else v
            for v in self.unwrap()
        ]

class SymV(Val):
    """Symbol value"""
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return "SymV(" + str(self.name) + ")"
    def __repr__(self):
        return "'" + self.name

    def unwrap(self):
        return "'" + self.name


class FunV(Val):
    """Function value"""
    def __init__(self, body, env):
        self.body, self.env = body, env

    def __str__(self):
        return repr(self)
    def __repr__(self):
        return "[user-defined function]"

    def unwrap(self):
        return lambda argVal: \
            self.body.eval([argVal] + self.env)

class PrimFunV(Val):
    """Primitive (native) function value"""
    def __init__(self, thunk):
        self.thunk = thunk

    def __str__(self):
        return repr(self)
    def __repr__(self):
        return "[native function]"

    def unwrap(self):
        return lambda argVal: \
            Val.wrap(self.thunk(argVal.unwrap()))