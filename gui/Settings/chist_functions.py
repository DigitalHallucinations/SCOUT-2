# gui/chat_history/chist_functions.py

import tkinter as tk
from datetime import datetime
import logging
from logging.handlers import RotatingFileHandler
from modules.chat_history.convo_manager import ConversationManager

logger = logging.getLogger('chist_functions.py')

log_filename = 'SCOUT.log'
log_max_size = 10 * 1024 * 1024  # 10 MB
log_backup_count = 5

# Create rotating file handler for file logging
rotating_handler = RotatingFileHandler(log_filename, maxBytes=log_max_size, backupCount=log_backup_count, encoding='utf-8')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
rotating_handler.setFormatter(formatter)

# Create stream handler for console logging
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

# Attach handlers to the logger
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

def load_chat_popup(chat_component):
    """Open the chat history popup.
    
    Parameters:
    - chat_component: The chat component instance.
    """
    logger.info("Opening chat history popup")
    chat_component.popup = tk.Toplevel(chat_component)
    chat_component.popup.title("Chat History")

    user = chat_component.user
    persona_name = chat_component.current_persona.get('name') if chat_component.current_persona else 'Unknown'
    logger.info(f"Current persona_name: {persona_name}")

    # Create a new ConversationManager instance for the specific persona
    conversation_manager = ConversationManager(user, persona_name)

    # Fetch chat logs for the current persona
    chat_logs = conversation_manager.get_conversations(user, persona=persona_name)
    logger.info(f"Chat logs fetched for {persona_name}: {chat_logs}")

    chat_component.chat_log_listbox = tk.Listbox(chat_component.popup)
    chat_component.chat_log_listbox.pack(side="top", padx=10, pady=(10, 0))

    for chat_log_tuple in chat_logs:
        _, timestamp, persona, conversation_id, name = chat_log_tuple
        display_name = name if name else persona
        formatted_timestamp = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S").strftime("%b %d, %Y")
        entry = f"{display_name}: {formatted_timestamp}@@{conversation_id}"  # Include conversation_id
        chat_component.chat_log_listbox.insert("end", entry)

    load_chat_button = tk.Button(chat_component.popup, text="Load Selected Chat", command=lambda: load_chat(chat_component, chat_component.chat_log_listbox.get(chat_component.chat_log_listbox.curselection())), bg="#7289da", fg="#ffffff", activebackground="#5a6dad", activeforeground="#ffffff")
    load_chat_button.pack(side="bottom", padx=10, pady=(0, 10))   

    delete_button = tk.Button(chat_component.popup, text="Delete", command=lambda: delete_conversation(chat_component), bg="#7289da", fg="#ffffff", activebackground="#5a6dad", activeforeground="#ffffff")
    delete_button.pack(side="bottom", padx=10, pady=(0, 10))

def delete_conversation(chat_component):
    """Delete the selected conversation from the chat history.
    
    Parameters:
    - chat_component: The chat component instance.
    """
    selected_index = chat_component.chat_log_listbox.curselection()
    if not selected_index:
        logger.error("No chat log selected for deletion")        
        return

    selected_chat_log = chat_component.chat_log_listbox.get(selected_index[0])

    # Extract details from the selected chat log entry
    parts = selected_chat_log.split(": ")
    persona_convo_id, _ = parts[0], parts[1]  # Timestamp is no longer needed
    _, conversation_id = persona_convo_id.rsplit(" (", 1)
    conversation_id = conversation_id.strip(")")
    user = chat_component.user

    persona_name = chat_component.current_persona.get('name') if chat_component.current_persona else 'Unknown'
    logger.info(f"Current persona_name: {persona_name}")

    # Create a new ConversationManager instance for the specific persona
    conversation_manager = ConversationManager(user, persona_name)

    # Delete the chat log and related data from the database
    conversation_manager.delete_conversation(user, conversation_id)

    # Remove the entry from the listbox
    chat_component.chat_log_listbox.delete(selected_index[0])

    logger.info(f"Chat log deleted: {selected_chat_log}")


def clear_chat_log(chat_component):
    """Clear the chat log in the chat component.
    
    Parameters:
    - chat_component: The chat component instance.
    """
    logger.info("Clearing chat log in the chat component")
    
    # Save the current chat log before clearing it
    save_chat_log(chat_component)
    
    # Clear the chat log in the chat component
    chat_component.chat_log.configure(state="normal")  
    chat_component.chat_log.delete(1.0, "end") 
    chat_component.chat_log.configure(state="disabled")

def save_chat_log(chat_component):
    """Save the current chat log.
    
    Parameters:
    - chat_component: The chat component instance.
    """
    current_chat_log = chat_component.chat_log.get('1.0', tk.END).strip()
    if current_chat_log:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        user = chat_component.user
        conversation_id = chat_component.conversation_id 

        persona_name = chat_component.current_persona.get('name') if chat_component.current_persona else 'Unknown'
        logger.info(f"Current persona_name: {persona_name}")

        # Create a new ConversationManager instance for the specific persona
        conversation_manager = ConversationManager(user, persona_name)

        conversation_manager.insert_conversation(user, conversation_id, current_chat_log, timestamp, chat_component.current_persona["name"])  
    logger.info(f"Chat log saved")


def load_chat(chat_component, selected_chat_log=None):
    """Load the selected chat log into the chat component.
    
    Parameters:
    - chat_component: The chat component instance.
    - selected_chat_log (optional): The selected chat log entry from the listbox.
    """
    if not selected_chat_log:
        logger.warning("No chat log entry selected.")
        return

    # Extracting the conversation ID from the listbox entry
    _, conversation_id = selected_chat_log.split("@@", 1)  # Splitting to get the conversation_id

    user = chat_component.user

    # Update conversation_id in ChatComponent
    chat_component.update_conversation_id(conversation_id)

    # Log the new conversation_id
    logger.info(f"Updated conversation_id in ChatComponent: {conversation_id}")

    # Clearing the chat log before loading new content
    clear_chat_log(chat_component)

    persona_name = chat_component.current_persona.get('name') if chat_component.current_persona else 'Unknown'
    logger.info(f"Current persona_name: {persona_name}")

    # Create a new ConversationManager instance for the specific persona
    conversation_manager = ConversationManager(user, persona_name)

    # Retrieving the actual chat log from the database
    actual_chat_log = conversation_manager.get_chat_log(user, conversation_id)

    if actual_chat_log:
        chat_component.chat_log.config(state="normal")
        chat_component.chat_log.delete(1.0, "end")
        chat_component.chat_log.insert("end", actual_chat_log)
        chat_component.chat_log.config(state="disabled")
        chat_component.chat_log.yview(tk.END)
    else:
        logger.error(f"No chat log found for Conversation ID: {conversation_id}")
