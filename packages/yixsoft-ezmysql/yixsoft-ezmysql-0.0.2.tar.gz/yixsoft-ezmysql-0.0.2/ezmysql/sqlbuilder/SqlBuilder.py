from abc import ABCMeta, abstractmethod

__all__ = ['SqlBuilder']


class SqlBuilder:
    __metadata__ = ABCMeta
    _query: list = None

    def __init__(self):
        self._query = []

    def where_equals(self, column: (str, list), params: dict):
        self._check_valid_column(column)
        if isinstance(column, list):
            self.where([self._where_item(col, params) for col in column])
        else:
            self.where(self._where_item(column, params))
        return self

    @staticmethod
    def _where_item(column: str, params: dict):
        val = params.get(column)
        if val is None:
            return f'`{column}` is null'
        else:
            return f'`{column}`=%s'

    def where(self, fragment: (str, list)):
        if isinstance(fragment, list):
            self._query += fragment
        else:
            self._query.append(fragment)
        return self

    def _build_where_fragments(self):
        return ' and '.join([self._wrap_(fragm, '(', ')') for fragm in self._query])

    @staticmethod
    def insert_into(table_name: str):
        return InsertSqlBuilder(table_name)

    @staticmethod
    def update(table_name: str):
        return UpdateSqlBuilder(table_name)

    @staticmethod
    def select_from(table_name: str):
        return SelectSqlBuilder(table_name)

    @staticmethod
    def delete_from(table_name: str):
        return DeleteSqlBuilder(table_name)

    @abstractmethod
    def build(self):
        pass

    @staticmethod
    def _wrap_(content: str, open_symbol: str, close_symbol: str = None):
        if close_symbol is None:
            close_symbol = open_symbol
        return open_symbol + content + close_symbol

    @staticmethod
    def _check_valid_column(column: (str, list)):
        invalid_characters = ['`', '*']
        if isinstance(column, list):
            for col in column:
                if not col.isprintable() or max([col.count(c) for c in invalid_characters]) > 0:
                    raise Exception('invalid column name:{}'.format(col))
        else:
            if column.count('`') > 0:
                raise Exception('invalid column name:{}'.format(column))


class InsertSqlBuilder(SqlBuilder):
    __table = None
    __columns = None

    def __init__(self, table_name: str):
        super().__init__()
        if table_name.count('`') > 0:
            raise Exception('Invalid table name:{}'.format(table_name))
        self.__table = table_name
        self.__columns = []

    def where(self, fragment):
        raise Exception('Unsupported operation')

    def values(self, column: (str, list)):
        self._check_valid_column(column)
        if isinstance(column, list):
            self.__columns += column
        else:
            self.__columns.append(column)
        return self

    def build(self):
        tpl = "insert into `{}` ({}) values ({})"
        return tpl.format(self.__table, ','.join([self._wrap_(col, '`') for col in self.__columns]),
                          ','.join(['%s'] * len(self.__columns)))


class UpdateSqlBuilder(SqlBuilder):
    __table: str = None
    __setters: list = None

    def __init__(self, table: str):
        super().__init__()
        if table.count('`') > 0:
            raise Exception('Invalid table name:{}'.format(table))
        self.__table = table
        self.__setters = []

    def set(self, column: (str, list)):
        self._check_valid_column(column)
        if isinstance(column, list):
            self.__setters += column
        else:
            self.__setters.append(column)
        return self

    def build(self):
        tpl = 'update `{}` set {} where {}'
        return tpl.format(self.__table,
                          ','.join([self.__set_fragment(col) for col in self.__setters]),
                          self._build_where_fragments())

    def __set_fragment(self, column: str):
        return self._wrap_(column, '`') + '=%s'


class SelectSqlBuilder(SqlBuilder):
    __table: str = None
    __selects: list = None

    def __init__(self, table_name: str):
        super().__init__()
        self.__table = table_name
        self.__selects = []

    def select_column(self, column: (str, list)):
        self._check_valid_column(column)
        if isinstance(column, list):
            self.__selects += column
        else:
            self.__selects.append(column)
        return self

    def build(self):
        column_params = ','.join([self._wrap_(col, '`') for col in self.__selects]) if len(self.__selects) > 0 else '*'
        tpl = f'select {column_params} from `{self.__table}` '
        if len(self._query) > 0:
            tpl += 'where ' + self._build_where_fragments()
        return tpl


class DeleteSqlBuilder(SqlBuilder):
    __table: str = None

    def __init__(self, table_name: str):
        super().__init__()
        self.__table = table_name

    def build(self):
        tpl = 'delete from `{}` where {}'
        return tpl.format(self.__table,
                          self._build_where_fragments())
