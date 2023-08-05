import logging
from abc import ABCMeta, abstractmethod

logger = logging.getLogger('ezmysql')

__all__ = ['SqlOperation', 'UpdateSqlOperation', 'DeleteSqlOperation', 'CommonInsertOperation', 'QuerySqlOperation',
           'QueryObjOperation', 'DescTableOperation', 'FindOneOperation']


class SqlOperation:
    __metadata__ = ABCMeta

    @abstractmethod
    def operate(self, cursor):
        pass

    @staticmethod
    def _convert_value(value):
        if isinstance(value, bytearray):
            return value.decode('utf-8')
        return value


class UpdateSqlOperation(SqlOperation):
    __sql = None
    __params = None

    def __init__(self, sql: str, params: list = None):
        if params is None:
            params = []
        self.__sql = sql
        self.__params = params

    def operate(self, cursor):
        logger.debug(f'executing sql----->{self.__sql}')
        if self.__params:
            logger.debug(f'params------->{",".join([str(v) for v in self.__params])}')
        cursor.execute(self.__sql, self.__params)
        rc = cursor.rowcount
        logger.debug(f'updated row count<--------{rc}')
        return rc


class DeleteSqlOperation(UpdateSqlOperation):

    def __init__(self, sql: str, params: list = None):
        super().__init__(sql, params)


class CommonInsertOperation(UpdateSqlOperation):
    def __init__(self, sql: str, params: dict = None):
        super().__init__(sql, params)

    def operate(self, cursor):
        super().operate(cursor)
        return cursor.lastrowid


class QuerySqlOperation(SqlOperation):
    __sql = None
    __params = None
    __lowercase = False

    def __init__(self, sql: str, params: list = None, lowercase=False):
        if params is None:
            params = []
        sql = sql.strip()
        if not sql.upper().startswith('SELECT') and not sql.upper().startswith('DESC'):
            raise Exception('Invalid call query:{}'.format(sql))
        self.__sql = sql
        self.__params = params
        self.__lowercase = lowercase

    def operate(self, cursor):
        logger.debug(f'executing sql----->{self.__sql}')
        if self.__params:
            logger.debug(f'params------->{",".join([str(v) for v in self.__params])}')
        cursor.execute(self.__sql, self.__params)
        try:
            fetchall = cursor.fetchall()
            logger.debug(f'response rows<---------{len(fetchall)}')
            if not self.__lowercase:
                return fetchall
            else:
                return [self._lower_key(item) for item in fetchall]
        except any:
            return []

    @staticmethod
    def _lower_key(obj):
        return dict([(k.lower(), obj[k]) for k in obj])


class FindOneOperation(QuerySqlOperation):

    def __init__(self, sql: str, params: list = None, lowercase=False):
        super().__init__(sql, params, lowercase)

    def operate(self, cursor):
        data = super().operate(cursor)
        if len(data) > 1:
            raise Exception('find one get more than 1 result', self.__sql, self.__params)
        return None if len(data) == 0 else data[0]


class QueryObjOperation(FindOneOperation):
    def __init__(self, sql: str, params: list):
        super().__init__(sql, params)

    def operate(self, cursor):
        data = super().operate(cursor)
        if data is None:
            return None
        items = data.items()
        if len(items) > 1:
            raise Exception('Query object but result contains more than one key:{}'.format(data))
        return next(iter(data.values()))


class DescTableOperation(QuerySqlOperation):
    def __init__(self, table_name: str):
        if table_name.count('`') > 0:
            raise Exception('invalid table name:{}'.format(table_name))
        super().__init__('DESC `{}`'.format(table_name), lowercase=True)
