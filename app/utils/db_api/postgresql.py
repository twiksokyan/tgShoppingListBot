import asyncpg
from typing import Union

from app import config

class Database:

    def __init__(self):
        self.pool: Union[asyncpg.pool.Pool, None] = None

    async def create_connection(self):
        self.pool = await asyncpg.create_pool(
            user=config.DB_USER,
            password=config.DB_PASS,
            host=config.DB_HOST,
            database=config.DB_NAME
        )

    async def execute_query(self, query, *args,
                      fetch: bool = False,
                      fetchval: bool = False,
                      fetchrow: bool = False,
                      execute: bool = False
                      ):
        async with self.pool.acquire() as connection:
            connection: asyncpg.Connection
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(query, *args)
                elif fetchval:
                    result = await connection.fetchval(query, *args)
                elif fetchrow:
                    result = await connection.fetchrow(query, *args)
                elif execute:
                    result = await connection.execute(query, *args)

            return result

    @staticmethod
    def format_args(sql, concat_var, parameters: dict):
        sql += f' {concat_var} '.join([f'{item} = ${num}' for num, item in enumerate(parameters.keys(), start=1)])

        return sql, tuple(parameters.values())

    # Таблица пользователей
    async def create_table_users(self):
        query = """
        CREATE TABLE IF NOT EXISTS USERS (
        TG_ID BIGINT NOT NULL,
        TG_USERNAME VARCHAR(255),
        FULL_NAME VARCHAR(255),
        CREATED_DTTM TIMESTAMP DEFAULT DATE_TRUNC('second', localtimestamp),
        PRIMARY KEY (TG_ID)
        );
        """

        await self.execute_query(query, execute=True)

    async def add_user(self, tg_id, tg_username, full_name):
        query = """
        INSERT INTO USERS (TG_ID, TG_USERNAME, FULL_NAME)
        VALUES ($1, $2, $3)
        RETURNING *
        """

        return await self.execute_query(query, tg_id, tg_username, full_name, fetchrow=True)

    # Таблица маппинга пользователь-список
    async def create_table_users_lists(self):
        query = """
        CREATE TABLE IF NOT EXISTS USERS_LISTS (
        LIST_ID SERIAL,
        TG_ID BIGINT NOT NULL,
        LIST_OWNER BOOLEAN DEFAULT FALSE,
        CREATED_DTTM TIMESTAMP DEFAULT DATE_TRUNC('second', localtimestamp)
        );
        """

        await self.execute_query(query, execute=True)

    async def add_new_list(self, tg_id):
        """Пользователь создает новый список, чтобы пригласить туда других участников"""
        query = """
        INSERT INTO USERS_LISTS (TG_ID, LIST_OWNER)
        VALUES ($1, TRUE)
        RETURNING *
        """

        return await self.execute_query(query, tg_id, fetchrow=True)

    async def add_user_to_list(self, tg_id, list_id):
        """Добавляем участника в список (Он сам будет добавляться после вызова команды)"""
        query = """
        INSERT INTO USERS_LISTS (TG_ID, LIST_ID)
        VALUES ($1, $2)
        RETURNING *
        """

        return await self.execute_query(query, tg_id, list_id, fetchrow=True)

    # async def list_owner_check(self, tg_id):
    #     """Проверка на владельца списка"""
    #     query = """
    #     SELECT LIST_OWNER FROM USERS_LISTS WHERE TG_ID = $1
    #     """
    #
    #     return await self.execute_query(query, tg_id, fetchval=True)

    async def get_list_id(self, tg_id):
        query = """
        SELECT LIST_ID FROM USERS_LISTS WHERE TG_ID = $1
        """

        return await self.execute_query(query, tg_id, fetchval=True)

    async def count_user_lists(self, tg_id):
        query = """
        SELECT COUNT(LIST_ID) FROM USERS_LISTS WHERE TG_ID = $1
        """

        return await self.execute_query(query, tg_id, fetchval=True)

    async def count_list_users(self, list_id):
        query = """
        SELECT COUNT(TG_ID) FROM USERS_LISTS WHERE LIST_ID = $1
        """

        return await self.execute_query(query, list_id, fetchval=True)

    async def get_list_users(self, tg_id):
        """Выбираем всех пользователей списка по любому пользователю из этого списка"""
        list_id = await self.get_list_id(tg_id)

        query = """
        SELECT UL.TG_ID, U.TG_USERNAME, U.FULL_NAME
        FROM USERS_LISTS UL
        JOIN USERS U
            ON UL.TG_ID = U.TG_ID
        WHERE UL.LIST_ID = $1 AND UL.TG_ID != $2
        """

        return await self.execute_query(query, list_id, tg_id, fetch=True)

    async def delete_user_from_list(self, tg_id):
        """Удаление участника списка"""
        query = """
        DELETE FROM USERS_LISTS WHERE TG_ID = $1
        RETURNING *
        """

        return await self.execute_query(query, tg_id, fetchrow=True)

    # Таблица наполнения списка покупок
    async def create_table_shopping_lists(self):
        query = """
        CREATE TABLE IF NOT EXISTS SHOPPING_LISTS (
        ITEM_ID SERIAL PRIMARY KEY,
        LIST_ID INTEGER NOT NULL,
        ITEM_NM VARCHAR(255) NOT NULL,
        CREATED_DTTM TIMESTAMP DEFAULT DATE_TRUNC('second', localtimestamp)
        );
        """

        await self.execute_query(query, execute=True)

    async def add_item(self, list_id, item_nm):
        """Добавления товара в список покупок"""
        query = """
        INSERT INTO SHOPPING_LISTS (LIST_ID, ITEM_NM)
        VALUES ($1, $2)
        RETURNING *
        """

        return await self.execute_query(query, list_id, item_nm, fetchrow=True)

    async def delete_item(self, item_id):
        """Удаления пункта списка"""
        query = """
        DELETE FROM SHOPPING_LISTS WHERE ITEM_ID = $1
        RETURNING*
        """

        return await self.execute_query(query, item_id, fetchrow=True)

    async def get_all_list(self, list_id):
        """Достать все товары из списка"""
        query = """
        SELECT ITEM_ID, ITEM_NM FROM SHOPPING_LISTS WHERE LIST_ID = $1 ORDER BY ITEM_ID
        """

        return await self.execute_query(query, list_id, fetch=True)

    async def clear_shopping_list(self, list_id):
        """Очистка всего списка"""
        query = """
        DELETE FROM SHOPPING_LISTS WHERE LIST_ID = $1
        """

        await self.execute_query(query, list_id, execute=True)
