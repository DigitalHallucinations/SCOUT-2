# gui/send_message.py

import asyncio
from modules.logging.logger import setup_logger

logger = setup_logger('send_message.py')

async def send_message(chat_component, user, message, session_id, conversation_id, conversation_manager, model_manager, provider_manager):
    logger.info(f"send_message called with user: {user}, session_id: {session_id}, conversation_id: {conversation_id}")
    if not message:
        logger.warning("No message provided in send_message")
        return
        
    await process_message(chat_component, user, message, session_id, conversation_id, conversation_manager, model_manager, provider_manager)

async def process_message(chat_component, user, message, session_id, conversation_id, conversation_manager, model_manager, provider_manager):
    logger.info("process_message called")

    try:
        response = await asyncio.create_task(
            chat_component.provider_manager.generate_response(
                user, 
                chat_component.current_persona, 
                message, 
                session_id, 
                conversation_id, 
                chat_component.temperature, 
                chat_component.top_p, 
                chat_component.top_k,
                conversation_manager, 
                model_manager,  
                provider_manager  
            )
        )
        logger.info("Response received")
        chat_component.show_message("system", response)
    except Exception as e:
        logger.error(f"Error in process_message: {e}")
        chat_component.show_message("system", "An error occurred while processing your message.")
    
    logger.info("process_message completed")