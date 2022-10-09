import logging


class WishesRepository:
    def __init__(self, connection_string: str):
        self._logger = logging.getLogger()
        self._connection_string = connection_string

    def connect(self):
        # Подключится к базе данных
        raise Exception("Not implemented")

    def create_database_and_tables_if_not_exist(self):
        # Создать базу данных и таблицы если их нет
        raise Exception("Not implemented")

