import logging
import os
from logging.handlers import RotatingFileHandler

def setup_logging(app_name):
    # Create logs directory if it doesn't exist
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    # Create a logger
    logger = logging.getLogger(app_name)
    logger.setLevel(logging.DEBUG)
    
    # Create handlers
    console_handler = logging.StreamHandler()
    file_handler = RotatingFileHandler(
        f'logs/{app_name}.log',
        maxBytes=1024 * 1024,  # 1MB
        backupCount=5
    )
    
    # Create formatters and add it to handlers
    log_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(log_format)
    file_handler.setFormatter(log_format)
    
    # Add handlers to the logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger 