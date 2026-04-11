class Field:
    def __init__(self):
        self.name = None

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        print(f"[GET] {self.name}")
        return instance.__dict__.get(self.name)

    def __set__(self, instance, value):
        print(f"[SET] {self.name} = {value}")
        instance.__dict__[self.name] = value


class ModelMeta(type):
    def __new__(cls, name, bases, dct):
        print(f"\n[Metaclass] Creating class: {name}")

        fields = {}

        for key, value in dct.items():
            if isinstance(value, Field):
                fields[key] = value

        dct["_fields"] = fields

        print(f"[Metaclass] Found fields: {list(fields.keys())}")

        return super().__new__(cls, name, bases, dct)


class Model(metaclass=ModelMeta):
    def save(self):
        print("\n[SAVE CALLED]")
        for field in self._fields:
            value = getattr(self, field)
            print(f"{field} = {value}")

class User(Model):
    name = Field()
    age = Field()


u = User()

u.name = "Davish"
u.age = 22

print(u.name)
print(u.age)

u.save()