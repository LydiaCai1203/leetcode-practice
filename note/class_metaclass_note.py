附上原文链接：
href: https://stackoverflow.com/questions/100003/what-are-metaclasses-in-python

--------------
以下是我看完这篇文章的一些总结
2019-04-11 这篇文章真的让我涨姿势了(另：周星星的歌真的好听啊，有恋爱的感觉哈哈哈哈)
some note about class
1. Classes in Python are objects too, it will be created as soon as u use the keyword class to define an Class
2. u can asign it to a variable
3. u can copy it
4. u can add attributes to it
5. u can pass it as a function parameter
6. hasattr(Class_name, parameter_name_string)
7. since Classes are objs, so u can create them on the fly(on runtime)
example but not so dynamic:
def choose_class(name):
    if name == 'foo':
        class Foo(object):
            pass
        return Foo
    else:
        class Bar(object):
            pass
        return Bar
8. type()
type can create classes on the fly,type can take the description of a class as parameters
and return a class. u can use it directly
9. someone say that it's silly that the same function can have two completely different
uses according to the parameters u pass to it.
10. MyShinyClass = type('MyShinyClass', (), {'name': 'caiqj'}) can create class on the fly
11. FooChild = type('FooChild', (Foo,), {}) # inherit
12. def echo_bar(self):  # create func_member
        print(self.bar)
    FooChild = type('FooChild', (Foo,), {'echo_bar': echo_bar})
--------------
1. we know class is object, metaclasses are that create these objects
2. cause type() is in fact a metaclass Python uses to create all classes behind the scenes
3. str the class that creates string objects, int the class that creates integer objects,
type is just the class that creates class objects
4. u can use __class__ check everything of obj
5. and obviously obj.__class__.__clas__ is type
6. class Foo(object, metaclass=something)
pass attributes as keyword-arguments into a metaclass, like so:
class Foo(object, metaclass=something, kwarg1=value1, kwarg2=value2):
    ...
7. the main purpose of metaclass is to change the class automatically, when it's created
8. __new__() is the method called before __init__
9. def __new__(upperattr_metaclass, future_class_name,
                future_class_parents, future_class_attr):
        uppercase_attr = {}
        for name, val in future_class_attr.items():
            if not name.startswith('__'):
                uppercase_attr[name.upper()] = val
            else:
                uppercase_attr[name] = val
        return type(future_class_name, future_class_parents, uppercase_attr)
if u want to control how the object is created.
----------------
last words:
if u want change classes, there are three different ways
1. metaclasses
2. monkey patching
3. class decorators




































