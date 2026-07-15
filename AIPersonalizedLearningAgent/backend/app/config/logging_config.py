import logging
import sys
from app.core.config import settings

def setup_logging():
    log_level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)
    
    # Configure root logger
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s [%(levelname)s] [%(name)s] (%(filename)s:%(lineno)d) - %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout)
        ],
        force=True  # Overwrites any pre-existing configurations
    )
    
    # Get logger for the app
    logger = logging.getLogger("app")
    logger.setLevel(log_level)
    logger.info(f"Logging initialized with level: {settings.LOG_LEVEL}")

# Convenient getter for module loggers
def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(f"app.{name}")
