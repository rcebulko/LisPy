import unittest
from lisp_exceptions import *
from lisp_parser import Parser
from ast import *
from val import PrimFunV
from env import DeEnv

'''
Interpreter class to execute the parsing, compilation, and evaluation steps
'''

class Interpreter:
    """Full Lisp interpreter"""

    def __init__(self):
        self.primOps = {
            "+": lambda x: lambda y: x + y,
            "-": lambda x: lambda y: x - y,
            "*": lambda x: lambda y: x * y,
            "/": lambda x: lambda y: x / y,
            "eq?": lambda x: lambda y: x == y,
            "map": lambda f: lambda lst: map(f, lst),
            "max": lambda x: lambda y: max(x, y),
            "min": lambda x: lambda y: min(x, y),
            "not": lambda x: not x,
            "and": lambda x: lambda y: x and y,
            "or": lambda x: lambda y: x or y,
            ">": lambda x: lambda y: x > y,
            ">=": lambda x: lambda y: x >= y,
            "<": lambda x: lambda y: x < y,
            "<=": lambda x: lambda y: x <= y
        }

        self.initEnv = map(PrimFunV, self.primOps.values())
        self.initDeEnv = DeEnv.fromList(self.primOps.keys())

    def run(self, stx):
        # Parse input into abstract syntax tree
        try:
            parsed = Parser.parse(stx)
        except LispParsingException, e:
            raise e
        except Exception, e:
            raise LispParsingException(
                "parse",
                "encountered unknown error during parsing: " + str(e)
            )

        # Compile abstract syntax tree into core objects
        try:
            compiled = parsed.compile(self.initDeEnv)
        except LispCompilationException, e:
            raise e
        except Exception, e:
            raise LispCompilationException(
                "compile",
                "encountered unknown error during compilation: " + str(e)
            )

        # Evaluate core objects into a result value
        try:
            evaluated = compiled.eval(self.initEnv)
        except LispRuntimeException, e:
            raise e
        except Exception, e:
            raise LispRuntimeException(
                "eval",
                "encountered unknown error during runtime: " + str(e)
            )

        # Convert result values into native Python objects
        try:
            return evaluated.normalize()
        except LispRuntimeException, e:
            raise e
        except Exception, e:
            raise LispRuntimeException(
                "normalize",
                "encountered unknown error displaying result: " + str(e)
            )

'''
Tests!
'''

class InterpreterTest(unittest.TestCase):
    """Test class covering full interpreter functionality"""
    # It's worth noting that these are more valuable than all of the tests at
    # each individual level since they test the full stack and ensure every part
    # works together properly.

    def assertEqualRun(self, x, y):
        return self.assertEqual(self.interpreter.run(x), y)

    def assertTrueRun(self, b):
        return self.assertTrue(self.interpreter.run(b))

    def setUp(self):
        self.interpreter = Interpreter()

    def test_atomic(self):
        """Test that atomic data types evaluate correctly"""
        self.assertEqualRun("4", 4)
        self.assertEqualRun("t", True)
        self.assertEqualRun("nil", False)
        self.assertEqualRun("'hello", "'hello")
        self.assertEqualRun("(cons 1 (cons 2 (cons 3 nil)))", [1, 2, 3])

    def test_bools(self):
        """Test basic conditionals and boolean operations"""
        self.assertTrueRun("(not nil)")
        self.assertTrueRun("(and t t)")
        self.assertTrueRun("(or nil t)")
        self.assertTrueRun("(and t (or nil t))")
        self.assertEqualRun("(if (and t t) 'yes 'no)", "'yes")
        self.assertEqualRun("(if (not t) 'yes 'no)", "'no")
        self.assertEqualRun("""
            (cond (nil 'no)
                  (t 'this_one)
                  (t 'too_far))
        """, "'this_one")

    def test_arithmetic(self):
        """Test arithmetic operations (all of which are native functions)"""
        self.assertEqualRun("(+ (* 3 (- 2 1)) (/ 12 3))", 7)
        self.assertEqualRun("(max 0 (min 100 50))", 50)
        self.assertTrueRun("(eq? 7 7)")
        self.assertTrueRun("(not (eq? 7 8))")
        self.assertTrueRun("(< 7 8)")
        self.assertTrueRun("(not (> 1 8))")
        self.assertTrueRun("(<= 7 7)")
        self.assertTrueRun("(not (>= 7 8))")

    def test_lists(self):
        """Test cons and list operations"""
        self.assertEqualRun("(list 1 2 3 4)", [1, 2, 3, 4])
        self.assertEqualRun("(car (list 1 2 3 4))", 1)
        self.assertEqualRun("(car (cdr (cdr (list 1 2 3 4))))", 3)
        self.assertEqualRun(
            "(map not (list t nil nil t nil))",
            [False, True, True, False, True]
        )

    def test_funcs(self):
        """Test function calls and currying"""
        self.assertEqualRun("(((lambda (x y) (+ x y)) 1) 2)", 3)
        self.assertEqualRun("((lambda (x y) (+ x y)) 1 2)", 3)
        self.assertEqualRun("(let ((x 1) (y 2)) (+ x y))", 3)

    def test_recursive(self):
        """Test recursive definitions and calls"""
        self.assertEqualRun("""
            (let-rec (fact (lambda (x)
                             (if (<= x 1)
                                 1
                                 (* x (fact (- x 1))))))
                     (fact 5))
        """, 120)

if __name__ == '__main__':
    unittest.main()