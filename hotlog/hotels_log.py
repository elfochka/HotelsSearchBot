from loguru import logger

logger.remove()
logger.add("hotels.log", rotation="10 MB", retention="2 weeks")
