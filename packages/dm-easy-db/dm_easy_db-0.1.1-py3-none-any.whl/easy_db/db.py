#!/usr/bin/env python
# -*- coding: utf-8 -*-

import functools
import logging
import threading
import time
import uuid
import hashlib
from abc import abstractmethod, ABCMeta
from typing import List, Union

__author__ = 'East'
__created__ = '2020-01-08 16:17'
__filename__ = 'db.py'

logger = logging.getLogger(__name__)

"""
logging.basicConfig(level=logging.INFO)

db = MysqlDB(host=Config.MYSQL_HOST, port=Config.MYSQL_PORT, database=Config.MYSQL_DB,
    user=Config.MYSQL_USER, password=Config.MYSQL_PASSWORD)

res = db.select('select * from plugin_page_code')
"""


class DBError(Exception):
    pass


class MultiColumnsError(Exception):
    pass


def next_id(t=None):
    """
    用于创建一个唯一的id，该ID综合了uuid和当前时间形成的，长度为50
    :param t: 当前的时间戳
    :return:
    """
    if t is None:
        t = time.time()
    return "%015d%s000" % (int(t * 1000), uuid.uuid4().hex)


def encrypt_dict(params: dict, secret: str = None) -> str:
    """
    根据传入的字典和密钥生成一个唯一的编码，编码采用md5。并且可以不考虑传入字典的顺序
    :param params: dict, 需要编码的字典
    :param secret: str, default None, 密钥字符串
    :return: str, 编码结果，全部为大写字母
    """
    params = sorted(params.items(), key=lambda item: item[0])
    text = ''
    if secret is not None:
        text += str(secret)
    for param in params:
        text += str(param[0])
        text += str(param[1])
    if secret is not None:
        text += str(secret)
    md5 = hashlib.md5()
    md5.update(text.encode('utf8'))
    return md5.hexdigest().upper()


def encrypt_df(df, key_names: Union[str, list, tuple], secret: str = None):
    """

    :param df: pandas.DataFrame, 需要编码的DataFrame
    :param key_names: str | list | tuple, 参与编码的字段
    :param secret: str, default None, 密钥字符串
    :return: pandas.DataFrame
    """
    if isinstance(key_names, str):
        key_names = [key_names]
    key_names = sorted(key_names)

    def encrypt_row(row):
        text = ''
        if secret is not None:
            text += str(secret)
        for key in key_names:
            text += str(key)
            text += str(row[key])
        if secret is not None:
            text += str(secret)
        md5 = hashlib.md5()
        md5.update(text.encode('utf8'))
        return md5.hexdigest().upper()

    keys = df.apply(encrypt_row, axis=1)
    df['uuid'] = keys
    return df


class _Engine(object):
    def __init__(self, connect):
        self._connect = connect

    def connect(self):
        return self._connect()


class _LazyConnection(object):
    def __init__(self, engine):
        self.connection = None
        self.engine = engine

    def cursor(self):
        if self.connection is None:
            _connection = self.engine.connect()
            logger.info("Open connection <%s>" % hex(id(_connection)))
            self.connection = _connection
        return self.connection.cursor()

    def commit(self):
        self.connection.commit()

    def rollback(self):
        self.connection.rollback()

    def cleanup(self):
        if self.connection:
            _connection = self.connection
            self.connection = None
            logger.info('close connection <%s>' % hex(id(_connection)))
            _connection.close()


class _DbCtx(threading.local):
    def __init__(self, engine):
        self.connection = None
        self.transactions = 0
        self.engine = engine

    def is_init(self):
        return self.connection is not None

    def init(self):
        self.connection = _LazyConnection(self.engine)

    def cleanup(self):
        self.connection.cleanup()
        self.connection = None

    def cursor(self):
        return self.connection.cursor()


class _ConnectionCtx(object):

    def __init__(self, _db_ctx):
        self._db_ctx = _db_ctx

    def __enter__(self):
        self.should_cleanup = False

        if not self._db_ctx.is_init():
            self._db_ctx.init()
            self.should_cleanup = True

        return self

    def __exit__(self, exctype, excvalue, traceback):
        if self.should_cleanup:
            self._db_ctx.cleanup()


