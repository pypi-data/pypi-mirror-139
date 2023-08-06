#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random

import pandas as pd
from nose import SkipTest
import nose

from easy_db.db import *

__author__ = 'East'
__created__ = '2021/11/16 10:55'
__filename__ = 'test_db.py'


def test_next_id():
    unique_id = next_id()
    assert len(unique_id) == 50
    assert next_id() != next_id()


def test_encrypt_dict():
    d = {'item_id': 123, 'shop_id': '645', 'cate_id': '3434'}
    code = encrypt_dict(d)
    # print(len(code))
    assert len(code) == 32
    d2 = {'shop_id': '645', 'item_id': 123, 'cate_id': '3434'}
    code2 = encrypt_dict(d2)
    assert code == code2

    d3 = {'shop_id': '645', 'item_id': "123", 'cate_id': '3434'}
    code3 = encrypt_dict(d3)

    assert code2 == code3

    d4 = {'shop_id': '645', 'item_id': 123.0, 'cate_id': '3434'}
    code4 = encrypt_dict(d4)
    assert code2 != code4


def test_encrypt_df():
    rows = [
        {'id': 1, 'name': '苗东方', 'gender': 1, 'age': 28, 'birthday': '1993-05-15'},
        {'id': 2, 'name': 'test001', 'gender': 0, 'age': 23, 'birthday': '1995-05-15'},
        {'id': 3, 'name': 'test002', 'gender': 1, 'age': 18, 'birthday': '1998-05-15'}
    ]
    df = pd.DataFrame(rows)
    res_df = encrypt_df(df, key_names=['id', 'name'])
    code1 = encrypt_dict({'name': '苗东方', 'id': 1, })
    code2 = encrypt_dict({'id': 2, 'name': 'test001', })
    code3 = encrypt_dict({'id': 3, 'name': 'test002'})
    # print(code1)
    # print(res_df.loc[res_df['id'] == 1, 'uuid'].iloc[0])
    assert res_df.loc[res_df['id'] == 1, 'uuid'].iloc[0] == code1
    assert res_df.loc[res_df['id'] == 2, 'uuid'].iloc[0] == code2
    assert res_df.loc[res_df['id'] == 3, 'uuid'].iloc[0] == code3

    res_df2 = encrypt_df(df, key_names=['id', 'name'], secret='12345')
    code11 = encrypt_dict({'id': 1, 'name': '苗东方', }, secret='12345')
    code22 = encrypt_dict({'id': 2, 'name': 'test001', }, secret='12345')
    code33 = encrypt_dict({'id': 3, 'name': 'test002'}, secret='12345')
    assert res_df2.loc[res_df['id'] == 1, 'uuid'].iloc[0] == code11
    assert res_df2.loc[res_df['id'] == 2, 'uuid'].iloc[0] == code22
    assert res_df2.loc[res_df['id'] == 3, 'uuid'].iloc[0] == code33

    assert res_df2.loc[res_df['id'] == 1, 'uuid'].iloc[0] != code1
    assert res_df2.loc[res_df['id'] == 2, 'uuid'].iloc[0] != code2
    assert res_df2.loc[res_df['id'] == 3, 'uuid'].iloc[0] != code3


