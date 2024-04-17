# gui/chat_history/chist_functions.py

import tkinter as tk
from datetime import datetime
from modules.chat_history.convo_manager import ConversationManager
from modules.logging.logger import setup_logger

logger = setup_logger('chist_functions.py')

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

    conversation_manager = ConversationManager(user, persona_name)

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

    parts = selected_chat_log.split(": ")
    persona_convo_id, _ = parts[0], parts[1]  
    _, conversation_id = persona_convo_id.rsplit(" (", 1)
    conversation_id = conversation_id.strip(")")
    user = chat_component.user

    persona_name = chat_component.current_persona.get('name') if chat_component.current_persona else 'Unknown'
    logger.info(f"Current persona_name: {persona_name}")

    conversation_manager = ConversationManager(user, persona_name)

    conversation_manager.delete_conversation(user, conversation_id)

    chat_component.chat_log_listbox.delete(selected_index[0])

    logger.info(f"Chat log deleted: {selected_chat_log}")


def clear_chat_log(chat_component):
    """Clear the chat log in the chat component.
    
    Parameters:
    - chat_component: The chat component instance.
    """
    logger.info("Clearing chat log in the chat component")
    
    save_chat_log(chat_component)
    
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

    _, conversation_id = selected_chat_log.split("@@", 1)  

    user = chat_component.user

    chat_component.update_conversation_id(conversation_id)

    logger.info(f"Updated conversation_id in ChatComponent: {conversation_id}")

    clear_chat_log(chat_component)

    persona_name = chat_component.current_persona.get('name') if chat_component.current_persona else 'Unknown'
    logger.info(f"Current persona_name: {persona_name}")

    conversation_manager = ConversationManager(user, persona_name)

    actual_chat_log = conversation_manager.get_chat_log(user, conversation_id)

    if actual_chat_log:
        chat_component.chat_log.config(state="normal")
        chat_component.chat_log.delete(1.0, "end")
        chat_component.chat_log.insert("end", actual_chat_log)
        chat_component.chat_log.config(state="disabled")
        chat_component.chat_log.yview(tk.END)
    else:
        logger.error(f"No chat log found for Conversation ID: {conversation_id}")