class _TransactionCtx(object):
    def __init__(self, _db_ctx):
        self._db_ctx = _db_ctx

    def __enter__(self):
        self.should_close_conn = False

        if not self._db_ctx.is_init():
            self._db_ctx.init()
            self.should_cleanup = True

        self._db_ctx.transactions = self._db_ctx.transactions + 1
        return self

    def __exit__(self, exctype, excvalue, traceback):
        self._db_ctx.transactions = self._db_ctx.transactions - 1
        try:
            if self._db_ctx.transactions == 0:
                if exctype is None:
                    self.commit()
                else:
                    self.rollback()
        finally:
            if self.should_close_conn:
                self._db_ctx.cleanup()

    def commit(self):
        try:
            self._db_ctx.connection.commit()
        except Exception as e:
            self._db_ctx.connection.rollback()
            raise e

    def rollback(self):
        self._db_ctx.connection.rollback()


class Dict(dict):
    """
    自定义一个字典，实现可以通过  dict.attr取出其中的值
    """

    def __init__(self, names=(), values=(), **kw):
        super(Dict, self).__init__(**kw)
        for k, v in zip(names, values):
            self[k] = v

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Dict' object has no attribute '%s'" % key)

    def __setattr__(self, k, v):
        self[k] = v


def with_transaction(func):
    @functools.wraps(func)
    def _wrapper(self, *args, **kw):
        _start = time.time()
        with _TransactionCtx(self._db_ctx):
            return func(self, *args, **kw)

    return _wrapper


def with_connection(func):
    @functools.wraps(func)
    def _wrapper(self, *args, **kw):
        with _ConnectionCtx(self._db_ctx):
            return func(self, *args, **kw)

    return _wrapper


class DbBase(metaclass=ABCMeta):

    def __init__(self):
        self.engine = None
        self._db_ctx = None

    def _get_sql(self, sql):
        return sql.replace('?', '%s')

    @abstractmethod
    def _create_engine(self, *args, **kwargs):
        pass

    def clear_engine(self):
        self.engine = None

    @with_connection
    def _select(self, sql, first, *args):
        cursor = None
        sql = self._get_sql(sql)
        logger.info("SQL:%s , ARGS: %s" % (sql, args))

        try:
            cursor = self._db_ctx.cursor()
            cursor.execute(sql, args)
            names = []
            if cursor.description:
                names = [x[0] for x in cursor.description]
            if first:
                values = cursor.fetchone()
                if not values:
                    return None
                return Dict(names, values)
            return [Dict(names, x) for x in cursor.fetchall()]
        finally:
            if cursor:
                cursor.close()

    @with_connection
    def select(self, sql: str, *args) -> List[Dict]:
        """
        查询，传入select查询语句和参数，返回查询结果
        select查询语句可以使用?作为占位符，如果包含占位符，需要通过args传入对应的参数
        如：
          select('select * from table where id=1')
          select('select * from table where id=?', 1)
        :param sql: str, sql语句
        :param args: 参数, 需要与sql语句中的?占位符的数量一致
        :return: List[Dict]
        """
        return self._select(sql, False, *args)

    @with_connection
    def select_df(self, sql: str, *args):
        """
        查询数据库，返回查询结果
        :param sql: str, sql语句
        :param args: 参数, 需要与sql语句中的?占位符的数量一致
        :return: pandas.DataFrame
        """
        try:
            import pandas as pd
        except ImportError:
            raise DBError("如果需要使用Dataframe需要先安装pandas，请运行 'pip install pandas' 安装")

        sql = sql.replace('?', '%s')
        logger.info("sql : %s ,args : %s" % (sql, args))
        result = pd.read_sql(sql, self._db_ctx.connection)
        columns = [col.split('.')[0] if len(col.split('.')) <= 1 else col.split('.')[1] for col in result.columns]
        result.columns = columns
        return result

    @with_connection
    def select_one(self, sql: str, *args) -> Dict:
        """
        查询数据库，返回第一条数据
        :param sql: str, sql语句
        :param args: 参数, 需要与sql语句中的?占位符的数量一致
        :return: Dict
        """
        return self._select(sql, True, *args)