# @SkipTest
class TestPGDB(object):

    def setUp(self):
        # self.client = app.test_client()
        self.db = PgDB(
            user='bluemoon',
            password='aipg1216',
            database='dw',
            host='192.168.235.9',
            port=5432
        )

        self.table_name = f'domp.pred_test_user_001'

        self.rows = [
            {'id': 1, 'name': '苗东方', 'gender': 1, 'age': 28, 'birthday': '1993-05-15'},
            {'id': 2, 'name': 'test001', 'gender': 0, 'age': 23, 'birthday': '1995-05-15'},
            {'id': 3, 'name': 'test002', 'gender': 1, 'age': 18, 'birthday': '1998-05-15'}
        ]
        self.db.truncate(self.table_name)
        self.db.insert_many(self.table_name, self.rows)

    def tearDown(self):
        self.db.truncate(self.table_name)

    def _get_where_clause(self, clause):
        s = ''
        for k, v in clause.items():
            if isinstance(v, str):
                s += f" {k}='{v}' "
            else:
                s += f" {k}={v} "
        return s

    @staticmethod
    def _get_col_name(col_name):
        return col_name

    def _get_count(self, res):
        return res.get('count')

    def test_select(self):
        res = self.db.select(f"select * from {self.table_name}")
        count_res = self.db.select_one(f"select count(*) as count from {self.table_name}")
        # print('------------------')
        # print(count_res)
        count = self._get_count(count_res)
        assert isinstance(res, list)
        assert len(res) == count
        assert len(res) == len(self.rows)

        res2 = self.db.select_one(f"select * from {self.table_name} where {self._get_where_clause({'id': 1})}")
        assert res2.get('name') == self.rows[0].get('name')
        assert res2.get('age') == self.rows[0].get('age')

    def test_select_df(self):
        # self.db.truncate(self.table_name)
        # self.db.insert_many(self.table_name, self.rows)
        res = self.db.select_df(f"select * from {self.table_name}")
        count_res = self.db.select_one(f"select count(*) as count from {self.table_name}")
        count = self._get_count(count_res)
        assert isinstance(res, pd.DataFrame)
        assert res.shape[0] == count
        name1 = res.loc[res['id'] == 1, 'name'][0]
        age1 = res.loc[res['id'] == 1, 'age'][0]
        assert name1 == self.rows[0].get('name')
        assert age1 == self.rows[0].get('age')
        # self.db.truncate(self.table_name)

    def test_select_one(self):
        res = self.db.select_one(f"select * from {self.table_name} where {self._get_where_clause({'id': 1})}")
        assert isinstance(res, Dict)
        assert res.get('name') == self.rows[0].get('name')
        assert res.get('age') == self.rows[0].get('age')

    def test_update(self):
        new_user_name = f'测试名字{random.randint(100000, 999999)}'
        sql = f"""
        update {self.table_name} set {self._get_col_name('name')}=? where {self._get_where_clause({'id': 1})}
              """
        count = self.db.update(sql, new_user_name)
        assert count == 1

        res = self.db.select_one(f"select * from {self.table_name} where {self._get_where_clause({'id': 1})}")
        assert res['name'] == new_user_name

    def test_insert(self):
        data = {'id': 4, 'name': 'Tom', 'gender': 0, 'age': 20, 'birthday': '2000-05-15'}
        row_num = self.db.insert(self.table_name, data=data)
        assert row_num == 1
        res = self.db.select_one(f"select * from {self.table_name} where {self._get_where_clause({'id': 4})}")
        assert data.get('name') == res.get('name')
        assert data.get('birthday') == res.get('birthday')

    def test_insert_many(self):
        rows = [
            {'id': 5, 'name': '苗东方', 'gender': 1, 'age': 28, 'birthday': '1993-05-15'},
            {'id': 6, 'name': 'test001', 'gender': 0, 'age': 23, 'birthday': '1995-05-15'},
            {'id': 7, 'name': 'test002', 'gender': 1, 'age': 18, 'birthday': '1998-05-15'}
        ]

        count = self.db.insert_many(table=self.table_name, data=rows)
        assert count == len(rows)
        res = self.db.select_one(f"select * from {self.table_name} where {self._get_where_clause({'id': 7})}")
        assert res.get('name') == rows[2].get('name')

    def test_insert_or_update(self):
        rows = [
            {'id': 3, 'name': '苗东方update', 'gender': 1, 'age': 28, 'birthday': '1993-05-15'},
            {'id': 4, 'name': 'test001update', 'gender': 0, 'age': 23, 'birthday': '1995-05-15'},
            {'id': 5, 'name': 'test002update', 'gender': 1, 'age': 18, 'birthday': '1998-05-15'}
        ]
        r = self.db.insert_or_update(self.table_name, rows, primary_key=['id'])

        count_res = self.db.select_one(f"select count(*) as count from {self.table_name}")
        r_count = self._get_count(count_res)
        # print(r_count)
        assert r_count == 5
        res = self.db.select_one(f"select * from {self.table_name} where {self._get_where_clause({'id': 3})}")
        assert res.get('name') == rows[0].get('name')

    def test_insert_df(self):
        rows = [
            {'id': 4, 'name': '苗东方', 'gender': 1, 'age': 28, 'birthday': '1993-05-15'},
            {'id': 6, 'name': 'ererer', 'gender': 0, 'age': 23, 'birthday': '1995-05-15'},
            {'id': 7, 'name': 'test002', 'gender': 1, 'age': 18, 'birthday': '1998-05-15'}
        ]

        df = pd.DataFrame(rows)

        self.db.insert_df(table=self.table_name, df=df)
        res_df = self.db.select_df(f"select * from {self.table_name}")
        # print(res_df)
        assert len(res_df) == 6
        name1 = res_df.loc[res_df['id'] == 6, 'name'].iloc[0]
        # print(name1)
        assert name1 == rows[1].get('name')

    def test_insert_or_update_df(self):
        rows = [
            {'id': 3, 'name': '苗东方updatedf', 'gender': 1, 'age': 28, 'birthday': '1993-05-15'},
            {'id': 6, 'name': 'ererer', 'gender': 0, 'age': 23, 'birthday': '1995-05-15'},
            {'id': 7, 'name': 'test002', 'gender': 1, 'age': 18, 'birthday': '1998-05-15'}
        ]

        df = pd.DataFrame(rows)

        self.db.insert_or_update_df(table=self.table_name, df=df, primary_key=['id'])
        res_df = self.db.select_df(f"select * from {self.table_name}")
        # print(res_df)
        assert len(res_df) == 5
        name1 = res_df.loc[res_df['id'] == 3, 'name'].iloc[0]
        # print(name1)
        assert name1 == rows[0].get('name')


