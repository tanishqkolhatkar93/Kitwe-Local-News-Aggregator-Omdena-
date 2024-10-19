import requests
from bs4 import BeautifulSoup
import pandas as pd

# List of RSS feed URLs for scraping
RSS_FEED_URLS = {
     'Copperbelt Energy': 'https://cecinvestor.com/search/kitwe/feed/rss2/',
     'ZNBC' : 'https://znbc.co.zm/news/search/kitwe/feed/rss2/',
     'News Invasion 24': 'https://newsinvasion24.com/search/kitwe/feed/rss2/',
     'Mwebantu': 'https://www.mwebantu.com/search/kitwe/feed/rss2/',
     'Lusaka Times': 'https://www.lusakatimes.com/search/kitwe/feed/rss2/',
     'Kitwe Online': 'https://kitweonline.com/search/kitwe/feed/rss2/',
     'Daily Revelation Zambia': 'https://dailyrevelationzambia.com/search/kitwe/feed/rss2/',
     'Zambia Monitor': 'https://www.zambiamonitor.com/search/kitwe/feed/rss2/',
     'Tech Africa News': 'https://www.techafricanews.com/search/kitwe/feed/rss2/',
     'Zambian Eye': 'https://zambianeye.com/search/kitwe/feed/rss2/',
     'DailyMail': 'https://www.daily-mail.co.zm/search/kitwe/feed/rss2/'
}

def fetch_rss_feed(feed_url, page):
    """
    Fetches and parses an RSS feed from the given URL and page number.
    
    Args:
        feed_url (str): The base URL of the RSS feed.
        page (int): The page number to fetch.
    
    Returns:
        BeautifulSoup: Parsed XML content of the RSS feed.
    """
    paged_url = f"{feed_url}?paged={page}"
    response = requests.get(paged_url)

    # Check if the request was successful
    if response.status_code != 200:
        print(f"Failed to fetch page {page}: {response.status_code}")
        return None
    
    # Parse the XML content
    soup = BeautifulSoup(response.content, 'xml')
    return soup

def extract_feed_entries(soup):
    """
    Extracts and formats entries from the parsed RSS feed content.
    
    Args:
        soup (BeautifulSoup): The parsed XML feed content.
    
    Returns:
        list: A list of dictionaries containing the extracted feed data.
    """
    entries = []
    
    # Find all items (news entries) in the RSS feed
    items = soup.find_all('item')
    
    if not items:
        return entries  # No items found
    
    # Extract the required data from each item
    for item in items:
        entry = {
            'title': item.find('title').text if item.find('title') else 'N/A',
            'link': item.find('link').text if item.find('link') else 'N/A',
            'description': item.find('description').text if item.find('description') else 'N/A',
            'pubDate': item.find('pubDate').text if item.find('pubDate') else 'N/A',
            'category': ', '.join([cat.text for cat in item.find_all('category')]) if item.find_all('category') else 'N/A'
        }
        entries.append(entry)
    
    return entries

def collect_all_feed_entries(feed_url, max_pages=10):
    """
    Collects all feed entries from paginated RSS feeds.
    
    Args:
        feed_url (str): The base URL of the RSS feed.
        max_pages (int): The maximum number of pages to fetch.
    
    Returns:
        list: A list of dictionaries containing all extracted feed entries.
    """
    all_entries = []
    
    for page in range(1, max_pages + 1):
        print(f"Fetching page {page} from {feed_url}")
        
        # Fetch the RSS feed for the given page
        soup = fetch_rss_feed(feed_url, page)
        if soup is None:
            break
        
        # Extract feed entries
        entries = extract_feed_entries(soup)
        
        # If no entries are found, stop pagination
        if not entries:
            print(f"No entries found on page {page}, stopping.")
            break
        
        all_entries.extend(entries)
    
    return all_entries

# Loop through each RSS feed URL and collect data
all_feed_data = []
for feed_url in RSS_FEED_URLS:
    entries = collect_all_feed_entries(feed_url, max_pages=10)
    print(f"RSS Feed done: {feed_url}")
    
    # Add source name (feed URL) to each entry
    for entry in entries:
        entry['source'] = feed_url  # Can be replaced with a more descriptive source name
    all_feed_data.extend(entries)

# Create a pandas DataFrame from the collected data
df = pd.DataFrame(all_feed_data, columns=['source', 'category', 'title', 'link', 'description', 'pubDate'])

# Display the first few rows of the DataFrame
df.head()

# Optional: Save the DataFrame to a CSV file
df.to_csv('rss_feed_data_bs_jupyter.csv', index=False)