class DbBaseWithWrite(DbBase):

    @abstractmethod
    def _create_engine(self, *args, **kwargs):
        pass

    def _get_insert_sql(self, table, cols, database=None):
        if database is not None:
            table_name = f"`{database}`.`{table}`"
        else:
            table_name = f"`{table}`"
        sql = f"insert into {table_name}(`{'`,`'.join(cols)}`) values ({','.join(['?' for _ in range(len(cols))])}) "
        # if update:
        #     sql += f"on duplicate key update {', '.join([f'{col}=VALUES(f{col})'for col in cols])}"
        return sql

    def _get_insert_or_update_sql(self, table, cols, database=None, primary_key=None, **kwargs):
        pass

    @with_connection
    def _update(self, sql, *args):
        cursor = None
        # sql = sql.replace('?', '%s')
        sql = self._get_sql(sql)
        logger.info("sql : %s ,args : %s" % (sql, args))
        try:
            cursor = self._db_ctx.cursor()
            cursor.execute(sql, args)
            r = cursor.rowcount
            if self._db_ctx.transactions == 0:
                logger.info("auto commit")
                self._db_ctx.connection.commit()
            return r
        finally:
            if cursor:
                cursor.close()

    @with_connection
    def _insert_many(self, sql, data: list):
        cursor = None
        # sql = sql.replace('?', '%s')
        sql = self._get_sql(sql)
        logger.info("sql : %s ,args : " % (sql,))
        try:
            cursor = self._db_ctx.cursor()
            cursor.executemany(sql, data)
            r = cursor.rowcount
            if self._db_ctx.transactions == 0:
                logger.info("auto commit")
                self._db_ctx.connection.commit()
            return r
        finally:
            if cursor:
                cursor.close()

    @with_connection
    def _insert_many_batch(self, sql, data: list, batch_size=10000):
        t = int(len(data) / batch_size)
        if batch_size is None:
            return self._insert_many(sql, data)

        r = 0
        for i in range(t):
            tmp = self._insert_many(sql, data[i * batch_size: (i + 1) * batch_size])
            r += tmp
        if t * batch_size < len(data):
            tmp = self._insert_many(sql, data[t * batch_size:])
            r += tmp

        return r

    def insert_many(self, table: str, data: List[dict], cols_name: list = None, database: str = None,
                    batch_size: int = 10000):
        """
        一次性同时插入多条数据
        :param table: str, 表名
        :param data: List[dict], 需要插入的数据
        :param cols_name: List[str], default None, 需要插入的列，
            如果有该参数将会只插入列表中出现的列, 如果data中某条数据不存在指定的列，将设置为None
            如果该参数为None，将获取data中第一个元素的所有key作为要插入的列
        :param database: str, default None 数据库名
        :param batch_size: int, default 10000 批量插入的数量
        :return: int, 受影响的行数
        """
        if data is None or len(data) == 0:
            raise ValueError('传入的data必须不为空')
        if cols_name is not None:
            keys = cols_name
        else:
            keys = list(data[0].keys())

        sql = self._get_insert_sql(table=table, database=database, cols=keys)
        insert_data = []
        for item in data:
            insert_data.append([item.get(k, None) for k in keys])

        return self._insert_many_batch(sql, insert_data, batch_size)

    def insert_df(self, table: str, df, cols_name: list = None, database: str = None, batch_size: int = 10000):
        """
        插入DataFrame
        :param table: str, 表名
        :param df: pandas.DataFrame, 需要插入的数据
        :param cols_name: List[str], default None, 需要插入的列，
            如果有该参数将会只插入列表中出现的列, 如果data中某条数据不存在指定的列，将设置为None
            如果该参数为None，将获取DataFrame中的列名作为要插入的列
        :param database: str, default None 数据库名
        :param batch_size: int, default 10000 批量插入的数量
        :return: int, 受影响的行数
        """
        data = [v for k, v in df.to_dict('index').items()]
        return self.insert_many(table, data, cols_name=cols_name, database=database, batch_size=batch_size)

    def insert_or_update(self, table,
                         data: list,
                         primary_key: Union[str, list] = None,
                         cols_name=None,
                         database=None,
                         batch_size=10000,
                         **kwargs):
        """
        插入或更新数据，如果存在则更新，如果不存在则插入
        :param table: str, 表名
        :param data: List[dict], 需要插入的数据
        :param primary_key str | List[str], default None，主键，
            如果是mysql数据库，则不需要传入该参数，数据库会自动根据主键或者唯一约束是否冲突决定执行插入还是更新操作
            如果是pg数据库，则必须传入该参数，否则无法更新操作，可以包括主键，也可以包括唯一约束
            如果是Phoenix数据库，则不需要传入该参数，它将根据row key进行更新
        :param cols_name: List[str], default None, 需要插入的列，
            如果有该参数将会只插入列表中出现的列, 如果data中某条数据不存在指定的列，将设置为None
            如果该参数为None，将获取DataFrame中的列名作为要插入的列
        :param database: str, default None 数据库名
        :param batch_size: int, default 10000 批量插入的数量
        :return: int, 受影响的行数
        """
        if data is None or len(data) == 0:
            raise ValueError('传入的data必须不为空')
        if cols_name is not None:
            keys = cols_name
        else:
            keys = list(data[0].keys())

        sql = self._get_insert_or_update_sql(table, keys, database=database, primary_key=primary_key)
        insert_data = []
        for item in data:
            insert_data.append([item.get(k, None) for k in keys])

        return self._insert_many_batch(sql, insert_data, batch_size)

    def insert_or_update_df(self, table, df, primary_key=None, cols_name=None, database=None, batch_size=10000,
                            **kwargs):
        """
        插入或更新数据，如果存在则更新，如果不存在则插入
        :param table: str, 表名
        :param df: pandas.DataFrame, 需要插入的数据
        :param primary_key str | List[str], default None，主键，
            如果是mysql数据库，则不需要传入该参数，数据库会自动根据主键或者唯一约束是否冲突决定执行插入还是更新操作
            如果是pg数据库，则必须传入该参数，否则无法更新操作，可以包括主键，也可以包括唯一约束
            如果是Phoenix数据库，则不需要传入该参数，它将根据row key进行更新
        :param cols_name: List[str], default None, 需要插入的列，
            如果有该参数将会只插入列表中出现的列, 如果data中某条数据不存在指定的列，将设置为None
            如果该参数为None，将获取DataFrame中的列名作为要插入的列
        :param database: str, default None 数据库名
        :param batch_size: int, default 10000 批量插入的数量
        :return: int, 受影响的行数
        """
        data = [v for k, v in df.to_dict('index').items()]
        return self.insert_or_update(
            table,
            data,
            cols_name=cols_name,
            batch_size=batch_size,
            primary_key=primary_key,
            database=database,
            **kwargs)

    @with_connection
    def insert(self, table, data: dict, database=None, cols_name=None):
        """
        向数据库中插入一条数据
        :param table: str, 表名
        :param data: List[dict], 需要插入的数据
        :param cols_name: List[str], default None, 需要插入的列，
            如果有该参数将会只插入列表中出现的列, 如果data中某条数据不存在指定的列，将设置为None
            如果该参数为None，将获取data中的所有key作为要插入的列
        :param database: str, default None 数据库名
        :return: int, 受影响的行数
        """
        cols, args = list(zip(*iter(data.items())))
        sql = self._get_insert_sql(table=table, database=database, cols=cols)
        return self._update(sql, *args)

    def update(self, sql, *args):
        """
        传入sql和参数，更新数据
        :param sql: str, sql语句
        :param args: 参数, 需要与sql语句中的?占位符的数量一致
        :return:
        """
        return self._update(sql, *args)

    @staticmethod
    def _get_table_name(table, database=None):
        if database is not None:
            return f'`{database}`.`{table}`'
        else:
            return f'`{table}`'

    def truncate(self, table, database=None):
        """
        清空表
        :param table:
        :param database
        :return:
        """
        table_name = self._get_table_name(table, database)
        return self.update(f"truncate table {table_name}")


