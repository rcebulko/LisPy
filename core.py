import unittest
from abc import ABCMeta, abstractmethod
from lisp_exceptions import LispRuntimeException
from val import *

'''
Compiled expressions which can be directly evaluated
'''

class CExpr:
    """Core expression data type"""
    __metaclass__ = ABCMeta

    @abstractmethod
    # Evaluate core expression into a Val
    def eval(self, env):
        pass

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

'''
Expressions related to booleans
'''

class CBool(CExpr):
    """Core boolean data type"""
    def __init__(self, state):
        self.state = state

    def __str__(self):
        return repr(self)
    def __repr__(self):
        return "CBool(" + str(self.state) + ")"

    def eval(self, env):
        # Simply wrap value in BoolV
        return BoolV(self.state)

class CIf(CExpr):
    """Core conditional data type"""
    def __init__(self, cond, ifBranch, elseBranch):
        self.cond, self.ifBranch, self.elseBranch = \
            cond, ifBranch, elseBranch

    def __str__(self):
        return repr(self)
    def __repr__(self):
        return "CIf(" + \
            str(self.cond) + ", " + \
            str(self.ifBranch) + ", " + \
            str(self.elseBranch) + ")"

    def eval(self, env):
        # It is very important we only evaluate one branch of the conditional
        b = self.cond.eval(env)
        if type(b) is BoolV:
            if b.state:
                return self.ifBranch.eval(env)
            else:
                return self.elseBranch.eval(env)
        else:
            raise LispRuntimeException(
                "eval",
                "expected a boolean when evaluating " + \
                str(cond) + \
                " but got " + \
                str(b)
            )

'''
Expressions related to arithmetic
'''

class CNum(CExpr):
    """Core number data type"""
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self)
    def __repr__(self):
        return "CNum(" + str(self.value) + ")"

    def eval(self, env):
        # Simply wrap value in NumV
        return NumV(self.value)

'''
Expressions related to cons
'''

class CCons(CExpr):
    """Core cons data type"""
    def __init__(self, head, tail):
        self.head, self.tail = head, tail

    def __str__(self):
        return repr(self)
    def __repr__(self):
        return "CCons(" + str(self.head) + ", " + str(self.tail) + ")"

    def eval(self, env):
        return ConsV(self.head.eval(env), self.tail.eval(env))

class CCar(CExpr):
    """Core car data type"""
    def __init__(self, pair):
        self.pair = pair

    def __str__(self):
        return repr(self)
    def __repr__(self):
        return "CCar(" + str(self.pair) + ")"

    def eval(self, env):
        # Evaluate the pair to fetch the head (make lazy later)
        return self.pair.eval(env).head

class CCdr(CExpr):
    """Core car data type"""
    def __init__(self, pair):
        self.pair = pair

    def __str__(self):
        return repr(self)
    def __repr__(self):
        return "CCdr(" + str(self.pair) + ")"

    def eval(self, env):
        # Evaluate the pair to fetch the tail (make lazy later)
        return self.pair.eval(env).tail

'''
Expressions related to functions
'''

class CFun(CExpr):
    """Core function data type"""
    def __init__(self, body):
        self.body = body

    def __str__(self):
        return repr(self)
    def __repr__(self):
        return "CFun(" + str(self.body) + ")"

    def eval(self, env):
        # Simply wrap value and scope in the appropriate Val to be called later
        return FunV(self.body, env)

class CPrimFun(CExpr):
    """Core primitive (native) function data type"""
    def __init__(self, thunk):
        self.thunk = thunk

    def __str__(self):
        return repr(self)
    def __repr__(self):
        return "CFun( [native code] )"

    def eval(self, env):
        return PrimFunV(self.thunk)

class CCall(CExpr):
    """Core function invocation data type"""
    def __init__(self, funExpr, argExpr):
        self.funExpr, self.argExpr = funExpr, argExpr

    def __str__(self):
        return repr(self)
    def __repr__(self):
        return "CCall(" + str(self.funExpr) + ", " + str(self.argExpr) + ")"

    def eval(self, env):
        fval = self.funExpr.eval(env)

        if type(fval) not in [FunV, PrimFunV]:
            raise LispRuntimeException(
                "eval",
                "'call' expects a function, got: " + str(fval)
            )

        fun = fval.unwrap()
        return fun(self.argExpr.eval(env))

'''
Expressions related to symbols
'''
class CSym(CExpr):
    """Core reference data type"""
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return repr(self)
    def __repr__(self):
        return "CSym(\"" + str(self.name) + "\")"

    def eval(self, env):
        # Get a value referenced in the environment based in its de-Bruijn index
        return SymV(self.name)

'''
Expressions related to references/de-Bruijn indices
'''

class CRef(CExpr):
    """Core reference data type"""
    def __init__(self, idx):
        self.idx = idx

    def __str__(self):
        return repr(self)
    def __repr__(self):
        return "CRef(" + str(self.idx) + ")"

    def eval(self, env):
        # Get a value referenced in the environment based in its de-Bruijn index
        return Val.wrap(env[self.idx])

'''
Tests!
'''

class CoreTest(unittest.TestCase):
    '''Test class for all CExpr subclasses'''
    def assertEqualEval(self, x, y, env):
        return self.assertEqual(x.eval(env), y.eval(env))

    def assertTrueEval(self, b, env):
        return self.assertTrue(b.eval(env))

    def setUp(self):
        self.testEnv = [NumV(x) for x in [1, 1, 2, 3, 5, 8, 13, 21]]

    def test_if(self):
        self.assertEqualEval(
            CIf(CBool(True),
                CNum(5),
                CNum(10)
            ),
            CNum(5),
            []
        )

        self.assertEqualEval(
            CIf(CBool(False),
                CNum(5),
                CNum(10)
            ),
            CNum(10),
            []
        )

    def test_cons(self):
        self.assertEqualEval(
            CCar(CCdr(
                CCons(CNum(1), CCons(CNum(2), CCons(CNum(3), CBool(False))))
            )),
            CNum(2),
            []
        )

    def test_fun_call(self):
        self.assertEqualEval(
            CCall(
                CCall(
                    CPrimFun(lambda x: lambda y: x + y),
                    CRef(7)
                ),
                CRef(6)
            ),
            CNum(34),
            self.testEnv
        )

        self.assertEqualEval(
            CCall(
                CCall(
                    CPrimFun(lambda x: lambda y: x - y),
                    CNum(2)
                ),
                CNum(2)
            ),
            CNum(0),
            []
        )

    def test_ref(self):
        env = self.testEnv

        self.assertEqualEval(CRef(3), CNum(3), env)
        self.assertEqualEval(CRef(6), CNum(13), env)

if __name__ == "__main__":
    unittest.main()