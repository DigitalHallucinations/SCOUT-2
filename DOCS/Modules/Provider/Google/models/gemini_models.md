Gemini models 

bookmark_border
Gemini is a family of generative AI models that lets developers generate content and solve problems. These models are designed and trained to handle both text and images as input. This guide provides information about each model variant to help you decide which is the best fit for your use case.

Model sizes
The following table shows the available sizes and what they mean relative to each other.

Model size	Description	Services
Gemini Pro	A model size that balances capability and efficiency.	
text
chat
Model versions
Gemini models are available in either preview or stable versions. In your code, you can use one of the following model name formats to specify which model and version you want to use.

Latest: Points to the cutting-edge version of the model for a specified generation and variation. The underlying model is updated regularly and might be a preview version. Only exploratory testing apps and prototypes should use this alias.

To specify the latest version, use the following pattern: <model>-<generation>-<variation>-latest. For example, gemini-1.0-pro-latest.

Latest stable: Points to the most recent stable version released for the specified model generation and variation.

To specify the latest stable version, use the following pattern: <model>-<generation>-<variation>. For example, gemini-1.0-pro.

Stable: Points to a specific stable model. Stable models don't change. Most production apps should use a specific stable model.

To specify a stable version, use the following pattern: <model>-<generation>-<variation>-<version>. For example, gemini-1.0-pro-001.

Note: gemini-pro is an alias for gemini-1.0-pro.
For models that have a stable version, see the "Model names" row for the model in Model variations.

Model variations
The Gemini API offers different models optimized for specific use cases. The following table describes attributes of each.

Note: For Gemini models, a token is equivalent to about 4 characters. 100 tokens are about 60-80 English words.
Variation	Attribute	Description
Gemini Pro	Model last updated	February 2024
Model code	models/gemini-pro
Model capabilities	
Input: text
Output: text
Generates text.
Can handle multi-turn conversational format.
Can handle zero, one, and few-shot tasks.
Supported generation methods	generateContent
Input token limit	30720
Output token limit	2048
Model safety	Automatically applied safety settings which are adjustable by developers. See the safety settings topic for details.
Rate limit	60 requests per minute [1]
Model names	
Latest version: gemini-1.0-pro-latest
Latest stable version: gemini-1.0-pro
Stable versions:
gemini-1.0-pro-001
Gemini Pro Vision	Model last updated	December 2023
Model code	models/gemini-pro-vision
Model capabilities	
Input: text and images
Output: text
Can take multimodal inputs, text and image.
Can handle zero, one, and few-shot tasks.
Supported generation methods	generateContent
Input token limit	12288
Output token limit	4096
Model safety	Automatically applied safety settings which are adjustable by developers. See the safety settings topic for details.
Rate limit	60 requests per minute [1]
Embedding	Model last updated	December 2023
Model code	models/embedding-001
Model capabilities	
Input: text
Output: text
Generates text embeddings for the input text.
Optimized for creating embeddings for text of up to 2048 tokens.
Supported generation methods	embedContent
Model safety	No adjustable safety settings.
Rate limit	1500 requests per minute [1]
AQA	Model last updated	December 2023
Model code	models/aqa
Model capabilities	
Input: text
Output: text
Model that performs Attributed Question Answering.
Model trained to return answers to questions that are grounded in provided sources, along with estimating answerable probability.
Supported generation methods	generateAnswer
Supported languages	English
Input token limit	7168
Output token limit	1024
Model safety	Automatically applied safety settings which are adjustable by developers. See the safety settings topic for details.
Rate limit	60 requests per minute [1]
See the examples to explore the capabilities of these model variations.

Model metadata
Use the ModelService API to get additional metadata about the latest models such as input and output token limits. The following table displays the metadata for the Gemini Pro model variant.

Attribute	Value
Display name	Gemini Pro
Model code	models/gemini-pro
Description	Model targeted for text generation
Supported generation methods	generateContent
Temperature	0.9
top_p	1
top_k	1
Model attributes
The following table describes the attributes of the Gemini models which are common to all model variations.

Note: The configurable parameters apply only to the text and chat model variations, but not embeddings.
Attribute	Description
Training data	Gemini's knowledge cutoff is early 2023. Knowledge about events after that time is limited.
Supported languages	See available languages
Configurable model parameters	
Top p
Top k
Temperature
Stop sequence
Max output length
Number of response candidates
[1] Specified rate limits are not guaranteed and actual capacity may vary.

See the model parameters section of the Intro to LLMs guide for information about each of these parameters.