class MysqlDB(DbBaseWithWrite):

    def __init__(self, user, database, password=None, host='127.0.0.1', port=3306, **kw):
        super().__init__()
        self._create_engine(user=user, database=database, password=password, host=host, port=port, **kw)

    def _create_engine(
            self, *args, **kwargs):
        try:
            import mysql.connector
        except ImportError:
            raise DBError("您必须安装mysql驱动才能查询mysql数据库，请运行 'pip install mysql-connector' 安装")

        port = kwargs.get('port', 3306)
        host = kwargs.get('port', '127.0.0.1')
        user = kwargs.get('user')
        password = kwargs.get('password')
        database = kwargs.get('database')

        params = dict(user=user, password=password, database=database, host=host, port=port)
        default = dict(use_unicode=True, charset='utf8', collation='utf8_general_ci', autocommit=False)
        for k, v in default.items():
            params[k] = v
        params.update(kwargs)
        params['buffered'] = True

        engine = _Engine(lambda: mysql.connector.connect(**params))
        self.engine = engine
        logger.info("Init engine <%s> ok." % hex(id(engine)))
        self._db_ctx = _DbCtx(self.engine)

    def _get_insert_or_update_sql(self, table, cols, database=None, primary_key=None):
        sql = self._get_insert_sql(table=table, database=database, cols=cols)
        sql += f"on duplicate key update {', '.join([f'{col}=VALUES({col})' for col in cols])}"
        return sql


