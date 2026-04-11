class MyDescriptor:
    def __get__(self, instance, owner):
        # print(instance) #obj
        # print(owner) # MyClass
        print("Getting value")
        return instance._value

    def __set__(self, instance, value):
        print("Setting value:", value)
        instance._value = value


class MyClass:
    x = MyDescriptor()


# obj = MyClass()
# # print(obj.x)

# obj.x = 20
# print(obj.x)

# print(help(MyClass)))


class PositiveNumber:
    def __get__(self, instance, owner):
        return instance._value

    def __set__(self, instance, value):
        if value < 0:
            raise ValueError("Must be positive")
        instance._value = value


class Product:
    price = PositiveNumber()


p = Product()
# p.price = 100
# p.price = -10

"""
Data Descriptor -> defines :  __get__ and __set__ 
- Takes priority over instance variables

Non-Data Descriptor -> defines: __get__
- Can be overriden by instance variables

"""


class D:
    def __get__(self, instance, owner):
        return "from descriptor"


class C:
    x = D()


obj = C()
obj.x = "instance value"

# print(obj.x)  # prints instance value because non data descriptor


class Typed:
    def __init__(self, expected_type):
        self.expected_type = expected_type

    def __set__(self, instance, value):
        if not isinstance(value, self.expected_type):
            raise TypeError("Wrong Type")
        instance.__dict__["value"] = value
        
    def __get__(self, instance, owner):
        return instance.__dict__.get("value")

class Person:
    age = Typed(int)
    
p = Person()
p.age = 20
# p.age = "abc"
