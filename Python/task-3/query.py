_OPERATORS = {"_gte": ">=", "_lte": "<=", "_gt": ">", "_lt": "<"}


class QuerySet:
    def __init__(self, model_class):
        self.model_class = model_class
        self.meta = model_class._meta_
        self._where = []
        self._order_by = None
        self._limit = None
        self._offset = None

    def filter(self, **kwargs):
        for key, value in kwargs.items():
            field, op = key, "="
            for suffix, sql_op in _OPERATORS.items():
                if key.endswith(suffix):
                    field = key[: -len(suffix)]
                    op = sql_op
                    break
            self._where.append((field, op, value))
        return self

    def order_by(self, field):
        if field.startswith("-"):
            self._order_by = f"{field[1:]} DESC"
        else:
            self._order_by = f"{field} ASC"
        return self

    def limit(self, n):
        self._limit = n
        return self

    def offset(self, n):
        self._offset = n
        return self

    def _build_sql(self):
        parts = [f"SELECT * FROM {self.meta.table_name}"]
        if self._where:
            parts.append("WHERE " + " AND ".join(f"{f} {op} ?" for f, op, _ in self._where))
        if self._order_by:
            parts.append(f"ORDER BY {self._order_by}")
        if self._limit:
            parts.append(f"LIMIT {self._limit}")
        if self._offset:
            parts.append(f"OFFSET {self._offset}")
        return " ".join(parts) + ";", [v for _, _, v in self._where]

    def _rows_to_instances(self, rows, columns):
        instances = []
        for row in rows:
            inst = self.model_class.__new__(self.model_class)
            inst.__dict__["id"] = row[0]
            for i, col in enumerate(columns[1:], 1):
                inst.__dict__[col] = row[i] if i < len(row) else None
            instances.append(inst)
        return instances

    def all(self):
        from db import get_connection
        sql, params = self._build_sql()
        cursor = get_connection().execute(sql, params)
        columns = [d[0] for d in cursor.description] if cursor.description else ["id"]
        return self._rows_to_instances(cursor.fetchall(), columns)

    def first(self):
        results = self.limit(1).all()
        return results[0] if results else None
