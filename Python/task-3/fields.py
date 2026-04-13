class Field:
    def __init__(self, nullable=False, default=None, unique=False):
        self.nullable = nullable
        self.default = default
        self.unique = unique

    def _constraints(self):
        parts = []
        if not self.nullable:
            parts.append("NOT NULL")
        if self.unique:
            parts.append("UNIQUE")
        return parts

    def to_sql(self):
        raise NotImplementedError()


class CharField(Field):
    def __init__(self, max_length=255, **kwargs):
        super().__init__(**kwargs)
        self.max_length = max_length

    def to_sql(self):
        return " ".join([f"VARCHAR({self.max_length})"] + self._constraints())


class IntegerField(Field):
    def to_sql(self):
        return " ".join(["INTEGER"] + self._constraints())


class ForeignKey(Field):
    def __init__(self, to_model, related_name=None, on_delete="CASCADE", **kwargs):
        super().__init__(**kwargs)
        self.to_model = to_model
        self.related_name = related_name
        self.on_delete = on_delete

    def to_sql(self):
        table = self.to_model.__name__.lower()
        return " ".join(
            ["INTEGER"] + self._constraints() + [f"REFERENCES {table}(id) ON DELETE {self.on_delete}"]
        )
