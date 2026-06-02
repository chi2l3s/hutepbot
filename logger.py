import sys
from loguru import logger

def setup_logger():
    logger.remove()

    logger.add(
        sys.stdout,
        format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level="DEBUG",
        colorize=True
    )

    logger.add(
        "logs/bot.log",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{line} - {message}",
        level="INFO",
        rotation="10 MB",
        retention="30 days",
        compression="zip",
        encoding="utf-8",
    )

    return logger