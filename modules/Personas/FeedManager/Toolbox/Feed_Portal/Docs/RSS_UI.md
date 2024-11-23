# RSS Feed Reader UI

The RSS Feed Reader UI is a graphical user interface (GUI) component that provides a user-friendly interface for interacting with the RSS Feed Reader module. It allows users to add, remove, and manage RSS feeds, as well as view and explore feed entries.

## Features

1. **Feed Management**: The UI allows users to add new RSS feeds by entering the feed URL and an optional category. Users can also remove existing feeds from the list.

2. **Feed Listing**: The UI displays a list of all the added RSS feeds, showing the feed URL and its associated category.

3. **Entry Listing**: When a feed is selected from the list, the UI retrieves and displays the entries associated with that feed. Users can browse through the list of entries and select an entry to view its details.

4. **Entry Details**: The UI provides a dedicated section to display the detailed information of a selected entry. It shows the entry's title, link, publication date, and summary.

5. **Configuration**: The UI allows users to configure various settings related to the RSS Feed Reader, such as the number of entries to display per feed, the refresh interval for updating the feeds, and the display format for presenting the entries.

6. **Logging**: The UI integrates with the logging mechanism of the RSS Feed Reader module, displaying log messages and errors in the console or a designated log file.

## Usage

To use the RSS Feed Reader UI, follow these steps:

1. Ensure that the necessary dependencies are installed, including the `tkinter` library for creating the graphical interface.

2. Import the `RSSFeedReaderUI` class from the `RSSFeedReaderUI` module in your application.

3. Create an instance of the `RSSFeedReaderUI` class, passing the root window as an argument:
   ```python
   root = tk.Tk()
   ui = RSSFeedReaderUI(root)
   ```

4. Start the main event loop of the GUI:
   ```python
   root.mainloop()
   ```

5. Interact with the RSS Feed Reader UI:
   - To add a new feed, enter the feed URL and category in the respective entry fields and click the "Add Feed" button.
   - To remove a feed, select the feed from the list and click the "Remove Feed" button.
   - To view the entries of a feed, click on the feed in the list. The entries will be displayed in the entry list section.
   - To view the details of an entry, click on the entry in the entry list. The entry details will be shown in the entry details section.

6. Customize the UI settings:
   - Click on the "Settings" button to open the settings window.
   - Adjust the desired settings, such as the number of entries per feed, refresh interval, and display format.
   - Click the "Save" button to apply the changes.

## Integration with RSS Feed Reader Module

The RSS Feed Reader UI is tightly integrated with the RSS Feed Reader module (`rss_feed_reader.py`). The UI utilizes the functionality provided by the module to perform various operations:

- When a new feed is added through the UI, it calls the `add_feed` method of the `RSSFeedReader` instance to add the feed to the underlying data structure.
- When a feed is removed through the UI, it calls the `remove_feed` method of the `RSSFeedReader` instance to remove the feed from the data structure.
- When a feed is selected in the UI, it calls the `get_feed_entries` method of the `RSSFeedReader` instance to retrieve the entries associated with that feed.
- When an entry is selected in the UI, it calls the `get_entry_details` method of the `RSSFeedReader` instance to retrieve the detailed information of that entry.

The UI also utilizes the logging functionality of the RSS Feed Reader module to display log messages and errors.

## Customization

The RSS Feed Reader UI can be customized to match the desired theme and design. The following aspects of the UI can be modified:

- **Colors**: The color scheme of the UI can be adjusted by modifying the color constants in the code, such as `self.window_bg`, `self.font_color`, `self.button_bg`, etc.

- **Fonts**: The font style and size used in the UI can be changed by modifying the `font_style` variable and specifying the desired font family and size.

- **Layout**: The layout of the UI elements can be rearranged or resized by adjusting the grid coordinates and column/row spans in the code.

- **Additional Features**: New features or functionalities can be added to the UI by extending the existing code and creating new widgets or interactions.

## Dependencies

The RSS Feed Reader UI relies on the following dependencies:

- `tkinter`: The standard Python library for creating graphical user interfaces.
- `rss_feed_reader`: The RSS Feed Reader module that provides the core functionality for managing and retrieving RSS feeds and entries.

Make sure to have these dependencies installed and properly imported in your application.

## Troubleshooting

If you encounter any issues while using the RSS Feed Reader UI, consider the following:

- Check the console or log file for any error messages or exceptions that occurred during the execution of the UI.
- Ensure that the RSS Feed Reader module is properly integrated and functioning correctly.
- Verify that the necessary dependencies are installed and properly imported.
- Review the code for any syntax errors or logical inconsistencies.

For further assistance or to report any bugs, please refer to the project's issue tracker or contact the development team.

## Example

Here's an e## RSS Feed Reader UI

The RSS Feed Reader UI is a graphical user interface (GUI) component that provides a user-friendly interface for interacting with the RSS Feed Reader module. It allows users to add, remove, and manage RSS feeds, as well as view and explore feed entries.

### Features

