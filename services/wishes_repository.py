import logging

import psycopg2
from psycopg2 import sql


class WishesRepository:
    def __init__(self, connection_string: str):
        self._logger = logging.getLogger()
        self._connection_string = connection_string
        self._connect()
        self._create_tables_if_not_exist()

    def _connect(self):
        # Подключиться к базе данных
        self._conn = psycopg2.connect(self._connection_string)
        self._cursor = self._conn.cursor()
        self._logger.debug("Connected")

    def _create_tables_if_not_exist(self):
        # Создать базу данных и таблицы если их нет
        self._cursor.execute(self._get_create_query("dear"))
        self._cursor.execute(self._get_create_query("wish"))
        self._cursor.execute(self._get_create_query("will_be"))
        self._cursor.execute(self._get_create_query("let"))
        self._conn.commit()

    @staticmethod
    def _get_create_query(table_name):
        query = '''CREATE TABLE IF NOT EXISTS {} (
                            id      int primary key,
                            is_male bool,
                            type    text,
                            content text NOT NULL UNIQUE
                        );'''

        return sql.SQL(query).format(sql.Identifier(table_name))
