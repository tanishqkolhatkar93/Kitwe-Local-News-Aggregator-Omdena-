import os
from bs4 import BeautifulSoup
from datetime import datetime
from src.newsaggregator import logger
import requests
from src.newsaggregator.entity.config_entity import (DataIngestionConfig)
import pandas as pd



class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.input_path = config.input_path
        self.output_path = config.output_path
        
    def load_and_save_data(self):
        """Load data from a CSV file and save it to another location."""
        try:
            # Load the data
            df = pd.read_csv(self.input_path, encoding='utf-8')
            logger.info(f"Data loaded successfully from {self.input_path}")

            # Ensure output directory exists
            self.output_path.parent.mkdir(parents=True, exist_ok=True)

            # Save the data
            df.to_csv(self.output_path, index=False)
            logger.info(f"Data saved successfully to {self.output_path}")
        except FileNotFoundError:
            logger.error(f"File not found: {self.input_path}")
        except PermissionError:
            logger.error(f"Permission denied: Cannot save to {self.output_path}")
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            raise e  # Re-raise the exception if needed

    