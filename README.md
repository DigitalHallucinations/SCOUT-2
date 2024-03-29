# SCOUT: Scalable Cognitive Operations Unified Team

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python Version](https://img.shields.io/badge/Python-3.7%2B-brightgreen.svg)](https://www.python.org/)
[![Build Status](https://img.shields.io/badge/Build-In%20Progress-yellow.svg)](#)
[![Discord](https://img.shields.io/discord/1094426948949790770.svg?label=&logo=discord&logoColor=ffffff&color=7389D8&labelColor=6A7EC2)](https://discord.gg/wBWPP6udpK)
[![Instagram](https://img.shields.io/badge/Instagram-digital__hallucinations-E4405F.svg?logo=instagram&logoColor=ffffff)](https://www.instagram.com/digital_hallucinations/)

SCOUT is an innovative AI-powered personal assistant that offers intelligent, scalable, and responsive support for a diverse array of tasks. Utilizing state-of-the-art technologies like transformers, multi-agent systems, and cognitive operations, SCOUT aims to deliver a user experience that is both seamless and highly personalized.

![SCOUT Demo](assets/scout_demo.gif)

## Key Features

- **Intelligent Task Management**: SCOUT is adept at managing various tasks, such as scheduling, reminders, to-do lists, weather updates, news discovery, programming assistance, language translation, research support, and medical patient assistance. It leverages natural language processing and machine learning to comprehend and accurately respond to user requests.

- **Multi-LLM Provider Platform**: SCOUT supports leading model providers including OpenAI, Anthropic, Mistral, Google, and limited HuggingFace support.

- **Multi-TTS/STT Provider Platform**: SCOUT currently supports Google TTS and STT, with plans to integrate more providers.

- **Multi-Agent System**: SCOUT's future multi-agent system will enable efficient task coordination and distribution among multiple agents, providing parallel processing, fault tolerance, and scalability. Users can currently invoke interactive personas, each with a unique system prompt and toolset. All personas share a base toolset, including internet search via `serp_api` and current time/date retrieval. Future updates will include follow-up actions on search results, such as webpage scraping.

- **Responsive Communication**: Designed for interactive communication, SCOUT understands and generates natural language responses for a more human-like interaction. Google Cloud Speech provides TTS and STT capabilities, with additional providers to be added.

- **Cognitive Operations**: SCOUT's cognitive operations enhance user interaction by learning and storing user preferences and observations, creating a personalized profile that helps models adapt and improve.

![SCOUT Architecture](assets/scout_architecture.png)

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

2. Install VLC media player from [here](https://www.videolan.org/vlc/download-windows.html).

3. Install Microsoft Visual C++ 14.0 or greater via the "Microsoft C++ Build Tools" [here](https://visualstudio.microsoft.com/visual-cpp-build-tools/).

4. Install required Python dependencies:
   ```
   pip install -r requirements.txt
   ```

5. Configure `.env_template` with your API keys and rename it to `.env`.

6. Enter your Google Cloud credentials in `./assets/scout/GCC_template.json` and rename it to `GCC.json`.

7. Create a desktop shortcut for `SCOUT.bat` and update paths in `run_app.vbs` and `SCOUT.bat` to match your directory.

8. Launch SCOUT using the shortcut, sign up, and enjoy the assistant!

## Documentation

For comprehensive usage details, refer to the [documentation](https://github.com/DigitalHallucinations/SCOUT-2/wiki) (coming soon).

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

SCOUT is available under the [MIT License](LICENSE).

---

SCOUT is in active development; features may be incomplete. Your patience and support are appreciated as we work towards a versatile AI assistant.

For questions or issues, please contact me. Join us in advancing AI-powered personal assistance!