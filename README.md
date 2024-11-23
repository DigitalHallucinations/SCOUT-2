# SCOUT: Scalable Cognitive Operations Unified Team

[![License](https://img.shields.io/badge/License-Custom-blue.svg)](LICENSE)
[![Python Version](https://img.shields.io/badge/Python-3.7%2B-brightgreen.svg)](https://www.python.org/)
[![Build Status](https://img.shields.io/badge/Build-In%20Progress-yellow.svg)](#)
[![Discord](https://img.shields.io/discord/1094426948949790770.svg?label=&logo=discord&logoColor=ffffff&color=7389D8&labelColor=6A7EC2)](https://discord.gg/wBWPP6udpK)
[![Instagram](https://img.shields.io/badge/Instagram-digital__hallucinations-E4405F.svg?logo=instagram&logoColor=ffffff)](https://www.instagram.com/digital_hallucinations/)

SCOUT is an AI-powered personal assistant that aims to empower people through intelligent, adaptive, and personalized support. Built on a foundation of open-source software and community collaboration, SCOUT offers a transparent and user-controlled approach to AI assistance. It serves as a platform for innovation and experimentation, enabling users to push the boundaries of artificial intelligence across various domains.

SCOUT is an innovative AI-powered personal assistant that offers intelligent, scalable, and responsive support for a diverse array of tasks. Utilizing state-of-the-art technologies like transformers, multi-agent systems, and cognitive operations, SCOUT aims to deliver a user experience that is both seamless and highly personalized.

## Vision

At its heart, SCOUT is about empowering people through artificial intelligence. It's an AI-powered personal assistant that goes beyond just answering questions or performing simple tasks. SCOUT is designed to be a true partner in every sense of the word - an intelligent, adaptive, and personalized system that can help users navigate the complexities of the modern world.

What sets SCOUT apart is its commitment to openness, transparency, and user control. Unlike other AI assistants that operate as black boxes, with opaque algorithms and proprietary codebases, SCOUT is built on a foundation of open-source software and community collaboration. This means that users can see exactly how the system works, contribute to its development, and even customize it to suit their own unique needs and preferences.

SCOUT isn't just a tool for individuals - it's a platform for innovation and experimentation. By providing a flexible, extensible framework for AI development, SCOUT enables researchers, developers, and enthusiasts from all walks of life to push the boundaries of what's possible with artificial intelligence. Whether you're interested in natural language processing, computer vision, robotics, or any other field, SCOUT gives you the tools and the community support you need to turn your ideas into reality.

SCOUT is about something much bigger than just technology. It's about the future of humanity, and the role that artificial intelligence will play in shaping that future. By putting the power of AI into the hands of the people, and by fostering a culture of openness, collaboration, and innovation, SCOUT is laying the groundwork for a world in which humans and machines can work together in harmony - not as master and servant, but as true partners in the quest for knowledge, understanding, and progress.

## Key Features

- **Intelligent Task Management**: SCOUT is adept at managing various tasks, such as scheduling, reminders, to-do lists, weather updates, news discovery, programming assistance, language translation, research support, and medical patient assistance. It leverages natural language processing and machine learning to comprehend and accurately respond to user requests.

- **Multi-LLM Provider Platform**: SCOUT supports leading model providers including OpenAI, Anthropic, Mistral, Google, and limited HuggingFace support.

- **Multi-TTS/STT Provider Platform**: SCOUT currently supports Google TTS and STT, with plans to integrate more providers.

- **Multi-Agent System**: SCOUT's future multi-agent system will enable efficient task coordination and distribution among multiple agents, providing parallel processing, fault tolerance, and scalability. Users can currently invoke interactive personas, each with a unique system prompt and toolset. All personas share a base toolset, including internet search via `serp_api` and current time/date retrieval. Future updates will include follow-up actions on search results, such as webpage scraping.

- **Responsive Communication**: Designed for interactive communication, SCOUT understands and generates natural language responses for a more human-like interaction. Google Cloud Speech provides TTS and STT capabilities, with additional providers to be added.

- **Cognitive Operations**: SCOUT's cognitive operations enhance user interaction by learning and storing user preferences and observations, creating a personalized profile that helps models adapt and improve.

## SCOUT Architecture

### 1. **Main Application Entry Point (`main.py`)**
- **Initialization**: Sets up logging, custom exception handling, and starts the application.
- **Asynchronous Context Management**: Uses `asynccontextmanager` to manage background tasks.
- **Dynamic Module Loading**: Loads different modules based on the current LLM (Large Language Model) and background provider.
- **Application Shutdown**: Handles cleanup and shutdown tasks.

### 2. **Graphical User Interface (GUI)**
- **Main Window**: Initializes the main application window, manages user sessions, and sets up the custom title bar.
- **Chat Component**: Manages the chat interface, including message entry, chat log, and persona selection.
- **Sidebar**: Provides navigation and tool selection options.
- **Tool Control Bar**: Manages quick access to various tools like VoIP, RSS feed, browser, and calendar.
- **Status Bar**: Displays current provider, model, and user information.
- **Appearance Settings**: Manages the visual settings of the application, including font styles, colors, and sizes.

### 3. **Background Services**
- **Cognitive Background Services**: Manages background tasks related to conversation processing, such as generating conversation names and updating user profiles.

### 4. **Conversation Management**
- **Conversation Manager**: Handles database operations related to conversations, messages, function calls, and responses. Uses SQLite for data storage.

### 5. **Provider Management**
- **Provider Manager**: Manages different LLM providers, background providers, and speech providers. Switches between providers based on the current configuration.
- **Model Manager**: Manages the current model and its configurations, such as allowed models and maximum tokens.

### 6. **Tool Management**
- **Tool Manager**: Loads functions from JSON and maps them to the current persona. Handles function calls and integrates them into the conversation flow.

### 7. **User Data Management**
- **User Data Manager**: Manages user profiles, EMRs (Electronic Medical Records), and system information. Formats and retrieves user data for persona personalization.

### 8. **OpenAI API Integration**
- **OpenAI API**: Handles communication with the OpenAI API for generating conversations and cognitive background services.

### 9. **Logging**
- **Logger Setup**: Configures logging for different modules to track application behavior and errors.

### 10. **Personas**
- **Persona Manager**: Manages different personas, personalizes them based on user data, and updates the current persona.

### 11. **Function and Tool Definitions**
- **Function Definitions**: JSON files defining available functions for each persona.
- **Function Maps**: Python files mapping function names to their implementations.

## Roadmap

Our roadmap outlines the upcoming features and improvements for SCOUT:

- [ ] Task management implementation (scheduling, reminders, to-do lists)
- [ ] Integration of tool use/function calling for all AI providers
- [ ] Expansion of supported tasks and domains
- [ ] Multi-agent coordination and task distribution enhancements
- [ ] User profile management and personalization improvements
- [ ] Advanced NLP techniques for better understanding and generation
- [ ] Additional TTS and STT provider integrations
- [ ] Performance and scalability optimizations
- [ ] Extensive testing and bug fixing
- [ ] Stable release version preparation

## Getting Started

To begin using SCOUT, follow these steps:

1. Clone the repository:
   ```
   git clone https://github.com/DigitalHallucinations/SCOUT-2.git
   ```

2. Install Microsoft Visual C++ 14.0 or greater via the "Microsoft C++ Build Tools" [here](https://visualstudio.microsoft.com/visual-cpp-build-tools/).

3. Install required Python dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Configure `.env_template` with your API keys and rename it to `.env`.

5. Enter your Google Cloud credentials in `./assets/scout/GCC_template.json` and rename it to `GCC.json`.

6. Create a desktop shortcut for `SCOUT.bat` and update paths in `run_app.vbs` and `SCOUT.bat` to match your directory. Change the icon to 'assets/SCOUT/SCOUT.ico'. Make sure to set the shortcut to run as administrator. You must give the shortcut administrative priviledges as several tools require it.

7. Launch SCOUT using the shortcut, sign up, and enjoy the assistant!

## Documentation

For comprehensive usage details, refer to the [documentation](DOCS/SCOUT_overview.md).

## API Keys Configuration

To use SCOUT, you will need to obtain several API keys and configure them in the `.env` file. Here's where you can find the required API keys:

1. **OpenAI API Key**:
   - Sign up for an OpenAI account at [openai.com](https://openai.com/).
   - Generate an API key by going to the [API Keys](https://platform.openai.com/account/api-keys) section in your OpenAI account.
   - Copy the API key and paste it in the `OPENAI_API_KEY` field in the `.env` file.

2. **Google Cloud Credentials**:
   _ This is not the same as the Google AI Studio.
   - Go to the [Google Cloud Console](https://console.cloud.google.com/) and create a new project.
   - Enable the necessary APIs, such as:
     - Cloud Speech-to-Text
     - Cloud Text-to-Speech
     - Cloud Natural Language API
   - Create a service account and download the JSON credentials file.
   - In the `./assets/SCOUT/` directory, there is a file called `GCC_template.json`. Open this file and fill in the following fields with the values from the downloaded JSON credentials file:
     - `"type"`
     - `"project_id"`
     - `"private_key_id"`
     - `"private_key"`
     - `"client_email"`
     - `"client_id"`
     - `"client_x509_cert_url"`
   - Rename the filled-out `GCC_template.json` file to `GCC.json`.
   - Update the `GOOGLE_APPLICATION_CREDENTIALS` field in the `.env` file to point to the `GCC.json` file.
   - In the Google Cloud Console, navigate to the [API Library](https://console.cloud.google.com/apis/library) and enable the following APIs for your project:
     - Cloud Speech-to-Text API
     - Cloud Text-to-Speech API
     - Cloud Natural Language API
     
3. **SerpAPI Key**:
   - Sign up for a SerpAPI account at [serpapi.com](https://serpapi.com/).
   - Generate an API key in the [API Keys](https://serpapi.com/dashboard) section of your SerpAPI account.
   - Copy the API key and paste it in the `SERPAPI_KEY` field in the `.env` file.

4. **NCBI API Key**:
   - Only neccessary for medical personas
   - Sign up for an NCBI account at [ncbi.nlm.nih.gov](https://www.ncbi.nlm.nih.gov/).
   - Generate an API key in the [API Key Management](https://www.ncbi.nlm.nih.gov/account/settings/) section of your NCBI account.
   - Copy the API key and paste it in the `NCBI_API_KEY` field in the `.env` file.

5. **OpenWeatherMap API Key**:
   - Sign up for an OpenWeatherMap account at [openweathermap.org](https://openweathermap.org/).
   - Generate an API key in the [API Keys](https://home.openweathermap.org/api_keys) section of your OpenWeatherMap account.
   - Copy the API key and paste it in the `OPENWEATHERMAP_API_KEY` field in the `.env` file.

6. **NewsAPI.org API Key**:
   - Sign up for a NewsAPI.org account at [newsapi.org](https://newsapi.org/).
   - Generate an API key in the [API Keys](https://newsapi.org/account) section of your NewsAPI.org account.
   - Copy the API key and paste it in the `NEWSAPI_API_KEY` field in the `.env` file.

7. **Google AI STUDIO API Key**:
   - This is separate from the Google Cloud Credentials.
   - Navigate to the [API Keys](https://aistudio.google.com/app/apikey) section in the Google Cloud Console.
   - Generate a new API key and copy it.
   - Paste the API key in the `GOOGLE_API_KEY` field in the `.env` file.

8. **Hugging Face API Key**:
   - Sign up for a Hugging Face account at [huggingface.co](https://huggingface.co/).
   - Generate an API token in the [Settings](https://huggingface.co/settings/tokens) section of your Hugging Face account.
   - Copy the API token and paste it in the `HF_API_TOKEN` field in the `.env` file.

9. **Mistral API Key**:
   - Sign up for a Mistral account at [mistral.ai](https://mistral.ai/).
   - Generate an API key in the [API Keys](https://mistral.ai/dashboard/api-keys) section of your Mistral account.
   - Copy the API key and paste it in the `Mistral_API_KEY` field in the `.env` file.

10. **Anthropic API Key**:
    - Sign up for an Anthropic account at [anthropic.com](https://www.anthropic.com/).
    - Generate an API key in the [API Keys](https://console.anthropic.com/account/api-keys) section of your Anthropic account.
    - Copy the API key and paste it in the `Anthropic_API_KEY` field in the `.env` file.

After configuring all the necessary API keys, save the `.env` file and proceed with the rest of the setup instructions.

## Contributing

Contributions are welcome! Please adhere to the [contributing guidelines](CONTRIBUTING.md).

To contribute:

1. Fork the repo and create a feature or bug-fix branch.
2. Develop your changes with adherence to coding conventions and style.
3. Write tests for stability and reliability.
4. Update documentation, including README and API/usage guides.
5. Submit a pull request with a clear description of your changes.

Your contributions are valued and will be reviewed promptly.

## License

SCOUT is available under a custom license with the following terms:

- **Non-Commercial Use**: SCOUT can only be used for personal and research purposes unless a commercial license is obtained from Digital Hallucinations.
- **Modification**: Modifications to the SCOUT codebase are encouraged, but the modified code must be submitted as a pull request and accepted by the SCOUT development team before it can be used.
- **Custom Deployments**: Custom deployments and commercial use of SCOUT can be arranged by obtaining a license from Digital Hallucinations.
- **Personal and Research Use**: SCOUT can be used for personal and research purposes under the following restrictions:
  - The SCOUT application and its components cannot be redistributed or shared publicly.
  - The SCOUT application and its components cannot be used to create derivative works or commercial products without prior approval from Digital Hallucinations.
  - The SCOUT application and its components must be used in accordance with the project's documentation and guidelines.

The full license details and terms will be provided in the project's `LICENSE` file. Users interested in commercial use or custom deployments should contact the Digital Hallucinations team to discuss licensing options.


---

SCOUT is in active development; features may be incomplete. Your patience and support are appreciated as we work towards a versatile AI assistant.

For questions or issues, please contact me. Join us in advancing AI-powered personal assistance!