# Web Scraper

The Web Scraper is a module within the SCOUT (Scalable Cognitive Operations Unified Team) application that provides a generic web scraping tool. It enables the LLM model to extract data from any website by specifying the target elements using CSS selectors or XPath expressions. The tool is highly versatile and can handle various scraping scenarios, including pagination, JavaScript-rendered content, and exporting the scraped data in different formats like CSV or JSON.

## Features

1. **Flexible Element Selection**: The Web Scraper allows users to specify the target elements they want to extract from a website using either CSS selectors or XPath expressions. This flexibility enables the tool to adapt to different website structures and layouts.

2. **Pagination Support**: The module can handle pagination when scraping websites with multiple pages. It automatically navigates to the next page and continues scraping until the maximum number of pages is reached or there are no more pages to scrape.

3. **JavaScript Rendering**: The Web Scraper can process JavaScript-rendered content by leveraging the Selenium WebDriver. This feature is particularly useful for scraping dynamic websites that heavily rely on JavaScript to load and display content.

4. **Data Export**: The scraped data can be easily exported in various formats, including CSV and JSON. The module provides methods to save the scraped data to files, making it convenient for further analysis or integration with other systems.

5. **Logging**: The Web Scraper incorporates a logging mechanism to track and record various events and errors during the scraping process. The logs are stored in a file named `SCOUT.log` and can be valuable for debugging and monitoring purposes.

## Usage

To utilize the Web Scraper module within SCOUT, follow these steps:

1. Ensure that the necessary dependencies are installed, including `requests`, `beautifulsoup4`, and `selenium`.

2. Import the `WebScraper` class from the `web_scraper` module in your SCOUT application.

3. Create an instance of the `WebScraper` class, optionally specifying the `use_selenium` and `headless` parameters:
   ```python
   scraper = WebScraper(use_selenium=True, headless=True)
   ```

   - `use_selenium`: Set to `True` if you want to use Selenium WebDriver for scraping JavaScript-rendered content. Default is `False`.
   - `headless`: Set to `True` if you want to run the browser in headless mode (without opening a visible window). Default is `True`.

4. Call the `scrape` method of the `WebScraper` instance, providing the necessary parameters:
   ```python
   url = 'https://example.com'
   target_elements = ['.title', '.description', '.price']
   scraped_data = scraper.scrape(url, target_elements, method='css', paginate=True, max_pages=5, javascript=True)
   ```

   - `url`: The URL of the website to scrape.
   - `target_elements`: A list of CSS selectors or XPath expressions to locate the desired elements on the page.
   - `method`: The method to use for locating elements, either 'css' for CSS selectors or 'xpath' for XPath expressions. Default is 'css'.
   - `paginate`: Set to `True` if pagination is required. Default is `False`.
   - `max_pages`: The maximum number of pages to scrape (optional).
   - `javascript`: Set to `True` if the page requires JavaScript rendering. Default is `False`.

5. The `scrape` method returns the scraped data as a list. You can further process or export the data as needed.

6. To export the scraped data, use the `export_csv` or `export_json` methods:
   ```python
   scraper.export_csv(scraped_data, 'output.csv')
   scraper.export_json(scraped_data, 'output.json')
   ```

7. If you used Selenium WebDriver for scraping, make sure to call the `quit` method to close the browser when you're done:
   ```python
   scraper.quit()
   ```

## Customization

The Web Scraper module can be customized based on your specific requirements:

- **Logging**: You can adjust the logging level by calling the `adjust_logging_level` function and passing the desired level (e.g., 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL').

- **Selenium WebDriver**: If you need to customize the Selenium WebDriver options, you can modify the `setup_selenium` method in the `WebScraper` class.

## Dependencies

The Web Scraper module relies on the following dependencies:

- `requests`: Used for sending HTTP requests to retrieve webpage content.
- `beautifulsoup4`: Used for parsing HTML and extracting data based on CSS selectors or XPath expressions.
- `selenium`: Used for scraping JavaScript-rendered content by automating a web browser.

Make sure to install these dependencies before using the Web Scraper module.

## Limitations

- The accuracy and completeness of the scraped data depend on the structure and consistency of the target website. Changes in the website's HTML structure may require updating the CSS selectors or XPath expressions accordingly.

- Some websites may have anti-scraping measures in place, such as rate limiting, IP blocking, or CAPTCHAs. The Web Scraper module does not include built-in mechanisms to bypass these measures. It is important to respect the website's terms of service and robots.txt file when scraping.

- The performance of the Web Scraper may be affected by factors such as network latency, website response time, and the complexity of the target website. Scraping large amounts of data or multiple pages may take a considerable amount of time.

## Troubleshooting

If you encounter any issues while using the Web Scraper module, consider the following:

- Check the `SCOUT.log` file for any error messages or exceptions that occurred during the scraping process.
- Ensure that you have a stable internet connection to retrieve webpage content.
- Verify that the provided URL is valid and accessible.
- Make sure you have the necessary dependencies installed (`requests`, `beautifulsoup4`, `selenium`).
- If using Selenium WebDriver, ensure that you have the appropriate browser driver installed and available in your system's PATH.

For further assistance or to report any bugs, please contact the SCOUT development team.

---

This documentation provides a comprehensive overview of the Web Scraper module, its features, usage instructions, customization options, dependencies, limitations, and troubleshooting tips. It serves as a detailed guide for users and developers working with the module within the SCOUT application.