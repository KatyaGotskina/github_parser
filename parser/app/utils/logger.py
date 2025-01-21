import logging
import sys

logger = logging.getLogger("system_logger")
logger.setLevel(logging.INFO)

console_handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter(
        "{asctime} | {levelname: <8} | {correlation_id} | {message}",
        "%Y-%m-%d %H:%M:%S",
        style='{'
    )
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)
