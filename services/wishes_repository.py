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
        self._logger.debug("Connected")

    def _create_tables_if_not_exist(self):
        # Создать базу данных и таблицы если их нет
        cursor = self._conn.cursor()

        cursor.execute(self._get_create_query("dear"))
        cursor.execute(self._get_create_query("wish"))
        cursor.execute(self._get_create_query("will_be"))
        cursor.execute(self._get_create_query("let"))
        self._conn.commit()

    @staticmethod
    def _get_create_query(table_name):
        query = '''CREATE TABLE IF NOT EXISTS {} (
                            id      int primary key,
                            is_male bool,
                            cringe_level    int,
                            content text NOT NULL UNIQUE
                        );'''

        return sql.SQL(query).format(sql.Identifier(table_name))

    def get_content_by_table(self, table_name: str, cringe_level: int, is_male: bool):
        cursor = self._conn.cursor()

        cursor.execute("SELECT content FROM " + table_name + " WHERE cringe_level < %s AND is_male is %s;", (cringe_level, is_male ))
        table_content = cursor.fetchall()
        print(table_content)


