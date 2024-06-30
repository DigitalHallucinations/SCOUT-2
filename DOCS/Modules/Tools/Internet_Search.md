# Internet Search Tool

The Internet Search Tool is an essential component of the SCOUT (Scalable Cognitive Operations Unified Team) application. It empowers users to perform web searches and retrieve relevant information directly within the SCOUT interface. The tool utilizes the SerpAPI to fetch search results from Google and employs web scraping techniques to extract additional details from the top search result page.

## Features

1. **Search Functionality**: Users can input a search query, and the tool will retrieve the corresponding search results from Google using the SerpAPI.

2. **Top Result Navigation**: In addition to presenting the search results, the tool automatically navigates to the top search result page and extracts pertinent information, such as the page title and main content.

3. **Optional Result Summarization**: The tool provides an option to generate a concise summary of the search results and the extracted information from the top result page using OpenAI's GPT-3.5-turbo-16k model. This summary offers users a quick overview of the most relevant information related to their search query.

4. **Logging**: The tool incorporates a logging mechanism to track and record various events and errors during the search process. The logs are stored in a file named `SCOUT.log` and can be valuable for debugging and monitoring purposes.

## Usage

To utilize the Internet Search Tool within SCOUT, follow these steps:

1. Ensure that the necessary dependencies are installed, including `requests`, `beautifulsoup4`, and the `OpenAIAPI` module.

2. Set up the required environment variables:
   - `SERPAPI_KEY`: Your SerpAPI API key for accessing the Google search functionality.

3. Import the `InternetSearch` class from the `internet_search` module in your SCOUT application.

4. Create an instance of the `InternetSearch` class, optionally providing your SerpAPI API key:
   ```python
   search_tool = InternetSearch(api_key='your_api_key')
   ```

5. Call the `_search` method of the `InternetSearch` instance, passing the search query and the optional `summarize` parameter:
   ```python
   status_code, search_results = await search_tool._search('your search query', summarize=True)
   ```

   - If `summarize` is set to `True`, the tool will generate a summary of the search results and the extracted information from the top result page.
   - If `summarize` is set to `False` (default), the summary will not be generated.

6. The `_search` method returns a tuple containing the HTTP status code and the search results. If the status code is 200, the search results will include the original search results from SerpAPI, as well as the extracted information from the top result page. If `summarize` was set to `True`, the search results will also include the generated summary.

## Data Returned to the Model

The Internet Search Tool returns the following data to the model:

1. **Search Results**: The tool provides the original search results obtained from the SerpAPI. These results include the page title, URL, and a snippet of the page content for each search result.

2. **Top Result Information**: The tool extracts additional information from the top search result page, such as the page title and the main content of the page. This information is included in the search results returned to the model.

3. **Summary (Optional)**: If the `summarize` parameter is set to `True`, the tool generates a concise summary of the search results and the extracted information from the top result page using OpenAI's GPT-3.5-turbo-16k model. This summary is returned to the model, providing a condensed overview of the most relevant information related to the search query.

The model can then utilize this data to provide informed responses, generate insights, or perform further analysis based on the search results and the extracted information.

## Customization

The Internet Search Tool can be customized and extended based on your specific requirements:

- **Logging**: You can adjust the logging level by calling the `adjust_logging_level` function and passing the desired level (e.g., 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL').

- **Page Content Extraction**: The `extract_page_info` function can be modified to extract additional information from the top result page based on the specific structure and layout of the website. You can use BeautifulSoup's methods and selectors to locate and extract the desired elements.

- **Summarization**: The `_summarize_results` method uses OpenAI's GPT-3.5-turbo-16k model for generating the summary. You can experiment with different models or adjust the prompt to customize the summarization process according to your needs.

## Dependencies

The Internet Search Tool relies on the following dependencies:

- `requests`: Used for making HTTP requests to the SerpAPI and fetching web page content.
- `beautifulsoup4`: Used for parsing HTML and extracting information from web pages.
- `OpenAIAPI`: Used for generating summaries of the search results using OpenAI's language models.

Make sure to install these dependencies before using the Internet Search Tool.

## Limitations

- The accuracy and relevance of the search results depend on the quality of the SerpAPI and the extracted information from the top result page.
- The tool may not be able to extract information from websites with complex or dynamically generated content.
- The summarization process relies on OpenAI's language models, which may have limitations in understanding and generating summaries for certain types of content.

## Troubleshooting

If you encounter any issues while using the Internet Search Tool, consider the following:

- Check the `SCOUT.log` file for any error messages or exceptions that occurred during the search process.
- Verify that your SerpAPI API key is valid and has sufficient quota for making requests.
- Ensure that you have a stable internet connection to fetch search results and web page content.
- If the tool fails to extract information from a specific website, inspect the website's structure and adjust the `extract_page_info` function accordingly.

For further assistance or to report any bugs, please contact the SCOUT development team.

---

This document provides an overview of the Internet Search Tool, its features, usage instructions, the data it returns to the model, customization options, dependencies, limitations, and troubleshooting tips. It serves as a comprehensive guide for users and developers working with the tool within the SCOUT application.