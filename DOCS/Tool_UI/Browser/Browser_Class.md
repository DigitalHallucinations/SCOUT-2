# Browser_Class.md

1. Browser Class (browser.py)
------------------------------

The Browser class is the main component of the browser implementation. It's a QMainWindow subclass that provides the core functionality for the web browser.

Key Features:
- Tabbed browsing interface
- Navigation controls (back, forward, reload, home)
- URL bar for manual navigation
- Bookmarks management
- History tracking
- Dark mode toggle
- Download management

Main Components:
a) Initialization:
   - Sets up the main window layout
   - Creates toolbars for navigation and bookmarks
   - Initializes the tab widget for multiple pages

b) Navigation Methods:
   - browser_back(): Navigate to the previous page
   - browser_forward(): Navigate to the next page
   - browser_reload(): Reload the current page
   - browser_home(): Navigate to the home page
   - navigate_to_url(): Load a URL entered in the address bar

c) Tab Management:
   - add_new_tab(): Create a new browser tab
   - close_tab(): Close the current tab

d) Bookmarks:
   - add_bookmark(): Add the current page to bookmarks
   - load_bookmarks(): Load saved bookmarks
   - show_bookmark_context_menu(): Manage bookmark options

e) History:
   - load_history(): Load browsing history
   - toggle_history_frame(): Show/hide the history panel

f) Downloads:
   - on_download_requested(): Handle file download requests

g) Context Menu:
   - show_context_menu(): Display context menu for additional options

2. Browser Database (browser_db.py)
-----------------------------------

The BrowserDatabase class manages the persistent storage of browser data using SQLite.

Main Tables:
- history: Stores browsing history
- bookmarks: Stores user bookmarks
- cookies: Stores website cookies

Key Methods:
- create_database(): Initialize the database and create tables
- add_history(): Add a new history entry
- get_all_history(): Retrieve all history entries
- add_cookie(): Store a new cookie
- get_all_cookies(): Retrieve all stored cookies
- add_bookmark(): Add a new bookmark
- get_all_bookmarks(): Retrieve all bookmarks
- update_bookmark_icon(): Update a bookmark's icon
- delete_bookmark(): Remove a bookmark

3. Content Security Policy (csp.py)
-----------------------------------

This module implements a Content Security Policy (CSP) for the browser using Flask.

Key Features:
- Defines CSP directives to enhance security
- Applies CSP headers to all responses

CSP Directives:
- default-src: Restrict default sources to 'self'
- script-src: Allow inline and eval for scripts
- style-src: Allow inline styles
- img-src: Allow images from 'self' and data URIs
- connect-src: Restrict connections to 'self'
- object-src: Disallow object sources
- frame-ancestors: Restrict framing to 'self'

4. Web Engine Page (web_engine_page.py)
---------------------------------------

The MyWebEnginePage class extends QWebEnginePage to provide custom behavior for web page rendering and JavaScript handling.

Key Features:
- Custom certificate error handling
- Detailed JavaScript console message logging
- Error handling for various scenarios (CSP violations, undefined properties, etc.)

Main Methods:
- certificateError(): Handle SSL certificate errors
- javaScriptConsoleMessage(): Process and log JavaScript console messages

Additional Checks:
- CSP errors
- Undefined property access
- Permutive initialization errors
- AbortErrors
- Loadable state errors
- Event parsing errors
- Fetch errors

This browser implementation provides a comprehensive set of features including secure browsing, history and bookmark management, and detailed error logging. The modular structure allows for easy maintenance and extension of functionality.