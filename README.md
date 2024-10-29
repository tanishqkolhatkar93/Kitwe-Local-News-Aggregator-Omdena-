# Kitwe-Focused News Project-Omdena

**A machine learning project to predict customer churn, designed to help businesses retain valuable customers and reduce revenue loss.**

---

## 🔥 Project Overview

The Kitwe-Focused News Project aims to gather, analyze, and interpret local news articles centered around Kitwe, Zambia, by creating a structured dataset from reputable Zambian news sources. This README will document each stage of the project, beginning with Data Collection and continuing through Data Preprocessing, Data Analysis, and Insights Generation.

---

## Project Stages

-  Data Collection
-  Data Preprocessing

---

## 👨‍💻 Author

Hi! I'm **Ambigathi**, a fresher data scientist with experience in **machine learning**, **API development**, and **model deployment**. I'm passionate about creating solutions that have real-world impact.

- **LinkedIn**: [linkedin.com/in/ambigathi](https://www.linkedin.com/in/ambigathi)
- **GitHub**: [github.com/yourusername](https://github.com/Ambigapathi-V)

---

## 1. Data Collection

The  Data Collection  stage focuses on gathering Kitwe-centered news articles to create a dataset for analysis.

### Approach
To collect relevant articles, we employed a systematic approach using RSS (Really Simple Syndication) feeds from Zambian news websites. The process involves:
- RSS Feed Access: Accessing RSS feeds from reputable sources to ensure real-time, structured updates.
- Filtering by “Kitwe”: Using a Python script to retrieve only articles tagged with "Kitwe" from these feeds, ensuring that the dataset remains focused on Kitwe-related news.
- Iterative Data Extraction: Configuring the script to retrieve up to 1,000 pages per source to maximize data collection.

## Tools and Libraries
- Python: The primary programming language for data collection.
- Feedparser: Used to parse and extract content from RSS feeds efficiently.
- CSV Library: Employed to store the data in a structured CSV file format, with each row representing a unique news article.

## Data Structure
Each article entry in the dataset includes:

- Source: Origin of the news article
- Category Tags: Relevant categories or tags from the source
- Headline: Title of the article
- Link: URL to the article
- Description: Brief description of the article
- Publication Date: Date the article was published
- Author: Author of the article, if available
##  Challenges
Some challenges encountered during the data collection stage include:

- Inconsistent Data Fields: Some articles lacked information like publication dates or descriptions, resulting in gaps in the dataset.
- Irregular Pagination: Non-standard pagination on some sites caused the script to halt, requiring adjustments.
- Connection Interruptions: Occasional connectivity issues with RSS feeds led to delays. Retry mechanisms were implemented, but some interruptions persisted.
- Duplicate Entries: Repeated articles across pages required duplicate filtering for data integrity.



## Limitations
- RSS Dependence: Only articles indexed by the RSS feeds were collected, potentially limiting coverage.
- Incomplete Metadata: Some articles lacked sufficient details, complicating classification efforts.
- Manual Quality Checks: Minor manual checks introduced a small margin for human error.

---

## 2.Data Cleaning

This stage focuses on improving the dataset's quality for analysis.

### Key Steps
1. Load Data: Import the raw dataset from a CSV file.
2. Handle Missing Values: Remove or impute missing entries.
3. Remove Duplicates: Eliminate duplicate articles based on headline and publication date.
4. Text Preprocessing:
- Lowercase text.
- Remove special characters and stop words.
- Lemmatize words.
5. Normalize Text: Address URLs to reduce distractions.
### Logging
- Track counts before and after cleaning, including any entries removed.
## Challenges
- Inconsistent article titles can complicate duplicate detection.
- Articles with incomplete information require careful handling.


## 🛠️ Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/Ambigapathi-V/Kitwe-Local-News-Aggregator-Omdena-
    ```
2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Run the pipeline :
    ```bash
    python main.py
    ```

---



## 💬 Feedback

If you have any feedback, feel free to reach out via [feedback](mailto:ambigapathikavin2@gmail.com).

---

## 🌟 Support

For support, please contact [support](mailto:ambigapathikavin2@gmail.com).
