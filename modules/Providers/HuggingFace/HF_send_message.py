# gui\HuggingFace\HF_send_message.py

import time
import asyncio
import logging


logger = logging.getLogger()

async def send_message(chat_log, user, message_entry, system_name, system_name_tag, typing_indicator_index, generate_response, current_persona, temperature_var, top_p_var, top_k_var):
    logger.info("send_message called")
    print("send_message called")
    message = message_entry.get("1.0", "end-1c").strip()
    if not message:
        logger.warning("No message provided in send_message")
        print("Warning: No message provided in send_message")
        return
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())  
    chat_log.configure(state="normal")
    chat_log.insert("end", f"{timestamp}\n", "timestamp")
    chat_log.insert("end", f"{user}: ", "You")   
    chat_log.insert("end", message + "\n")
    chat_log.configure(state="disabled")
    chat_log.yview("end")
    message_entry.delete("1.0", "end")
        
    asyncio.create_task(process_message(chat_log, system_name, system_name_tag, typing_indicator_index, generate_response, message, current_persona, temperature_var, top_p_var, top_k_var))

async def process_message(chat_log, system_name, system_name_tag, typing_indicator_index, generate_response, message, current_persona, temperature_var, top_p_var, top_k_var):
    logger.info("process_message called with message: %s", message)
    print("process_message called with message:", message)
    chat_log.configure(state="normal")
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    chat_log.insert("end", f"{timestamp}\n", "timestamp")
    chat_log.insert("end", f"{system_name}: ", system_name_tag)
    typing_indicator_index = chat_log.index("end-1c")  
    chat_log.insert("end", "is typing...\n", "typing_indicator")
    chat_log.update_idletasks()
    chat_log.configure(state="disabled")
    chat_log.yview("end")
    chat_log.update_idletasks()

    response = await generate_response(current_persona, [{'role': 'user', 'content': message}], temperature_var, top_p_var, top_k_var)  # pass message as list of dict
    response_content = response.get('generated_text')  # get generated_text from response
    logger.info("Generated response: %s", response_content)
    chat_log.configure(state="normal")
    chat_log.delete(typing_indicator_index, "end")  
    chat_log.insert("end", response_content + "\n")
    chat_log.configure(state="disabled")
    chat_log.yview("end")
