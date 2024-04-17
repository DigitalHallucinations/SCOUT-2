# gui\components\send_message.py

import time
import asyncio
from modules.logging.logger import setup_logger

logger = setup_logger('send_message.py')
 
async def send_message(chat_log, user, message_entry, system_name, system_name_tag, typing_indicator_index, generate_response, current_persona, temperature_var, top_p_var, top_k_var, session_id, conversation_id):
    logger.info(f"send_message called with user: {user}, session_id: {session_id}, conversation_id: {conversation_id}")
    message = message_entry.get("1.0", "end-1c").strip()
    if not message:
        logger.warning("No message provided in send_message")
        return
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())  
    chat_log.configure(state="normal")
    chat_log.insert("end", f"{timestamp}\n", "timestamp")
    chat_log.insert("end", f"{user}: ")   
    chat_log.insert("end", message + "\n")
    chat_log.configure(state="disabled")
    chat_log.yview("end")
    message_entry.delete("1.0", "end")
        
    asyncio.create_task(process_message(user, chat_log, system_name, system_name_tag, typing_indicator_index, generate_response, message, current_persona, temperature_var, top_p_var, top_k_var, session_id, conversation_id))


async def process_message(user, chat_log, system_name, system_name_tag, typing_indicator_index, generate_response, message, current_persona, temperature_var, top_p_var, top_k_var, session_id, conversation_id):
    logger.info("process_message called")

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

    response = await generate_response(user, current_persona, message, session_id, conversation_id, temperature_var, top_p_var, top_k_var)
  
    logger.info("Response received")
    
    chat_log.configure(state="normal")
    chat_log.delete(typing_indicator_index, "end")  
    chat_log.insert("end", response + "\n")
    chat_log.configure(state="disabled")
    chat_log.yview("end")
    logger.info("process_message completed")