import os

absPath = os.path.dirname(os.path.abspath(__file__))

def define_shared(name, value):
    globals()[name] = value
