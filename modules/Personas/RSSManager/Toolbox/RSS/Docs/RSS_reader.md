# RSS Feed Reader

The RSS Feed Reader is a module within the SCOUT (Scalable Cognitive Operations Unified Team) application that allows users to retrieve and process RSS feeds. It provides functionality to add and manage feeds, retrieve feed entries, and extract relevant information from those entries. This module is particularly useful for staying up-to-date with news, blogs, podcasts, or any other content distributed via RSS feeds.

## Features

1. **Feed Management**: The module allows users to add and remove RSS feeds using their URL addresses. Users can maintain a list of their preferred feeds for easy access and management.

2. **Feed Retrieval**: The module retrieves and parses RSS feeds by sending requests to the specified feed URLs. It extracts relevant information from the feed, such as titles, links, publication dates, and summaries.

3. **Entry Listing**: Users can retrieve a list of entries for a specific RSS feed. The module provides methods to fetch the entries associated with a particular feed URL.

4. **Entry Details**: The module allows users to retrieve detailed information for each entry within a feed. It extracts the title, link, publication date, and summary of individual entries, providing a comprehensive view of the content.

5. **Logging**: The RSS Feed Reader incorporates a logging mechanism to track and record various events and errors during the feed retrieval and processing. The logs are stored in a file named `SCOUT.log` and can be valuable for debugging and monitoring purposes.

## Usage

To utilize the RSS Feed Reader module within SCOUT, follow these steps:

1. Ensure that the necessary dependencies are installed, particularly the `feedparser` library, which is used for parsing RSS feeds.

2. Import the `RSSFeedReader` class from the `rss_feed_reader` module in your SCOUT application.

3. Create an instance of the `RSSFeedReader` class:
   ```python
   reader = RSSFeedReader()
   ```

4. Add RSS feeds to the reader using the `add_feed` method, providing the URL address of the feed:
   ```python
   reader.add_feed("https://www.example.com/feed")
   ```

5. Manage the feeds as needed:
   - To remove a feed, use the `remove_feed` method, specifying the feed URL:
     ```python
     reader.remove_feed("https://www.example.com/feed")
     ```
   - To retrieve a list of currently added feeds, use the `get_feeds` method:
     ```python
     feeds = reader.get_feeds()
     ```

6. Retrieve the entries for a specific feed using the `get_feed_entries` method, providing the feed URL:
   ```python
   entries = reader.get_feed_entries("https://www.example.com/feed")
   ```

7. Access the detailed information for each entry using the `get_entry_details` method, passing the entry object:
   ```python
   details = reader.get_entry_details(entries[0])
   ```

   - The `details` dictionary will contain the following keys:
     - `title`: The title of the entry.
     - `link`: The URL link to the full article or content.
     - `published`: The publication date of the entry.
     - `summary`: A summary or excerpt of the entry's content.

## Customization

The RSS Feed Reader module can be customized based on your specific requirements:

- **Logging**: You can adjust the logging level by calling the `adjust_logging_level` function and passing the desired level (e.g., 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL').

## Dependencies

The RSS Feed Reader module relies on the following dependencies:

- `feedparser`: Used for parsing RSS feeds and extracting relevant information.

Make sure to install the `feedparser` library before using the RSS Feed Reader module.

## Limitations

- The accuracy and completeness of the retrieved feed information depend on the structure and formatting of the RSS feed. Some feeds may have non-standard formats or missing information, which may affect the module's ability to extract all desired details.

- The module relies on the availability and accessibility of the RSS feeds. If a feed URL is invalid, inaccessible, or has been modified, the module may not be able to retrieve the feed or its entries.

## Troubleshooting

If you encounter any issues while using the RSS Feed Reader module, consider the following:

- Check the `SCOUT.log` file for any error messages or exceptions that occurred during the feed retrieval and processing.
- Ensure that you have a stable internet connection to retrieve RSS feeds.
- Verify that the provided feed URLs are valid and accessible.
- Make sure you have the `feedparser` library installed and properly imported in your SCOUT application.

For further assistance or to report any bugs, please contact the SCOUT development team.

## Example

Here's an example of how to use the RSS Feed Reader module within SCOUT:

```python
from modules.Tools.Internet_Tools.rss_feed_reader import RSSFeedReader

# Create an instance of the RSSFeedReader
reader = RSSFeedReader()

# Add an RSS feed
reader.add_feed("https://www.example.com/feed")

# Retrieve the list of added feeds
feeds = reader.get_feeds()
print("Added Feeds:")
for feed in feeds:
    print(feed)

# Retrieve entries for a specific feed
entries = reader.get_feed_entries("https://www.example.com/feed")

# Print the details of each entry
for entry in entries:
    details = reader.get_entry_details(entry)
    print("Title:", details['title'])
    print("Link:", details['link'])
    print("Published:", details['published'])
    print("Summary:", details['summary'])
    print("---")