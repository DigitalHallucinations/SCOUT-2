# Webpage Retriever

The Webpage Retriever is a module within the SCOUT (Scalable Cognitive Operations Unified Team) application that allows users to retrieve the text content and optionally capture a screenshot of a webpage given its URL address. This module is particularly useful for vision-capable models that can process and analyze webpage screenshots.

## Features

1. **Text Content Retrieval**: The module retrieves the text content of a webpage by sending a GET request to the specified URL and parsing the HTML response using BeautifulSoup.

2. **Screenshot Capture (Optional)**: The module provides an option to capture a screenshot of the webpage using a headless Chrome browser powered by Selenium. This feature is useful for vision-capable models that can process and analyze webpage images.

3. **Logging**: The module incorporates a logging mechanism to track and record various events and errors during the webpage retrieval process. The logs are stored in a file named `SCOUT.log` and can be valuable for debugging and monitoring purposes.

## Usage

To utilize the Webpage Retriever module within SCOUT, follow these steps:

1. Ensure that the necessary dependencies are installed, including `requests`, `beautifulsoup4`, and `selenium`.

2. Make sure you have the Chrome webdriver installed and available in your system's PATH. You can download the Chrome webdriver from the official Selenium website (https://sites.google.com/a/chromium.org/chromedriver/) and place it in a directory that is included in your system's PATH.

3. Import the `WebpageRetriever` class from the `webpage_retriever` module in your SCOUT application.

4. Create an instance of the `WebpageRetriever` class, optionally specifying the timeout duration (default is 10 seconds):
   ```python
   retriever = WebpageRetriever(timeout=10)
   ```

5. Call the `retrieve_page` method of the `WebpageRetriever` instance, passing the URL address and optionally specifying whether to capture a screenshot:
   ```python
   result = await retriever.retrieve_page(url='https://example.com', capture_screenshot=True)
   ```

   - If `capture_screenshot` is set to `True`, the module will capture a screenshot of the webpage along with the text content.
   - If `capture_screenshot` is set to `False` (default), only the text content will be retrieved.

6. The `retrieve_page` method returns a dictionary containing the following keys:
   - `content`: The text content of the webpage.
   - `screenshot`: The base64-encoded screenshot of the webpage (if `capture_screenshot` is set to `True`).

7. You can access the retrieved text content and screenshot from the returned dictionary:
   ```python
   text_content = result['content']
   screenshot_base64 = result['screenshot']
   ```

   - The `text_content` variable will contain the retrieved text content of the webpage.
   - The `screenshot_base64` variable will contain the base64-encoded screenshot of the webpage (if `capture_screenshot` is set to `True`).

## Customization

The Webpage Retriever module can be customized based on your specific requirements:

- **Logging**: You can adjust the logging level by calling the `adjust_logging_level` function and passing the desired level (e.g., 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL').

- **Timeout**: You can specify a custom timeout duration (in seconds) when creating an instance of the `WebpageRetriever` class to control the maximum time allowed for the webpage retrieval process.

## Dependencies

The Webpage Retriever module relies on the following dependencies:

- `requests`: Used for sending HTTP requests to retrieve webpage content.
- `beautifulsoup4`: Used for parsing HTML and extracting text content from the webpage.
- `selenium`: Used for capturing screenshots of the webpage using a headless Chrome browser.

Make sure to install these dependencies before using the Webpage Retriever module.

## Limitations

- The accuracy and completeness of the retrieved text content depend on the structure and formatting of the webpage. Some webpages may have complex layouts or dynamically generated content that may not be fully captured by the module.

- The screenshot capture feature requires the Chrome webdriver to be installed and available in the system's PATH. Ensure that you have the appropriate version of the Chrome webdriver compatible with your Chrome browser version.

- The module may not be able to retrieve content or capture screenshots from websites that require authentication, have strict security measures, or employ anti-scraping techniques.

## Troubleshooting

If you encounter any issues while using the Webpage Retriever module, consider the following:

- Check the `SCOUT.log` file for any error messages or exceptions that occurred during the webpage retrieval process.
- Ensure that you have a stable internet connection to retrieve webpage content and capture screenshots.
- Verify that the provided URL is valid and accessible.
- Make sure you have the necessary dependencies installed, including `requests`, `beautifulsoup4`, and `selenium`.
- Ensure that you have the Chrome webdriver installed and available in your system's PATH.

For further assistance or to report any bugs, please contact the SCOUT development team.

---

This documentation provides an overview of the Webpage Retriever module, its features, usage instructions, customization options, dependencies, limitations, and troubleshooting tips. It serves as a comprehensive guide for users and developers working with the module within the SCOUT application.