# SCOUT: Scalable Cognitive Operations Unified Team

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/DigitalHallucinations/scout/blob/main/LICENSE)
[![Python Version](https://img.shields.io/badge/Python-3.7%2B-brightgreen.svg)](https://www.python.org/)
[![Build Status](https://img.shields.io/badge/Build-In%20Progress-yellow.svg)](https://github.com/DigitalHallucinations/scout)

SCOUT is a cutting-edge AI-powered personal assistant designed to provide intelligent, scalable, and responsive support for a wide range of tasks. By leveraging advanced technologies such as transformers, multi-agent systems, and cognitive operations, SCOUT delivers a seamless and personalized user experience.

![SCOUT Demo](assets/scout_demo.gif)

## Key Features

- **Intelligent Task Management**: SCOUT is being developed to handle a variety of tasks, including scheduling appointments, setting reminders, managing to-do lists, checking the weather, finding the latest relevant news, programming in different languages, language translation, research assistance, patient medical assistance, and much more. It utilizes natural language processing and machine learning algorithms to understand user requests and provide accurate and relevant responses.

- **Multi-Agent System**: SCOUT will eventually employ a multi-agent system to efficiently coordinate and distribute tasks among multiple agents. This architecture enables parallel processing, fault tolerance, and scalability. Currently, users can manually invoke agents as interactive personas, each equipped with a unique system prompt and set of tools. All personas have access to a base set of tools, including internet search using the `serp_api` and the ability to retrieve the current time and date.

- **Responsive Communication**: SCOUT is designed to provide responsive and interactive communication with users. It can understand and generate natural language responses, making interactions feel more human-like. Text-to-speech (TTS) and speech-to-text (STT) capabilities are provided through Google Cloud Speech, with plans to integrate additional providers in the future.

- **Cognitive Operations**: SCOUT incorporates cognitive background operations to enhance its user interaction capabilities. It can learn and store information about the user's preferences and observations during interactions, building a user profile over time. This profile helps the underlying models adapt to new situations, improving performance and personalization.

![SCOUT Architecture](assets/scout_architecture.png)

## Roadmap

Here's a high-level roadmap of the features and improvements planned for SCOUT:

- [ ] Implement task management capabilities (scheduling, reminders, to-do lists)
- [ ] Integrate tool use/function calling for all AI providers
- [ ] Expand the range of supported tasks and domains
- [ ] Improve multi-agent coordination and task distribution
- [ ] Enhance user profile management and personalization
- [ ] Implement advanced NLP techniques for better understanding and generation
- [ ] Integrate additional TTS and STT providers
- [ ] Optimize performance and scalability
- [ ] Conduct extensive testing and bug fixing
- [ ] Prepare for a stable release version

## Getting Started

To get started with SCOUT, follow these steps:

1. Clone the SCOUT repository from GitHub:
   ```
   git clone https://github.com/DigitalHallucinations/scout.git
   ```

2. Install VLC media player from the official website: [https://www.videolan.org/vlc/download-windows.html](https://www.videolan.org/vlc/download-windows.html)

3. Install Microsoft Visual C++ 14.0 or greater. You can obtain it through the "Microsoft C++ Build Tools": [https://visualstudio.microsoft.com/visual-cpp-build-tools/](https://visualstudio.microsoft.com/visual-cpp-build-tools/)

4. Install the required Python dependencies:
   ```
   pip install -r requirements.txt
   ```

5. Open the `.env_template` file and add your API keys. Several API keys are required, which means setting up accounts and consoles for various services, including OpenAI, Google, Hugging Face, Anthropic, Mistral, NCBI, SerpAPI, and OpenWeatherMap. As more tools are built and providers are added, this list will grow. Save the file and rename it to `.env`.

6. Open `./assets/scout/GCC_template.json` and enter your Google Cloud credentials. Without this, Google TTS, STT, and Gmail integration will not work. You must first set up OAuth 2.0 and create a project in the Google Cloud Console. Add TTS, STT, and the Gmail API to the project. Rename the file to `./assets/scout/GCC.json`.

7. Open the SCOUT root folder and create a shortcut for `SCOUT.bat` on your desktop. Change the icon to the SCOUT icon located in the `assets` folder. Open `SCOUT.bat` and `run_app.vbs`. In `run_app.vbs`, change the line `WshShell.Run chr(34) & "C:\SCOUT\SCOUT.bat" & Chr(34), 0` and in `SCOUT.bat`, change `python C:\SCOUT\main.py` to match your current working directory.

8. Double-click the shortcut to start SCOUT. Sign up for an account and start using the assistant!

## Documentation

For detailed information on how to use SCOUT and its various features, refer to the [documentation](https://github.com/DigitalHallucinations/scout/wiki) (coming soon).

## Contributing

I welcome contributions from the community! If you'd like to contribute to SCOUT, please follow the guidelines outlined in the [contributing guide](https://github.com/DigitalHallucinations/scout/blob/main/CONTRIBUTING.md).

To contribute to SCOUT, follow these steps:

1. Fork the repository and create a new branch for your feature or bug fix.
2. Develop your changes, adhering to the project's coding conventions and style guide.
3. Write appropriate tests to ensure the stability and reliability of your changes.
4. Update the documentation, including the README and any relevant API or usage guides.
5. Submit a pull request, clearly describing the purpose and scope of your changes.

Again, I appreciate your contributions and will review your pull request as soon as possible. Thank you for helping to improve SCOUT!

## License

SCOUT is released under the [MIT License](https://github.com/DigitalHallucinations/scout/blob/main/LICENSE).

---

Please note that SCOUT is currently under active development, and many features may not be fully implemented yet. I appreciate your patience and support as "we" (the AI and myself) work towards delivering a powerful and versatile AI assistant.

If you have any questions or encounter any issues, please don't hesitate to reach out to me. I'm excited to have you join us on this journey of pushing the boundaries of AI-powered personal assistance!
