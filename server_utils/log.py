import logging

from fastapi import FastAPI

# Define a logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create a log file handler
handler = logging.FileHandler('./server_utils/logs/app.log')
handler.setLevel(logging.INFO)

# Define the log file format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# Add the file handler to the logger
logger.addHandler(handler)