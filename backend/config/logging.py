import sys
from loguru import logger

def setup_logging():
    """
    Configures Loguru for application-wide logging.
    """
    logger.remove()
    
    # Standard output format
    fmt = "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
    
    logger.add(sys.stdout, format=fmt, level="INFO", colorize=True)
    
    # File logging for auditing
    logger.add("logs/agent_{time:YYYY-MM-DD}.log", rotation="10 MB", retention="14 days", format=fmt, level="DEBUG")
    
    logger.info("Logging initialized successfully.")
