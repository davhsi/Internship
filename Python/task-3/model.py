from db import get_connection
from query import QuerySet
from fields import Field, ForeignKey


class ModelMeta(type):
    def __new__(mcs, class_name, bases, attrs):
        cls = super().__new__(mcs, class_name, bases, attrs)
        if class_name == "Model":
            return cls

        cls._meta_ = type("_meta", (), {})()
        cls._meta_.table_name = class_name.lower()
        cls._meta_.fields = {}

        for attr_name, attr_value in attrs.items():
            if isinstance(attr_value, Field):
                cls._meta_.fields[attr_name] = attr_value
                if isinstance(attr_value, ForeignKey):
                    related_name = attr_value.related_name or f"{class_name.lower()}_set"
                    setattr(
                        attr_value.to_model,
                        related_name,
                        property(lambda self, m=cls, f=attr_name: m.filter(**{f: self.id})),
                    )

        for base in bases:
            if hasattr(base, "_meta_"):
                cls._meta_.fields.update(base._meta_.fields)

        return cls


class Model(metaclass=ModelMeta):
    def __init__(self, **kwargs):
        self.id = None
        for key, value in kwargs.items():
            if key not in self._meta_.fields:
                raise TypeError(f"{type(self).__name__} has no field '{key}'")
            field = self._meta_.fields[key]
            self.__dict__[key] = value.id if isinstance(field, ForeignKey) and hasattr(value, "id") else value

    def __getattr__(self, name):
        field = self._meta_.fields.get(name)
        if isinstance(field, ForeignKey):
            fk_id = self.__dict__.get(name)
            return None if fk_id is None else QuerySet(field.to_model).filter(id=fk_id).first()
        raise AttributeError(f"'{type(self).__name__}' has no attribute '{name}'")

    def __repr__(self):
        parts = [f"id={self.id}"] if self.id else []
        parts += [f"{name}={self.__dict__.get(name)!r}" for name in self._meta_.fields]
        return f"{type(self).__name__}({', '.join(parts)})"

    @classmethod
    def create_table(cls):
        cols = ["id INTEGER PRIMARY KEY AUTOINCREMENT"] + [
            f"{name} {field.to_sql()}" for name, field in cls._meta_.fields.items()
        ]
        sql = f"CREATE TABLE IF NOT EXISTS {cls._meta_.table_name} ({', '.join(cols)});"
        conn = get_connection()
        conn.execute(sql)
        conn.commit()

    def save(self):
        meta = self._meta_
        fields = list(meta.fields.keys())
        values = [self.__dict__.get(f) for f in fields]
        conn = get_connection()

        if self.id is None:
            placeholders = ", ".join("?" for _ in fields)
            sql = f"INSERT INTO {meta.table_name} ({', '.join(fields)}) VALUES ({placeholders})"
            self.id = conn.execute(sql, values).lastrowid
        else:
            set_clause = ", ".join(f"{f} = ?" for f in fields)
            sql = f"UPDATE {meta.table_name} SET {set_clause} WHERE id = ?"
            conn.execute(sql, values + [self.id])

        conn.commit()
        return self

    def delete(self):
        if self.id is None:
            raise ValueError("Cannot delete unsaved object")
        conn = get_connection()
        conn.execute(f"DELETE FROM {self._meta_.table_name} WHERE id = ?", (self.id,))
        conn.commit()
        self.id = None

    @classmethod
    def filter(cls, **kwargs):
        return QuerySet(cls).filter(**kwargs)

    @classmethod
    def all(cls):
        return QuerySet(cls).all()

    @classmethod
    def get(cls, **kwargs):
        results = cls.filter(**kwargs).limit(1).all()
        return results[0] if results else None
