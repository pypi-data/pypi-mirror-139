import logging
from abc import ABCMeta, abstractmethod

from ..sqlbuilder import SqlBuilder
from .SqlOperation import *
from ..TableCache import TableStructureCache

logger = logging.getLogger('ezmysql')

__all__ = ['TableOperation', 'TableInsertOperation', 'UpdateTableOperation', 'SelectTableSqlOperation',
           'SelectObjectFromTableOperation', 'SelectOneFromTableOperation', 'DeleteTableOperation',
           'DescTableOperation']


class TableOperation(SqlOperation):
    __metadata__ = ABCMeta
    _table_cache: TableStructureCache = None

    def __init__(self, cache: TableStructureCache):
        self._table_cache = cache

    @abstractmethod
    def operate(self, cursor):
        pass


class TableInsertOperation(TableOperation):
    __table_name = None
    __item = None

    def __init__(self, cache: TableStructureCache, table_name: str, item: dict):
        super().__init__(cache)
        self.__table_name = table_name
        self.__item = item

    def operate(self, cursor):
        structure = self._table_cache.find_structure(self.__table_name, cursor)

        exists_columns = structure.exists_columns(self.__item)
        sql = SqlBuilder.insert_into(self.__table_name).values(exists_columns).build()
        values = [self.__item[key] for key in exists_columns]
        logger.debug('executing sql [{}] with params \n{}'.format(sql, ','.join([str(param) for param in values])))
        update_operation = UpdateSqlOperation(sql, values)
        update_operation.operate(cursor)
        return cursor.lastrowid


class UpdateTableOperation(TableOperation):
    __table_name = None
    __content = None
    __select_param = None

    def __init__(self, cache: TableStructureCache, table_name: str, content: dict, where: dict):
        super().__init__(cache)
        self.__table_name = table_name
        self.__content = content
        self.__select_param = where

    def operate(self, cursor):
        table_structure = self._table_cache.find_structure(self.__table_name, cursor)
        exists_content_columns = table_structure.exists_columns(self.__content)
        exists_param_columns = table_structure.exists_columns(self.__select_param)
        if len(exists_param_columns) == 0:
            raise Exception('invalid operation: where params is null')
        params = [self.__content[key] for key in exists_content_columns] + \
                 [self.__select_param[key] for key in exists_param_columns if self.__select_param[key] is not None]
        sql = SqlBuilder.update(self.__table_name).set(exists_content_columns) \
            .where_equals(exists_param_columns, self.__select_param).build()
        logger.debug('executing sql [{}] with params \n{}'.format(sql, ','.join([str(param) for param in params])))
        cursor.execute(sql, params)
        return cursor.rowcount


class DeleteTableOperation(TableOperation):
    __table_name: str = None
    __params: dict = None

    def __init__(self, cache: TableStructureCache, table_name: str, where: dict):
        super().__init__(cache)
        self.__table_name = table_name
        self.__params = where

    def operate(self, cursor):
        table_structure = self._table_cache.find_structure(self.__table_name, cursor)
        exists_param_columns = table_structure.exists_columns(self.__params)
        if len(exists_param_columns) == 0:
            raise Exception('invalid operation: where params is null')
        params = [self.__params[key] for key in exists_param_columns if self.__params[key] is not None]
        sql = SqlBuilder.delete_from(self.__table_name).where_equals(exists_param_columns, self.__params).build()
        logger.debug('executing sql [{}] with params \n{}'.format(sql, ','.join([str(param) for param in params])))
        cursor.execute(sql, params)
        return cursor.rowcount


class SelectTableSqlOperation(TableOperation):
    __table_name: str = None
    __params: dict = None
    __columns: list = None

    def __init__(self, cache: TableStructureCache, table_name: str, params: dict = None, columns: list = None):
        super().__init__(cache)
        if columns is None:
            columns = []
        self.__table_name = table_name
        self.__params = params
        self.__columns = columns

    def operate(self, cursor):
        sql_builder = SqlBuilder.select_from(self.__table_name)
        if len(self.__columns) > 0:
            sql_builder.select_column(self.__columns)
        params = []
        if self.__params is not None:
            table_structure = self._table_cache.find_structure(self.__table_name, cursor)
            param_columns = table_structure.exists_columns(self.__params)
            sql_builder.where_equals(param_columns, self.__params)
            params = [self.__params[key] for key in param_columns if self.__params[key] is not None]
        sql = sql_builder.build()
        logger.debug('executing sql [{}] with params \n{}'.format(sql, ','.join([str(param) for param in params])))
        return self._operate(cursor, sql, params)

    def _operate(self, cursor, sql, params):
        return QuerySqlOperation(sql, params).operate(cursor)


class SelectOneFromTableOperation(SelectTableSqlOperation):
    def __init__(self, cache: TableStructureCache, table_name: str, params: dict = None, columns: list = None):
        super().__init__(cache, table_name, params, columns)

    def _operate(self, cursor, sql, params):
        return FindOneOperation(sql, params).operate(cursor)


class SelectObjectFromTableOperation(SelectTableSqlOperation):

    def __init__(self, cache: TableStructureCache, table_name: str, column: str, params: dict = None):
        super().__init__(cache, table_name, params, [column])

    def _operate(self, cursor, sql, params):
        return QueryObjOperation(sql, params).operate(cursor)
