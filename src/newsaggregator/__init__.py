import os
import sys
import logging

# Define logging format
logger_str = "[%(asctime)s: %(levelname)s: %(module)s: %(message)s]"

# Define log directory and file path
log_dir = "logs"
log_filepath = os.path.join(log_dir, "logger.log")
os.makedirs(log_dir, exist_ok=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format=logger_str,
    handlers=[
        logging.FileHandler(log_filepath),
        logging.StreamHandler(sys.stdout)
    ]
)

# Create a logger instance
logger = logging.getLogger("NewsAggregatorLogger")

# Log a welcome message
logger.info("Hi, welcome to the news aggregator!")