class ImpalaDB(DbBase):
    def __init__(self, user=None, database=None, password=None, host='127.0.0.1', port=21050, timeout=None, **kw):
        super().__init__()
        self._create_engine(user=user, database=database, password=password, host=host, port=port, timeout=timeout,
                            **kw)

    def _create_engine(
            self, *args, **kwargs):
        try:
            import impala.dbapi
        except ImportError:
            raise DBError("需要先安装impala驱动才能连接impala数据库，请运行 'pip install impyla' 安装")
        port = kwargs.get('port', 21050)
        host = kwargs.get('port', '127.0.0.1')
        params = dict(host=host, port=port)
        params.update(kwargs)
        engine = _Engine(lambda: impala.dbapi.connect(**params))
        self.engine = engine
        logger.info("Init engine <%s> ok." % hex(id(engine)))
        self._db_ctx = _DbCtx(self.engine)


class HiveDB(DbBase):
    def __init__(self, user=None, database=None, password=None, host='127.0.0.1', port=10000, **kw):
        super().__init__()
        self._create_engine(user=user, database=database, password=password, host=host, port=port, **kw)

    def _create_engine(self, *args, **kwargs):
        try:
            from pyhive import hive
        except ImportError:
            raise DBError("需要先安装pyhive才能连接hive，请运行 'pip install pyhive' 安装")
        port = kwargs.get('port', 10000)
        host = kwargs.get('host', '127.0.0.1')
        params = dict(host=host, port=port)
        params.update(kwargs)

        engine = _Engine(lambda: hive.Connection(**params))
        self.engine = engine
        logger.info("Init engine <%s> ok." % hex(id(engine)))
        self._db_ctx = _DbCtx(self.engine)


