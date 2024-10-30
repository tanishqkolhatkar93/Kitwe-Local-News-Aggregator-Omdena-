import os
import logging
from datetime import datetime
import requests
import pandas as pd
import yaml
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import KNeighborsClassifier
from src.newsaggregator.entity.config_entity import DataCategorizingConfig
from src.newsaggregator import logger

class DataCategorizing:
    def __init__(self, config: DataCategorizingConfig):
        self.input_path = config.input_path
        self.output_path = config.output_path
        self.categories_keywords = config.categories_keywords
        
        logger.info("Initializing DataLabelling with input_path: %s and output_path: %s", self.input_path, self.output_path)
        
        # Load data
        self.data = self.load_data()
        self.vectorizer = TfidfVectorizer(max_features=5000)
        self.knn = KNeighborsClassifier(n_neighbors=5)

    def load_data(self):
        """Load and process initial data."""
        logger.info("Loading data from %s", self.input_path)
        self.data = pd.read_csv(self.input_path)
        self.data['Description'] = self.data['Description'].astype(str)
        logger.info("Data loaded successfully. Number of records: %d", len(self.data))
        return self.data

    def prioritize_category(self, description):
        """Assign a single category based on highest keyword count."""
        keyword_count = {}
        for category, keywords in self.categories_keywords.items():
            count = sum(description.lower().count(keyword) for keyword in keywords)
            if count > 0:
                keyword_count[category] = count
        if keyword_count:
            assigned_category = max(keyword_count, key=keyword_count.get)
            logger.debug("Assigned category '%s' for description: %s", assigned_category, description)
            return assigned_category
        else:
            logger.debug("No keywords found for description: %s. Assigned category: 'Uncategorized'", description)
            return 'Uncategorized'

    def assign_single_categories(self):
        """Apply single category based on keyword prioritization."""
        if self.categories_keywords is None:
            logger.error("categories_keywords is None. Ensure config.yaml is loaded correctly.")
            raise ValueError("categories_keywords is None. Ensure config.yaml is loaded correctly.")

        logger.info("Assigning single categories to descriptions...")
        self.data['categories'] = self.data['Description'].apply(self.prioritize_category)
        self.data['categories'] = self.data['categories'].str.capitalize()
        logger.info("Single categories assigned. Sample data:\n%s", self.data[['Description', 'categories']].head())

    def train_knn_classifier(self):
        """Train the KNN model to predict categories for uncategorized entries."""
        categorized_df = self.data[self.data['categories'] != 'Uncategorized']
        uncategorized_df = self.data[self.data['categories'] == 'Uncategorized']
        
        # Ensure there is enough data to train
        if categorized_df.empty:
            logger.error("No categorized data available for training.")
            raise ValueError("No categorized data available for training.")

        logger.info("Training KNN classifier with %d categorized entries...", len(categorized_df))

        # Training data
        X_train = categorized_df['Description']
        y_train = categorized_df['categories']
        
        # Convert text to TF-IDF vectors
        X_train_tfidf = self.vectorizer.fit_transform(X_train)
        
        # Train KNN classifier
        self.knn.fit(X_train_tfidf, y_train)
        
        logger.info("KNN classifier trained successfully.")

        # Predict uncategorized entries
        if not uncategorized_df.empty:
            logger.info("Predicting categories for %d uncategorized entries...", len(uncategorized_df))
            X_test_tfidf = self.vectorizer.transform(uncategorized_df['Description'])
            y_pred = self.knn.predict(X_test_tfidf)
            self.data.loc[self.data['categories'] == 'Uncategorized', 'categories'] = y_pred
            logger.info("Predicted categories for uncategorized entries.")

    def save_output(self):
        """Save the categorized DataFrame to the specified output path."""
        logger.info("Saving categorized data to %s", self.output_path)
        self.data.to_csv(self.output_path, index=False)
        logger.info("Categorized data saved successfully.")

    def get_categorized_data(self):
        """Return the categorized DataFrame."""
        return self.data

    def categorize(self):
        """Run all categorization steps in sequence."""
        logger.info("Starting the categorization process...")
        self.assign_single_categories()  # Ensure this is called first
        self.train_knn_classifier()
        self.save_output()
        logger.info("Categorization process completed.")
        return self.get_categorized_data()
