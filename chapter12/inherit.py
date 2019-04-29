"""
1. 基本上，内置类型的方法不会调用子类覆盖的方法。比如，dict的子类覆盖的__getitem__()不会被内置类型的get()所调用
2. 
"""
class DoppelDict(dict):
    def __setitem__(self, key, value):
        super().__setitem__(key, [value] * 2)
