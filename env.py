import unittest
from abc import ABCMeta, abstractmethod
from lisp_exceptions import LispCompilationException

'''
Environments to handle symbol lookup and scoping
'''

class DeEnv:
    """Syntactic environments for the de-Bruijn preprocessing"""
    __metaclass__ = ABCMeta

    @abstractmethod
    def lookup(self, id):
        pass

    @staticmethod
    def fromList(ids):
        if len(ids) == 0:
            return DeEmptyEnv()
        else:
            return DeExtend(
                DeEnv.fromList(ids[1:]),
                ids[0]
            )

class DeEmptyEnv(DeEnv):
    """Empty environment"""

    def lookup(self, id):
        raise LispCompilationException("lookup", "free identifier: " + id)

class DeExtend(DeEnv):
    """de-Bruijn indexed environment"""
    def __init__(self, tail, head):
        self.tail, self.head = tail, head

    def lookup(self, id):
        if id == self.head:
            return 0
        else:
            return 1 + self.tail.lookup(id)

'''
Tests!
'''

class EnvTest(unittest.TestCase):
    '''Test class for all DeEnv classes'''
    def test_extend(self):
        e = DeExtend(DeExtend(DeEmptyEnv(), "b"), "a")
        self.assertEqual([0, 1], [e.lookup(s) for s in ["a", "b"]])

    def test_empty(self):
        exceptCaught = False

        try:
            DeEmptyEnv().lookup("x")
        except LispCompilationException, e:
            exceptCaught = True

        self.assertTrue(exceptCaught)

    def test_deEnvFromList(self):
        self.assertEqual(
            DeEnv.fromList(["x", "y", "z"]).lookup("z"),
            2
        )

if __name__ == "__main__":
    unittest.main()