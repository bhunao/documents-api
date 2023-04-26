import logging

logger = logging.getLogger("documents-api")

logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler('api.log')
file_handler.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

formatter = logging.Formatter(
    '[%(asctime)s | %(name)s | %(levelname)s | %(funcName)s |]: %(message)s')

file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)