1. **Feed Management**: The UI allows users to add new RSS feeds by entering the feed URL and an optional category. Users can also remove existing feeds from the list.

2. **Feed Listing**: The UI displays a list of all the added RSS feeds, showing the feed URL and its associated category.

3. **Entry Listing**: When a feed is selected from the list, the UI retrieves and displays the entries associated with that feed. Users can browse through the list of entries and select an entry to view its details.

4. **Entry Details**: The UI provides a dedicated section to display the detailed information of a selected entry. It shows the entry's title, link, publication date, and summary.

5. **Entry Removal**: Users can remove a specific entry from a feed by selecting the entry and clicking the "Remove Entry" button.

6. **Configuration**: The UI allows users to configure various settings related to the RSS Feed Reader, such as font style, colors, and refresh interval. The settings are loaded from a configuration file (`config.ini`) and can be customized.

7. **Logging**: The UI integrates with the logging mechanism of the RSS Feed Reader module, displaying log messages and errors in the console or a designated log file.

8. **Tooltips**: The UI provides tooltips for various buttons and widgets to provide helpful information to the user when hovering over them.

9. **URL Opening**: When an entry is selected, users can click on the entry link to open the corresponding URL in their default web browser.

10. **Refresh Feeds**: The UI automatically refreshes the feeds at a specified interval to fetch the latest entries. The refresh interval can be configured in the settings.

### Usage

To use the RSS Feed Reader UI, follow these steps:

1. Ensure that the necessary dependencies are installed, including the `PySide6` library for creating the graphical interface.

2. Import the `RSSFeedReaderUI` class from the `RSSFeedReaderUI` module in your application.

3. Create an instance of the `RSSFeedReaderUI` class:
   ```python
   ui = RSSFeedReaderUI()
   ```

4. Show the UI window:
   ```python
   ui.show()
   ```

5. Interact with the RSS Feed Reader UI:
   - To add a new feed, enter the feed URL and category in the respective entry fields and click the "Add Feed" button.
   - To remove a feed, select the feed from the list and click the "Remove Feed" button.
   - To view the entries of a feed, click on the feed in the list. The entries will be displayed in the entry list section.
   - To view the details of an entry, click on the entry in the entry list. The entry details will be shown in the entry details section.
   - To remove an entry, select the entry from the entry list and click the "Remove Entry" button.
   - To open the URL of an entry, click on the entry link in the entry details section.

6. Customize the UI settings:
   - Modify the `config.ini` file to change the font style, colors, and refresh interval.
   - The changes will be reflected when the UI is restarted.

### Integration with RSS Feed Reader Module

The RSS Feed Reader UI is tightly integrated with the RSS Feed Reader module (`rss_feed_reader.py`). The UI utilizes the functionality provided by the module to perform various operations:

- When a new feed is added through the UI, it calls the `add_feed` method of the `RSSFeedReader` instance to add the feed to the underlying data structure.
- When a feed is removed through the UI, it calls the `remove_feed` method of the `RSSFeedReader` instance to remove the feed from the data structure.
- When a feed is selected in the UI, it calls the `get_feed_entries` method of the `RSSFeedReader` instance to retrieve the entries associated with that feed.
- When an entry is selected in the UI, it calls the `get_entry_details` method of the `RSSFeedReader` instance to retrieve the detailed information of that entry.
- When an entry is removed through the UI, it calls the `remove_entry` method of the `RSSFeedReader` instance to remove the entry from the feed.

The UI also utilizes the logging functionality of the RSS Feed Reader module to display log messages and errors.

### Customization

The RSS Feed Reader UI can be customized to match the desired theme and design. The following aspects of the UI can be modified:

- **Colors**: The color scheme of the UI can be adjusted by modifying the color constants in the `config.ini` file, such as `main_window_color`, `window_bg`, `font_color`, `button_bg`, etc.

- **Fonts**: The font style and size used in the UI can be changed by modifying the `font_family` and `font_size` variables in the `config.ini` file.

- **Refresh Interval**: The interval at which the feeds are automatically refreshed can be adjusted by modifying the `refresh_interval_mins` variable in the code.

- **Additional Features**: New features or functionalities can be added to the UI by extending the existing code and creating new widgets or interactions.

### Dependencies

The RSS Feed Reader UI relies on the following dependencies:

- `PySide6`: The Python binding for the Qt framework, used for creating the graphical user interface.
- `rss_feed_reader`: The RSS Feed Reader module that provides the core functionality for managing and retrieving RSS feeds and entries.

Make sure to have these dependencies installed and properly imported in your application.

### Troubleshooting

If you encounter any issues while using the RSS Feed Reader UI, consider the following:

- Check the console or log file for any error messages or exceptions that occurred during the execution of the UI.
- Ensure that the RSS Feed Reader module is properly integrated and functioning correctly.
- Verify that the necessary dependencies are installed and properly imported.
- Review the code for any syntax errors or logical inconsistencies.
- Check the `config.ini` file for any incorrect or missing configuration values.

For further assistance or to report any bugs, please refer to the project's issue tracker or contact the development team.

