# Text to speech

API that converts text into lifelike speech with best-in-class latency & uses the most advanced AI audio model ever. Create voiceovers for your videos, audiobooks, or create AI chatbots for free.

POST/v1/text-to-speech/{voice_id}
​
# Introduction

    Our AI model produces the highest-quality AI voices in the industry. Here is an example of one of our default voices Grace in action:


    Our text to speech API allows you to convert text into audio in 29 languages and 1000s of voices. Integrate our realistic text to speech voices into your react app, use our Python library or our websockets guide to get started.

​
# API Features

    High-quality voices
    1000s of voices, in 29 languages, for every use-case, at 128kbps

    Ultra-low latency
    Achieve ~400ms audio generation times with our Turbo model.

    Contextual awareness
    Understands text nuances for appropriate intonation and resonance.


# Visit profile

    Next click on the eye icon on your profile to access your xi-api-key. Do not show your account to anyone else. If someone gains access to your xi-api-key he can use your account as he could if he knew your password.

    You can generate a new xi-api-key at any time by clicking on the spinning arrows next to the text field. This will invalidate your old xi-api-key.

​
# Audio generation

    Generate spoken audio from text with a simple request like the following Python example:


    import requests

    CHUNK_SIZE = 1024
    url = "https://api.elevenlabs.io/v1/text-to-speech/<voice-id>"

    headers = {
    "Accept": "audio/mpeg",
    "Content-Type": "application/json",
    "xi-api-key": "<xi-api-key>"
    }

    data = {
    "text": "Born and raised in the charming south, 
    I can add a touch of sweet southern hospitality 
    to your audiobooks and podcasts",
    "model_id": "eleven_monolingual_v1",
    "voice_settings": {
        "stability": 0.5,
        "similarity_boost": 0.5
    }
    }

    response = requests.post(url, json=data, headers=headers)
    with open('output.mp3', 'wb') as f:
        for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
            if chunk:
                f.write(chunk)
​
# Voices

    We offer 1000s of voices in 29 languages. Visit the Voice Lab to explore our pre-made voices or clone your own. Visit the Voices Library to see voices generated by ElevenLabs users. Below are some of our most popular voices:

    ​
    Dave

    ​
# Supported languages

    Currently supports the following languages:

    Chinese, Korean, Dutch, Turkish, Swedish, Indonesian, Filipino, Japanese, Ukrainian, Greek, Czech, Finnish, Romanian, Russian, Danish, Bulgarian, Malay, Slovak, Croatian, Classic Arabic, Tamil, English, Polish, German, Spanish, French, Italian, Hindi and Portuguese.

    To use them, simply provide the input text in the language of your choice.

# Integration Guides

    Headers
    xi-api-key
    string
    Your API key. This is required by most endpoints to access our API programatically. You can view your xi-api-key using the 'Profile' tab on the website.

# Path Parameters

    voice_id
    string
    required
    Voice ID to be used, you can use https://api.elevenlabs.io/v1/voices to list all the available voices.

# Query Parameters

    optimize_streaming_latency
    integer
    default: 0
    You can turn on latency optimizations at some cost of quality. The best possible final latency varies by model. Possible values: 0 - default mode (no latency optimizations) 1 - normal latency optimizations (about 50% of possible latency improvement of option 3) 2 - strong latency optimizations (about 75% of possible latency improvement of option 3) 3 - max latency optimizations 4 - max latency optimizations, but also with text normalizer turned off for even more latency savings (best latency, but can mispronounce eg numbers and dates).

    Defaults to 0.

# output_format

    string
    default: mp3_44100_128
    Output format of the generated audio. Must be one of: mp3_22050_32 - output format, mp3 with 22.05kHz sample rate at 32kbps. mp3_44100_32 - output format, mp3 with 44.1kHz sample rate at 32kbps. mp3_44100_64 - output format, mp3 with 44.1kHz sample rate at 64kbps. mp3_44100_96 - output format, mp3 with 44.1kHz sample rate at 96kbps. mp3_44100_128 - default output format, mp3 with 44.1kHz sample rate at 128kbps. mp3_44100_192 - output format, mp3 with 44.1kHz sample rate at 192kbps. Requires you to be subscribed to Creator tier or above. pcm_16000 - PCM format (S16LE) with 16kHz sample rate. pcm_22050 - PCM format (S16LE) with 22.05kHz sample rate. pcm_24000 - PCM format (S16LE) with 24kHz sample rate. pcm_44100 - PCM format (S16LE) with 44.1kHz sample rate. Requires you to be subscribed to Pro tier or above. ulaw_8000 - μ-law format (sometimes written mu-law, often approximated as u-law) with 8kHz sample rate. Note that this format is commonly used for Twilio audio inputs.

    Body
    application/json
    model_id
    string
    default: eleven_monolingual_v1
    Identifier of the model that will be used, you can query them using GET /v1/models. The model needs to have support for text to speech, you can check this using the can_do_text_to_speech property.

# pronunciation_dictionary_locators

    object[]
    A list of pronunciation dictionary locators (id, version_id) to be applied to the text. They will be applied in order. You may have up to 3 locators per request


    Show child attributes

    text
    string
    required
    The text that will get converted into speech.

# voice_settings

    object
    Voice settings overriding stored setttings for the given voice. They are applied only on the given request.


    Show child attributes

    Response
    200 - audio/mpeg
    The response is of type file.