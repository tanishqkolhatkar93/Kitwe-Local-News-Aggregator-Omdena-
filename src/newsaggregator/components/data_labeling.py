
import pandas as pd
from urllib.parse import urlparse
import re
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.metrics.pairwise import cosine_similarity
from textblob import TextBlob
import numpy as np
from src.newsaggregator import logger


class DataLabelling:
    def __init__(self, config):
        # Load the input data and assign it to the `data` attribute
        self.data = pd.read_csv(config.input_path)
        self.reputable_sources = config.reputable_sources
        self.suspicious_domain_patterns = re.compile(config.suspicious_domain_patterns[0])
        self.sensational_keywords = config.sensational_keywords
        self.thresholds = config.thresholds
        self.output_path = config.output_path

        # Fill NaN values in important columns to avoid issues in processing
        self.data['Description'] = self.data['Description'].fillna("")
        self.data['Headline'] = self.data['Headline'].fillna("")
        self.data['Author'] = self.data['Author'].fillna("")

        # Log successful initialization
        logger.info("DataLabelling class initialized with input data and configuration.")
        logger.debug(f"Input data shape: {self.data.shape}")

    def check_source_credibility(self, url):
        parsed_url = urlparse(url)
        domain = parsed_url.netloc.lower()
        credibility = 0  # Default to neutral
        
        if any(source in domain for source in self.reputable_sources):
            credibility = -1  # Reputable source
            logger.debug(f"URL '{url}' found to be a reputable source.")
        elif self.suspicious_domain_patterns.search(domain):
            credibility = 1  # Suspicious source
            logger.debug(f"URL '{url}' found to be suspicious.")
        
        return credibility

    def detect_clickbait(self, headline):
        if not isinstance(headline, str):
            logger.debug("Headline is not a string.")
            return 0
        excessive_punctuation = len(re.findall(r'[!?.]{2,}', headline)) > 0
        all_caps = headline.isupper()
        provocative_words = any(word in headline.lower() for word in [
            'shocking', 'unbelievable', "you wont believe", 'secret', 
            'amazing', 'incredible'
        ])
        if excessive_punctuation or all_caps or provocative_words:
            logger.debug(f"Clickbait detected in headline: {headline}")
            return 1
        return 0

    def count_sensational_keywords(self, description):
        if not isinstance(description, str):
            logger.debug("Description is not a string.")
            return 0
        count = sum(description.lower().count(word) for word in self.sensational_keywords)
        logger.debug(f"Sensational keywords counted: {count} in description.")
        return count

    def apply_topic_modeling(self):
        logger.info("Applying topic modeling...")
        count_vectorizer = CountVectorizer(max_features=300, stop_words='english')
        count_data = count_vectorizer.fit_transform(self.data['Description'].astype(str))
        
        lda = LatentDirichletAllocation(n_components=5, random_state=42)
        lda.fit(count_data)
        topic_distribution = lda.transform(count_data)
        
        dominant_topics = topic_distribution.argmax(axis=1)
        logger.debug(f"Dominant topics assigned: {dominant_topics}")
        return dominant_topics

    def get_sentiment_score(self, text):
        if not isinstance(text, str):
            logger.debug("Sentiment text is not a string.")
            return 0
        try:
            sentiment = TextBlob(text).sentiment
            logger.debug(f"Sentiment score calculated: {sentiment.polarity} for text: {text}")
            return sentiment.polarity
        except Exception as e:
            logger.error(f"Error calculating sentiment: {e}")
            return 0

    def check_mismatch_headline_description(self, row):
        headline, description = row['Headline'], row['Description']
        if not (isinstance(headline, str) and isinstance(description, str)):
            logger.debug("Headline or description is not a string.")
            return 0
        tfidf_vectorizer = TfidfVectorizer(stop_words='english')
        combined_text = [headline, description]
        tfidf_matrix = tfidf_vectorizer.fit_transform(combined_text)
        similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
        mismatch = similarity[0][0] < 0.3
        if mismatch:
            logger.debug(f"Mismatch detected between headline and description: {headline} | {description}")
        return mismatch

    def check_excessive_capitalization(self, text):
        if not isinstance(text, str):
            logger.debug("Text is not a string.")
            return 0
        words = text.split()
        capitalized_words = [word for word in words if word.isupper() and len(word) > 1]
        excessive = len(capitalized_words) > self.thresholds['excessive_capitalization']
        if excessive:
            logger.debug(f"Excessive capitalization detected in text: {text}")
        return excessive

    def check_vague_author(self, author):
        if not isinstance(author, str):
            logger.debug("Author is not a string.")
            return 0
        vague_authors = ['admin', 'editor', 'newsroom', 'staff', 'unknown']
        is_vague = any(vague_name in author.lower() for vague_name in vague_authors)
        if is_vague:
            logger.debug(f"Vague author detected: {author}")
        return is_vague

    def count_suspicious_links(self, description):
        if not isinstance(description, str):
            logger.debug("Description is not a string.")
            return 0
        urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\\\(\\\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', description)
        count = len(urls)
        logger.debug(f"Suspicious links counted: {count} in description.")
        return count

    def check_short_sensational_description(self, description):
        if not isinstance(description, str):
            logger.debug("Description is not a string.")
            return 0
        description_length = len(description)
        sensational_word_count = self.count_sensational_keywords(description)
        if description_length < 100 and sensational_word_count > 1:
            logger.debug(f"Short sensational description detected: {description}")
            return 1
        return 0

    def determine_fake_news(self):
        logger.info("Determining fake news labels...")
        # Compute indicators and save directly to columns in `self.data`
        self.data['Source_Credibility'] = self.data['Link'].apply(self.check_source_credibility)
        self.data['Headline_Type'] = self.data['Headline'].apply(self.detect_clickbait)
        self.data['Sensational_Keyword_Count'] = self.data['Description'].apply(self.count_sensational_keywords)
        self.data['Dominant_Topic'] = self.apply_topic_modeling()
        self.data['Sentiment_Score'] = self.data['Description'].apply(self.get_sentiment_score)
        self.data['Excessive_Capitalization'] = self.data['Headline'].apply(self.check_excessive_capitalization)
        self.data['Headline_Description_Mismatch'] = self.data.apply(self.check_mismatch_headline_description, axis=1)
        self.data['Vague_Author'] = self.data['Author'].apply(self.check_vague_author)
        self.data['Suspicious_Links_Count'] = self.data['Description'].apply(self.count_suspicious_links)
        self.data['Short_Sensational_Description'] = self.data['Description'].apply(self.check_short_sensational_description)

        # Logging output to examine the distribution of the indicators
        logger.info("Indicators computed successfully. Summary statistics:")
        logger.info(self.data[['Source_Credibility', 'Headline_Type', 'Sensational_Keyword_Count', 
                               'Dominant_Topic', 'Sentiment_Score', 'Excessive_Capitalization', 
                               'Headline_Description_Mismatch', 'Vague_Author', 'Suspicious_Links_Count', 
                               'Short_Sensational_Description']].describe())

        # Use `apply` to consolidate indicators into 'Target_final'
        self.data['Target_final'] = self.data.apply(
            lambda row: self.enhanced_determine_fake_news(
                row,
                row['Source_Credibility'],
                row['Headline_Type'],
                row['Sensational_Keyword_Count'],
                row['Dominant_Topic'],
                row['Sentiment_Score'],
                row['Excessive_Capitalization'],
                row['Headline_Description_Mismatch'],
                row['Vague_Author'],
                row['Suspicious_Links_Count'],
                row['Short_Sensational_Description']
            ), axis=1
        )

        logger.info("Target_final label distribution:\n%s", self.data['Target_final'].value_counts())

        return self.data

    def enhanced_determine_fake_news(
        self, row, source_credibility, headline_type, sensational_keyword_count,
        dominant_topic, sentiment_score, excessive_capitalization, 
        headline_description_mismatch, vague_author, suspicious_links_count, 
        short_sensational_description
    ):
        logger.debug(f"Evaluating row: {row['Headline']} | {row['Description']}")
        
        # Decision logic based on the computed indicators
        if source_credibility == 1 or headline_type == 1:
            logger.debug("Marking as fake due to suspicious source or clickbait.")
            return 1
        if sensational_keyword_count > 2:
            logger.debug("Marking as fake due to excessive sensational keywords.")
            return 1
        if dominant_topic == 4:  # Assuming topic 4 is fake news-related
            logger.debug("Marking as fake due to dominant topic.")
            return 1
        if sentiment_score < 0:
            logger.debug("Marking as fake due to negative sentiment.")
            return 1
        if excessive_capitalization:
            logger.debug("Marking as fake due to excessive capitalization.")
            return 1
        if headline_description_mismatch:
            logger.debug("Marking as fake due to headline-description mismatch.")
            return 1
        if vague_author:
            logger.debug("Marking as fake due to vague author.")
            return 1
        if suspicious_links_count > 1:
            logger.debug("Marking as fake due to suspicious links.")
            return 1
        if short_sensational_description:
            logger.debug("Marking as fake due to short sensational description.")
            return 1
        
        logger.debug("Marking as real news.")
        return 0

    def save_to_csv(self):
        logger.info("Saving labeled data to CSV.")
        self.data.to_csv(self.output_path, index=False)
        logger.info(f"Labeled data saved to {self.output_path}.")
