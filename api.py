from vkbottle.api import API
from vkbottle.utils import logger
from config import config

logger.remove()

with open(str(config.tokens)) as fin:
    tokens = [token.strip() for token in fin]

api = API(tokens=tokens, throw_errors=True)
