import logging

from services.telegram_integration import TelegramIntegrations
from services.wishes_generator import WishesGenerator
from services.wishes_repository import WishesRepository

TOKEN = "<TOKEN>"
PSQL_CONNECTION_STRING = "<CONNECTION_STRING>"

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

if __name__ == '__main__':
    # initialize database
    wish_repository = WishesRepository(PSQL_CONNECTION_STRING)
    wishes_generator = WishesGenerator(wish_repository)

    # start
    telegram_bot = TelegramIntegrations(TOKEN, wishes_generator).initialize().run()
