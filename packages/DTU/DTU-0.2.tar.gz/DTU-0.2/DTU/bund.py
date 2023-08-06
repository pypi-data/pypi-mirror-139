import numpy as np

class shrek_class:
    def __init__(self):
        self.name = "shrek"
    
    def say_hello(self):
        return "Hello im " + self.name

def numpy_test_func(arr):
    return np.mean(arr)