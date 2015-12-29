# -*- coding: utf-8 -*-

"""
What's a decorator:
- decorator is a function that takes another function as input and return a new function as output:
    obj = decorator(obj) # obj can be function or class
- closure is used inside decorator to create a new function.
  So, we can access input function and decorator parameters inside the closure
- decorator can be implemented as function or class, with or without parameters
- a rule of thumb:
    don't change the semantic of the input function when using decorator
    
What's a closure:
- Closure is a fancy term meaning that when a function is declared,
  it maintains a reference to the lexical environment in which it was declared.

Common pratices:
- check parameters: e.g. assertion, range check
- debugging, logging or timing: log function call
- hook or lock acquire/release: entry and exit hooks
- cache result

"""

import sys

def decorator_func_no_params(fn):
    def fn_wrapper(*args, **kwargs):
        print "@before '%s()'" % fn # fn.__name__
        result = fn(*args, **kwargs)
        print "@after '%s()'" % fn # fn.__name__
        return result
    return fn_wrapper
    pass
    
def decorator_func_with_params(arg1, arg2):
    def fn_decorator(fn):
        def fn_wrapper(*args, **kwargs):
            print "@before '%s(%r, %r)'" % (fn, arg1, arg2)
            result = fn(*args, **kwargs)
            print "@after '%s(%r, %r)'" % (fn, arg1, arg2)
            return result
        return fn_wrapper
    return fn_decorator
    pass
    
class decorator_class_no_params:
    def __init__(self, fn): # take fn on initialization
        self.fn = fn
    
    def __call__(self, *args, **kwargs):
        print "@before '%s()'" % self.fn
        result = self.fn(*args, **kwargs)
        print "@after '%s()'" % self.fn
        return result
    pass
    
class decorator_class_with_params:
    def __init__(self, arg1, arg2): # take params on initialization
        self.arg1 = arg1
        self.arg2 = arg2
    
    def __call__(self, fn): # take fn in __call__ function
        def fn_wrapper(*args, **kwargs):
            print "@before '%s(%r, %r)'" % (fn, self.arg1, self.arg2)
            result = fn(*args, **kwargs)
            print "@after '%s(%r, %r)'" % (fn, self.arg1, self.arg2)
            return result
        return fn_wrapper
    pass

@decorator_func_with_params('hi', 'there')
@decorator_func_no_params
def hello1():
    print 'inside %s() function...' % sys._getframe().f_code.co_name



@decorator_class_no_params
@decorator_class_with_params('hi', 'there')
def hello2():
    print 'inside %s() function...' % sys._getframe().f_code.co_name

if __name__ == '__main__':
    hello1()
    print '======================='
    hello2()
