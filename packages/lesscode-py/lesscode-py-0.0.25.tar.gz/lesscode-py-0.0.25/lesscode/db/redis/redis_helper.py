# -*- coding: utf-8 -*-
# author:chao.yy
# email:yuyc@ishangqi.com
# date:2021/11/26 3:56 下午
# Copyright (C) 2021 The lesscode Team
import aioredis

from lesscode.db.base_sql_helper import BaseSqlHelper
from lesscode.db.condition_wrapper import ConditionWrapper


class RedisHelper(BaseSqlHelper):

    def get_connection(self):
        return aioredis.Redis(connection_pool=self.pool, decode_responses=True)

    async def set(self, name, value, ex=None, px=None, nx: bool = False, xx: bool = False, keepttl: bool = False):
        await self.get_connection().set(name, value, ex, px, nx, xx, keepttl)

    async def get(self, name):
        await self.get_connection().get(name)

    async def delete(self, name):
        await self.get_connection().delete(name)

    async def rpush(self, name, values: list, time=None):
        await self.get_connection().rpush(name, *values)
        if time:
            await self.get_connection().expire(name, time)

    async def insert_data(self, table_name: str, data):
        pass

    async def insert_one_data(self, table_name: str, data: dict):
        pass

    async def insert_many_data(self, table_name: str, data: list):
        pass

    async def update_data(self, condition_wrapper: ConditionWrapper, param: dict):
        pass

    async def delete_data(self, condition_wrapper: ConditionWrapper):
        pass

    async def fetchone_data(self, condition_wrapper: ConditionWrapper):
        pass

    async def fetchall_data(self, condition_wrapper: ConditionWrapper):
        pass

    async def fetchall_page(self, condition_wrapper: ConditionWrapper, page_num=1, page_size=10):
        pass

    async def execute_sql(self, sql: str, param=None):
        pass

    async def executemany_sql(self, sql: str, param=None):
        pass

    async def execute_fetchone(self, sql: str, param=None):
        pass

    async def execute_fetchall(self, sql: str, param=None):
        pass

    def prepare_insert_sql(self, table_name: str, item: dict):
        pass

    def prepare_update_sql(self, condition_wrapper: ConditionWrapper, param: dict):
        pass

    def prepare_delete_sql(self, condition_wrapper: ConditionWrapper):
        pass

    def prepare_condition_sql(self, conditions: list):
        pass

    def prepare_query_sql(self, condition_wrapper: ConditionWrapper):
        pass

    def prepare_page_sql(self, condition_wrapper: ConditionWrapper, page_num: int, page_size: int):
        pass
