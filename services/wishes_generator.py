import logging

from services.wishes_repository import WishesRepository


class WishesGenerator:
    def __init__(self, repository: WishesRepository):
        self._logger = logging.getLogger()
        self._repository = repository

    def get_simple_wish(self):

        # Извлечь из БД и создать простое поздравление
        raise Exception("Not implemented")

    def get_complex_wish(self):
        # Извлечь из БД и создать сложное поздравление
        raise Exception("Not implemented")

