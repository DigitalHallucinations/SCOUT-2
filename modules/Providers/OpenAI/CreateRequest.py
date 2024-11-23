# modules/Providers/OpenAI/create_request_body.py

import logging

logger = logging.getLogger('create_request_body.py')

def create_request_body(model, current_persona, messages, temperature_var, top_p_var, max_tokens, functions=None):
    logger.info("Creating request body.")
    logger.info(f"Model: {model}")
    logger.info(f"Max Tokens: {max_tokens}")
    logger.info(f"Temperature: {temperature_var}")
    logger.info(f"Messages: {messages}")

    data = {
        "model": model,
        "messages": [{"role": "system", "content": current_persona["content"]}] + messages,
        "temperature": temperature_var,
        "max_tokens": max_tokens,
        "top_p": top_p_var
    }
    if functions:
        data["functions"] = functions
        data["function_call"] = "auto"

    logger.info("Request body created.")
    return data