# @SkipTest
class TestMysqlDB(TestPGDB):

    def setUp(self):
        self.db = MysqlDB(
            user='bigdata',
            password='bluemoon2018#',
            database='xxl-job',
            host='192.168.235.3',
            port=3306
        )

        self.table_name = f'pred_test_user_001'

        self.rows = [
            {'id': 1, 'name': '苗东方', 'gender': 1, 'age': 28, 'birthday': '1993-05-15'},
            {'id': 2, 'name': 'test001', 'gender': 0, 'age': 23, 'birthday': '1995-05-15'},
            {'id': 3, 'name': 'test002', 'gender': 1, 'age': 18, 'birthday': '1998-05-15'}
        ]
        self.db.truncate(self.table_name)
        self.db.insert_many(self.table_name, self.rows)


class TestPhoenixDB(TestPGDB):

    def setUp(self):
        self.db = PhoenixDB(
            jdbc_url='jdbc:phoenix:bd-dev-235-51,bd-dev-235-52,bd-dev-235-53:2181',
            driver_path='/Users/miaodongfang/bin/phoenix-4.13.2-cdh5.11.2-client.jar')

        # sql = """
        # create table "pred_system"."pred_test_user_001"
        #     (
        #         "id" INTEGER not null primary key,
        #         "name" VARCHAR(50),
        #         "age" INTEGER,
        #         "gender" INTEGER,
        #         "birthday" VARCHAR(50)
        #     ) column_encoded_bytes=0
        # """
        #
        # self.db.update(sql)

        self.table_name = '"pred_system"."pred_test_user_001"'

        self.rows = [
            {'id': 1, 'name': '苗东方', 'gender': 1, 'age': 28, 'birthday': '1993-05-15'},
            {'id': 2, 'name': 'test001', 'gender': 0, 'age': 23, 'birthday': '1995-05-15'},
            {'id': 3, 'name': 'test002', 'gender': 1, 'age': 18, 'birthday': '1998-05-15'}
        ]
        self.db.truncate(self.table_name)
        self.db.insert_many(self.table_name, self.rows)

    def _get_where_clause(self, clause):
        s = ''
        for k, v in clause.items():
            if isinstance(v, str):
                s += f" \"{k}\"='{v}' "
            else:
                s += f" \"{k}\"={v} "
        return s

    def _get_count(self, res):
        return res.get('COUNT')

    @staticmethod
    def _get_col_name(col_name):
        return f'"{col_name}"'

    def test_update(self):
        new_user_name = f'测试名字{random.randint(100000, 999999)}'
        sql = f"""
        upsert into {self.table_name}("id", "name") values(1, ?)
              """
        count = self.db.update(sql, new_user_name)
        assert count == 1

        res = self.db.select_one(f"select * from {self.table_name} where {self._get_where_clause({'id': 1})}")
        assert res['name'] == new_user_name


if __name__ == '__main__':
    nose.run()
