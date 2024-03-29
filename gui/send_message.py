# gui\components\send_message.py

import time
import asyncio
import logging

from logging.handlers import RotatingFileHandler

logger = logging.getLogger('send_message.py')

log_filename = 'SCOUT.log'
log_max_size = 10 * 1024 * 1024  # 10 MB
log_backup_count = 5

rotating_handler = RotatingFileHandler(log_filename, maxBytes=log_max_size, backupCount=log_backup_count, encoding='utf-8')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
rotating_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(rotating_handler)
logger.addHandler(stream_handler)
logger.setLevel(logging.INFO)

def adjust_logging_level(level):
    """Adjust the logging level.
    
    Parameters:
    - level (str): Desired logging level. Can be 'DEBUG', 'INFO', 'WARNING', 'ERROR', or 'CRITICAL'.
    """
    levels = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR,
        'CRITICAL': logging.CRITICAL
    }
    
    logger.setLevel(levels.get(level, logging.WARNING))
 
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