# SCOUT API Reference

Version: 1.0.0
Last Updated: 2023-06-29

## Table of Contents
1. [ChatComponent Module](#chatcomponent-module)
2. [ProviderManager Module](#providermanager-module)
3. [PersonaManager Module](#personamanager-module)
4. [ToolIntegration Module](#toolintegration-module)
5. [UserManagement Module](#usermanagement-module)
6. [DataStorage Module](#datastorage-module)
7. [ConfigurationManager Module](#configurationmanager-module)

---

## ProviderManager Module

The ProviderManager module handles the integration and switching between different AI providers.

### Class: ProviderManager

#### Constructor

```
def __init__(self, config_path: str)
Creates a new instance of the ProviderManager.
Parameters:

config_path (str): Path to the configuration file containing provider settings.

Returns:

None

Raises:

FileNotFoundError: If the configuration file is not found.
JSONDecodeError: If the configuration file is not valid JSON.

Method: switch_provider
def switch_provider(self, provider_name: str) -> bool
Switches the current AI provider.
Parameters:

provider_name (str): The name of the provider to switch to.

Returns:

bool: True if the switch was successful, False otherwise.

Raises:

ValueError: If the specified provider is not supported.

Example usage:
success = provider_manager.switch_provider("OpenAI")
if success:
    print("Switched to OpenAI provider")
else:
    print("Failed to switch provider")
Method: get_current_provider
def get_current_provider(self) -> str
Gets the name of the current AI provider.
Parameters:

None

Returns:

str: The name of the current provider.

Example usage:
current_provider = provider_manager.get_current_provider()
print(f"Current provider: {current_provider}")
Method: send_request
async def send_request(self, prompt: str, **kwargs) -> str
Sends a request to the current AI provider.
Parameters:

prompt (str): The input prompt for the AI.
**kwargs: Additional parameters specific to the current provider.

Returns:

str: The response from the AI provider.

Raises:

ConnectionError: If unable to connect to the AI provider.
TimeoutError: If the AI provider takes too long to respond.

Example usage:
response = await provider_manager.send_request("Tell me a joke", max_tokens=100)
print(f"AI response: {response}")
Constants

SUPPORTED_PROVIDERS: A list of supported AI provider names.


## PersonaManager Module

The PersonaManager module handles the creation, modification, and switching of AI personas.
Class: PersonaManager
Constructor
def __init__(self, persona_directory: str)
Creates a new instance of the PersonaManager.
Parameters:

persona_directory (str): Path to the directory containing persona configurations.

Returns:

None

Raises:

NotADirectoryError: If the specified path is not a directory.

Method: load_persona
def load_persona(self, persona_name: str) -> dict
Loads a persona configuration.
Parameters:

persona_name (str): The name of the persona to load.

Returns:

dict: The persona configuration.

Raises:

FileNotFoundError: If the persona configuration file is not found.

Example usage:
code_genius_persona = persona_manager.load_persona("CodeGenius")
print(f"Loaded persona: {code_genius_persona['name']}")
Method: create_persona
def create_persona(self, persona_config: dict) -> bool
Creates a new persona.
Parameters:

persona_config (dict): The configuration for the new persona.

Returns:

bool: True if the persona was created successfully, False otherwise.

Raises:

ValueError: If the persona configuration is invalid.

Example usage:
new_persona = {
    "name": "MathWizard",
    "description": "Expert in mathematics and problem-solving",
    "traits": ["analytical", "precise", "patient"]
}
success = persona_manager.create_persona(new_persona)
if success:
    print("New persona created successfully")
Method: switch_persona
def switch_persona(self, persona_name: str) -> dict
Switches the current persona.
Parameters:

persona_name (str): The name of the persona to switch to.

Returns:

dict: The configuration of the new active persona.

Raises:

ValueError: If the specified persona does not exist.

Example usage:
active_persona = persona_manager.switch_persona("MathWizard")
print(f"Switched to persona: {active_persona['name']}")

## ToolIntegration Module

The ToolIntegration module manages the integration of various tools within the SCOUT application.
Class: ToolIntegration
Constructor
def __init__(self)
Creates a new instance of the ToolIntegration.
Parameters:

None

Returns:

None

Method: register_tool
def register_tool(self, tool_name: str, tool_instance: object) -> bool
Registers a new tool with the integration system.
Parameters:

tool_name (str): The name of the tool to register.
tool_instance (object): An instance of the tool class.

Returns:

bool: True if the tool was registered successfully, False otherwise.

Raises:

ValueError: If a tool with the same name is already registered.

Example usage:
calculator_tool = Calculator()
success = tool_integration.register_tool("calculator", calculator_tool)
if success:
    print("Calculator tool registered successfully")
Method: get_tool
def get_tool(self, tool_name: str) -> object
Retrieves a registered tool.
Parameters:

tool_name (str): The name of the tool to retrieve.

Returns:

object: The instance of the requested tool.

Raises:

KeyError: If the requested tool is not registered.

Example usage:
try:
    calculator = tool_integration.get_tool("calculator")
    result = calculator.add(5, 3)
    print(f"5 + 3 = {result}")
except KeyError:
    print("Calculator tool not found")
Method: execute_tool
async def execute_tool(self, tool_name: str, method_name: str, *args, **kwargs) -> Any
Executes a method on a registered tool.
Parameters:

tool_name (str): The name of the tool to use.
method_name (str): The name of the method to execute on the tool.
*args: Positional arguments to pass to the method.
**kwargs: Keyword arguments to pass to the method.

Returns:

Any: The result of the tool method execution.

Raises:

KeyError: If the requested tool is not registered.
AttributeError: If the requested method does not exist on the tool.

Example usage:
try:
    result = await tool_integration.execute_tool("calculator", "add", 10, 20)
    print(f"10 + 20 = {result}")
except KeyError:
    print("Calculator tool not found")
except AttributeError:
    print("Add method not found on calculator")

## UserManagement Module

The UserManagement module handles user authentication, registration, and profile management.
Class: UserManager
Constructor
def __init__(self, database_path: str)
Creates a new instance of the UserManager.
Parameters:

database_path (str): Path to the user database file.

Returns:

None

Raises:

FileNotFoundError: If the database file is not found.

Method: register_user
def register_user(self, username: str, password: str, email: str) -> bool
Registers a new user.
Parameters:

username (str): The desired username for the new user.
password (str): The password for the new user.
email (str): The email address of the new user.

Returns:

bool: True if the user was registered successfully, False otherwise.

Raises:

ValueError: If the username already exists or if the password is too weak.

Example usage:
success = user_manager.register_user("newuser", "securepassword123", "newuser@example.com")
if success:
    print("User registered successfully")
else:
    print("Failed to register user")
Method: authenticate_user
def authenticate_user(self, username: str, password: str) -> bool
Authenticates a user.
Parameters:

username (str): The username of the user to authenticate.
password (str): The password to check.

Returns:

bool: True if authentication is successful, False otherwise.

Example usage:
if user_manager.authenticate_user("existinguser", "userpassword"):
    print("Authentication successful")
else:
    print("Authentication failed")
Method: get_user_profile
def get_user_profile(self, username: str) -> dict
Retrieves the profile of a user.
Parameters:

username (str): The username of the user whose profile to retrieve.

Returns:

dict: The user's profile information.

Raises:

KeyError: If the user does not exist.

Example usage:
try:
    profile = user_manager.get_user_profile("existinguser")
    print(f"User email: {profile['email']}")
except KeyError:
    print("User not found")

## DataStorage Module

The DataStorage module handles data persistence and retrieval for the SCOUT application.
Class: DataManager
Constructor
def __init__(self, database_url: str)
Creates a new instance of the DataManager.
Parameters:

database_url (str): URL of the database to connect to.

Returns:

None

Raises:

ConnectionError: If unable to connect to the database.

Method: save_data
async def save_data(self, collection: str, data: dict) -> str
Saves data to the specified collection.
Parameters:

collection (str): The name of the collection to save data to.
data (dict): The data to save.

Returns:

str: The ID of the saved data.

Raises:

ValueError: If the data is not in the correct format.

Example usage:
chat_data = {
    "user": "example_user",
    "message": "Hello, AI!",
    "timestamp": "2023-06-29T10:00:00Z"
}
data_id = await data_manager.save_data("chat_history", chat_data)
print(f"Saved chat data with ID: {data_id}")
Method: get_data
async def get_data(self, collection: str, query: dict) -> list
Retrieves data from the specified collection based on the query.
Parameters:

collection (str): The name of the collection to retrieve data from.
query (dict): The query to filter the data.

Returns:

list: A list of matching data items.

Example usage:
query = {"user": "example_user"}
chat_history = await data_manager.get_data("chat_history", query)
for chat in chat_history:
    print(f"Message: {chat['message']}, Time: {chat['timestamp']}")
Method: update_data
async def update_data(self, collection: str, data_id: str, update_data: dict) -> bool
Updates existing data in the specified collection.
Parameters:

collection (str): The name of the collection containing the data.
data_id (str): The ID of the data to update.
update_data (dict): The new data to apply.

Returns:

bool: True if the update was successful, False otherwise.

Raises:

KeyError: If the specified data_id does not exist.

Example usage:
update = {"message": "Updated message"}
success = await data_manager.update_data("chat_history", "abc123", update)
if success:
    print("Chat message updated successfully")
else:
    print("Failed to update chat message")

## ConfigurationManager Module

The ConfigurationManager module handles application-wide and user-specific settings.
Class: ConfigManager
Constructor
def __init__(self, config_file: str)
Creates a new instance of the ConfigManager.
Parameters:

config_file (str): Path to the configuration file.

Returns:

None

Raises:

FileNotFoundError: If the configuration file is not found.

Method: get_setting
def get_setting(self, setting_name: str, default_value: Any = None) -> Any
Retrieves the value of a setting.
Parameters:

setting_name (str): The name of the setting to retrieve.
default_value (Any, optional): The default value to return if the setting is not found.

Returns:

Any: The value of the setting, or the default value if not found.

Example usage:
theme = config_manager.get_setting("app_theme", default_value="light")
print(f"Current theme: {theme}")
Method: set_setting
def set_setting(self, setting_name: str, value: Any) -> bool
Sets the value of a setting.
Parameters:

setting_name (str): The name of the setting to set.
value (Any): The value to assign to the setting.

Returns:

bool: True if the setting was set successfully, False otherwise.

Example usage:
success = config_manager.set_setting("app_theme", "dark")
if success:
    print("Theme updated successfully")
else:
    print("Failed to update theme")
Method: save_config
def save_config(self) -> bool
Saves the current configuration to the file.
Parameters:

None

Returns:

bool: True if the configuration was saved successfully, False otherwise.

Example usage:
if config_manager.save_config():
    print("Configuration saved successfully")
else:
    print("Failed to save configuration")

