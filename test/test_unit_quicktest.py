import unittest
import os

#https://stackoverflow.com/questions/27219439/please-what-does-func-mean-in-python-when-used-inside-a-function#:~:text=func%20is%20an%20argument%20given,func%20when%20it%20is%20run.
def standard_function(self=None):
    return "standard_function"

def curry (prior, *additional):
    def curried(*args):
        return prior(*(args + additional))
    return curried

class A:
    def __init__(self):
        self.function_to_be_defined = None

    def hello(self):
        return "hello"

    def hello2(self, a, b):
        return f'Hello {a} {b}'

    def hello3(self, a, b, c):
        return a(b,c)

    def hello4(self, function_a, a, b):
        self.function_to_be_defined = curry(function_a, a, b)
        return None

    def hello5(self, function_a, *args):
        self.function_to_be_defined = curry(function_a, *args)
        return None

# Quick File for testing out concepts before using them in project
class Test_Unit_QuickTest(unittest.TestCase):

    def test_get_raw_data(self):
        A.hello = standard_function
        self.assertEqual(A().hello(), "standard_function")
        self.assertEqual(A().hello2("a", "b"),"Hello a b" )
        a = A()
        a.hello4(a.hello2, 'a', 'b')
        self.assertEqual(a.function_to_be_defined(),"Hello a b" )
        b = A()
        b.hello5(b.hello2, 'b')
        self.assertEqual(b.function_to_be_defined('a'),"Hello a b" )

        c = A()
        c.hello5(c.hello2, 'a', 'b')
        self.assertEqual(c.function_to_be_defined(),"Hello a b" )


if __name__ == '__main__':
    unittest.main()
