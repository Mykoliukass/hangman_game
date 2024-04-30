import logging
from functools import wraps

# Setup logging
logging.basicConfig(
    level=logging.DEBUG,
    filename="game_data_logged.log",
    filemode="a",
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%d/%m/%Y %H:%M:%S",
)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

console_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%d/%m/%Y %H:%M:%S",
)
console_handler.setFormatter(console_formatter)

logging.getLogger().addHandler(console_handler)


#
