class Field:
    def __init__(self, column_type):
        self.column_type = column_type
        self.name = None

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__.get(self.name)

    def __set__(self, instance, value):
        instance.__dict__[self.name] = value


class IntegerField(Field):
    def __set__(self, instance, value):
        if not isinstance(value, int):
            raise TypeError(f"{self.name} must be int")
        super().__set__(instance, value)


class CharField(Field):
    def __set__(self, instance, value):
        if not isinstance(value, str):
            raise TypeError(f"{self.name} must be str")
        super().__set__(instance, value)


class Model:
    def save(self):
        fields = []
        values = []

        for key, value in self.__class__.__dict__.items():
            if isinstance(value, Field):
                fields.append(key)
                val = getattr(self, key)

                if isinstance(val, str):
                    val = f"'{val}'"

                values.append(val)

        table_name = self.__class__.__name__.lower()

        query = f"INSERT INTO {table_name} ({', '.join(fields)}) VALUES ({', '.join(map(str, values))});"
        print(query)


class User(Model):
    name = CharField("TEXT")
    age = IntegerField("INTEGER")


u = User()
u.name = "Davish"
u.age = 22
u.save()
