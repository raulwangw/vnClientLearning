from qtdDataType import *
from ctypes import *
import ctypes as ct
import win32api


def xxx((n,a,b)):
    print("n = %d"%n)
    print("a = %s"%a)

def yyy((m,n,q,b)):
    print(m)
    print(n)
    print(q)
    print(b)

def ttt():
    return 1,"2g",3

def mmm():
    return 2,"3g","pkq",[7,8]

class test(object):
    def __init__(self):
        
        pass
    
    def _test(self):
        print("__test")

class testA(object):
    val=2

if __name__ == "__main__":
    a={"a":1}
    count=9
    x = (create_string_buffer(256))
    print(x)
