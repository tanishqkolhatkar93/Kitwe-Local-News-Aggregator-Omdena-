from src.newsaggregator import logger
from src.newsaggregator.entity.config_entity import DataCleaningConfig
import pandas as pd
import string
import nltk
import os
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from dataclasses import dataclass
from typing import List
from pathlib import Path
class DataCleaning:
    def __init__(self, config: DataCleaningConfig):
        self.input_path = config.input_path
        self.output_path = config.output_path
        self.date_column = config.date_column
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))
        self.df = None
        self.text_columns = config.text_columns

    def load_cleaning(self):
        """Load the dataset and perform initial cleaning steps."""
        try:
            self.df = pd.read_csv(self.input_path)  # Load the data
            logger.info("........Loaded Dataset")
        except FileNotFoundError:
            logger.error(f"File not found at {self.input_path}")
            return
        except pd.errors.EmptyDataError:
            logger.error("No data found in the file.")
            return
        except Exception as e:
            logger.error(f"An error occurred while loading the dataset: {str(e)}")
            return
        
        if self.df.empty:
            logger.error("Loaded DataFrame is empty. Cleaning process aborted.")
            return

        logger.info("Converting date column into Datetime format")
        if self.date_column in self.df.columns:
            self.df[self.date_column] = pd.to_datetime(self.df[self.date_column], errors="coerce")
            logger.info("Date column converted into Datetime")
        else:
            logger.warning(f"Date column '{self.date_column}' not found in DataFrame.")

        logger.info("Dropping duplicates based on 'title' column")
        initial_count = self.df.shape[0]
        self.df.drop_duplicates(inplace=True)
        final_count = self.df.shape[0]
        duplicates_dropped = initial_count - final_count
        logger.info(f"{duplicates_dropped} duplicates dropped successfully")

        self.df.fillna("Unknown", inplace=True)
        logger.info("Filled missing values as 'Unknown'.")

    def create_output_directory(self):
        """Create the output directory if it does not exist."""
        if not os.path.exists(os.path.dirname(self.output_path)):
            try:
                os.makedirs(os.path.dirname(self.output_path))
                logger.info(f"Output directory created at {os.path.dirname(self.output_path)}")
            except Exception as e:
                logger.error(f"Error creating output directory: {e}")

    def normalize_text(self, text: str) -> str:
        """Normalize text by removing punctuation and converting to lowercase."""
        text = text.lower()  # Convert to lowercase
        text = "".join([char for char in text if char not in string.punctuation])  # Remove punctuation
        return text

    def lemmatize_text(self, text: str) -> str:
        """Lemmatize the input text."""
        return " ".join([self.lemmatizer.lemmatize(word) for word in text.split()])

    def remove_stopwords(self, text: str) -> str:
        """Remove stopwords from the text."""
        return " ".join([word for word in text.split() if word not in self.stop_words])

    def text_preprocessing(self):
        """Apply text preprocessing to relevant columns."""
        if self.df is None:
            logger.error("DataFrame is not loaded. Please run load_cleaning() first.")
            return
        
        logger.info("Starting text preprocessing...")
        for column in self.text_columns:
            if column in self.df.columns:
                try:
                    self.df[column] = self.df[column].astype(str).apply(self.normalize_text)
                    self.df[column] = self.df[column].apply(self.lemmatize_text)
                    self.df[column] = self.df[column].apply(self.remove_stopwords)
                    logger.info(f"Text preprocessing completed for column: {column}")
                except Exception as e:
                    logger.error(f"Error occurred while processing column {column}: {str(e)}")
                    raise

    def save_cleaned_data(self):
        """Save the cleaned dataset to a CSV file."""
        if self.df is not None:
            try:
                # Create the output directory if it doesn't exist
                if not os.path.exists(os.path.dirname(self.output_path)):
                    os.makedirs(os.path.dirname(self.output_path))
                    logger.info(f"Output directory created at {os.path.dirname(self.output_path)}")

                logger.info(f"Saving cleaned data to {self.output_path}...")
                self.df.to_csv(self.output_path, index=False)
                logger.info(f"Cleaned data saved to {self.output_path}")
            except Exception as e:
                logger.error(f"Error saving cleaned data: {e}")
        else:
            logger.error("Error: No data available to save.")

    def get_cleaned_data(self):
        """Returns the cleaned DataFrame."""
        return self.df

    def clean(self):
        """Main function to execute the entire cleaning process."""
        logger.info("Starting the cleaning process...")
        self.load_cleaning()

        if self.df is None or self.df.empty:
            logger.error("Error: No data loaded. Cleaning process aborted.")
            return

        self.text_preprocessing()
        self.save_cleaned_data()
        logger.info("Cleaning process completed successfully.")
