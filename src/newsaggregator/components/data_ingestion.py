import os
from bs4 import BeautifulSoup
from datetime import datetime
from src.newsaggregator import logger
import requests
from src.newsaggregator.entity.config_entity import (DataIngestionConfig)
import pandas as pd

class DataIngestion:
    def __init__(self, config:DataIngestionConfig):
        self.config = config
        self.News_websites = config.News_websites  
        self.output_path = config.output_path

    def clean_text(self, text):
        """Clean HTML tags and unnecessary whitespace."""
        return ' '.join(BeautifulSoup(text, 'xml').stripped_strings) if text else 'N/A'

    def parse_pub_date(self, date_str):
        """Parse the publication date into a standardized format."""
        formats = ['%a, %d %b %Y %H:%M:%S %Z', '%Y-%m-%dT%H:%M:%SZ']  # Add more formats if needed
        for fmt in formats:
            try:
                return datetime.strptime(date_str, fmt)
            except ValueError:
                continue
        return 'N/A'

    def get_feed_entries(self, feed_url, pages=10):
        all_entries = []
        for page in range(1, pages + 1):
            paged_url = f"{feed_url}?paged={page}"
            logger.info(f"Fetching page {page} from {feed_url}")
            try:
                response = requests.get(paged_url, timeout=10)
                response.raise_for_status()
            except requests.exceptions.RequestException as e:
                logger.error(f"Failed to fetch page {page}: {e}")
                break

            soup = BeautifulSoup(response.content, 'html.parser')
            items = soup.find_all('item')

            if not items:
                logger.info("No more entries found.")
                break

            for item in items:
                entry = {
                    'title': item.find('title').text.strip() if item.find('title') else 'N/A',
                    'link': item.find('link').text.strip() if item.find('link') else 'N/A',
                    'description': BeautifulSoup(item.find('description').text, 'html.parser').text.strip() if item.find('description') else 'N/A',
                    'pubDate': self.parse_pub_date(item.find('pubDate').text) if item.find('pubDate') else 'N/A',
                    'category': ', '.join([cat.text.strip() for cat in item.find_all('category')]) if item.find_all('category') else 'N/A'
                }
                all_entries.append(entry)

        return all_entries

    def ingest_data(self, pages=10):
        all_feed_data = []
        for source_name, feed_url in self.News_websites.items():
            entries = self.get_feed_entries(feed_url, pages)
            logger.info(f'RSS Feed done: {source_name}')

            # Add source name to each entry
            for entry in entries:
                entry['source'] = source_name
            all_feed_data.extend(entries)

        # Create a pandas DataFrame
        df = pd.DataFrame(all_feed_data, columns=['source', 'category', 'title', 'link', 'description', 'pubDate'])

        # Remove rows with missing essential fields
        df.dropna(subset=['title', 'link', 'description'], inplace=True)
        
        # Save the DataFrame to CSV
        os.makedirs(self.output_path.parent, exist_ok=True)
        df.to_csv(self.output_path, index=False)
        logger.info(f"Data saved to {self.output_path}")

        return df