class PgDB(DbBaseWithWrite):

    def __init__(self, host='localhost', port=5432, database=None,
                 timeout=None, user=None, password=None, **kw):

        """

        :param host:
        :param port:
        :param database:
        :param timeout:
        :param user:
        :param password:
        :param kw:
        """

        super().__init__()
        self._create_engine(user=user, database=database, password=password, host=host, port=port, timeout=timeout,
                            **kw)

    def _get_insert_sql(self, table, cols, database=None):
        if database is not None:
            table_name = f"{database}.{table}"
        else:
            table_name = table
        sql = f"insert into {table_name}({', '.join(cols)}) values ({','.join(['?' for _ in range(len(cols))])}) "
        return sql

    @staticmethod
    def _get_table_name(table, database=None):
        if database is not None:
            return f'{database}.{table}'
        else:
            return f'{table}'

    def _get_insert_or_update_sql(self, table, cols, database=None, primary_key=None, **kwargs):
        if primary_key is None:
            raise ValueError('primay key不能为None')
        if isinstance(primary_key, str):
            primary_key = [primary_key]
        sql = self._get_insert_sql(table=table, database=database, cols=cols)
        sql += f"on CONFLICT({','.join(primary_key)}) DO UPDATE set " \
               f"{', '.join([f'{col}=excluded.{col}' for col in cols])}"
        return sql

    def _create_engine(self, *args, **kwargs):
        try:
            import psycopg2
        except ImportError:
            raise DBError("需要先安装pg驱动才能操作pg数据库，请运行 'pip install psycopg2-binary' 安装")
        port = kwargs.get('port', 3306)
        host = kwargs.get('port', '127.0.0.1')
        user = kwargs.get('user')
        password = kwargs.get('password')
        database = kwargs.get('database')
        timeout = kwargs.get('timeout')
        params = dict(host=host, port=port, database=database, timeout=timeout, user=user, password=password)
        params.update(kwargs)
        engine = _Engine(lambda: psycopg2.connect(**params))
        self.engine = engine
        logger.info("Init engine <%s> ok." % hex(id(engine)))
        self._db_ctx = _DbCtx(self.engine)


class PhoenixDB(DbBaseWithWrite):
    def __init__(self, jdbc_url, driver_path, user=None, password=None, **kw):
        super().__init__()
        self._create_engine(jdbc_url=jdbc_url, driver_path=driver_path, username=user, password=password, **kw)

    def _create_engine(self, *args, **kwargs):
        try:
            import jaydebeapi
        except ImportError:
            raise DBError("需要先安装jaydebeapi才能连接phoenix，请运行 'pip install jaydebeapi' 安装")

        jdbc_url = kwargs.get('jdbc_url')
        driver_path = kwargs.get('driver_path')
        driver_params = dict()
        username = kwargs.get('username')
        password = kwargs.get('password')
        if username is not None:
            driver_params['username'] = username
        if password is not None:
            driver_params["password"] = password
        # driver_params.update(kw)
        driver_params['phoenix.schema.isNamespaceMappingEnabled'] = 'true'
        engine = _Engine(lambda: jaydebeapi.connect(
            'org.apache.phoenix.jdbc.PhoenixDriver',
            jdbc_url,
            driver_params,
            driver_path))

        self.engine = engine
        logger.info("Init engine <%s> ok." % hex(id(engine)))
        self._db_ctx = _DbCtx(self.engine)

    @staticmethod
    def _get_table_name(table, database=None):
        if database is None:
            table_name = table
        else:
            if database.startswith('"') and database.endswith('"'):
                pass
            else:
                database = f'"{database}"'
            if table.startswith('"') and table.endswith('"'):
                pass
            else:
                table = f'"{table}"'
            table_name = f'{database}.{table}'
        return table_name

    def _get_insert_sql(self, table, cols, database=None):
        table_name = self._get_table_name(table, database)

        sql = f"""
        upsert into {table_name}({','.join([f'"{col}"' for col in cols])})
        values({",".join(['?' for _ in range(len(cols))])})
        """
        return sql

    def _get_insert_or_update_sql(self, table, cols, database=None, **kwargs):
        return self._get_insert_sql(table, cols, database)

    def _get_sql(self, sql):
        return sql

    def truncate(self, table, database=None):
        table_name = self._get_table_name(table, database)
        return self.update(f"delete from {table_name}")
