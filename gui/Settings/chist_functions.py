# gui/Settings/chist_functions.py

from PySide6 import QtWidgets, QtGui
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
    chat_component.popup = QtWidgets.QDialog(chat_component)
    chat_component.popup.setWindowTitle("Chat History")
    chat_component.popup.setStyleSheet(f"background-color: #000000; color: {chat_component.font_color};")

    font = QtGui.QFont(chat_component.font_family, int(chat_component.font_size), QtGui.QFont.Normal)
    chat_component.popup.setFont(font)

    user = chat_component.user
    persona_name = chat_component.current_persona.get('name') if chat_component.current_persona else 'Unknown'
    logger.info(f"Current persona_name: {persona_name}")

    conversation_manager = ConversationManager(user, persona_name)

    chat_logs = conversation_manager.get_conversations(user, persona=persona_name)
    logger.info(f"Chat logs fetched for {persona_name}: {chat_logs}")

    chat_component.chat_log_listbox = QtWidgets.QListWidget(chat_component.popup)
    chat_component.chat_log_listbox.setFont(font)
    chat_component.chat_log_listbox.setStyleSheet(f"background-color: #000000; color: {chat_component.font_color};")

    for chat_log_tuple in chat_logs:
        _, timestamp, persona, conversation_id, name = chat_log_tuple
        display_name = name if name else persona
        formatted_timestamp = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S").strftime("%b %d, %Y")
        entry = f"{display_name}: {formatted_timestamp}@@{conversation_id}"  # Include conversation_id
        chat_component.chat_log_listbox.addItem(entry)

    layout = QtWidgets.QVBoxLayout(chat_component.popup)
    layout.addWidget(chat_component.chat_log_listbox)

    load_chat_button = QtWidgets.QPushButton("Load Selected Chat", chat_component.popup)
    load_chat_button.setFont(font)
    load_chat_button.setStyleSheet(f"background-color: #7289da; color: {chat_component.font_color};")
    load_chat_button.clicked.connect(lambda: load_chat(chat_component, chat_component.chat_log_listbox.currentItem().text()))
    layout.addWidget(load_chat_button)   

    delete_button = QtWidgets.QPushButton("Delete", chat_component.popup)
    delete_button.setFont(font)
    delete_button.setStyleSheet(f"background-color: #7289da; color: {chat_component.font_color};")
    delete_button.clicked.connect(lambda: delete_conversation(chat_component))
    layout.addWidget(delete_button)

    chat_component.popup.exec()

def delete_conversation(chat_component):
    """Delete the selected conversation from the chat history.
    
    Parameters:
    - chat_component: The chat component instance.
    """
    selected_item = chat_component.chat_log_listbox.currentItem()
    if not selected_item:
        logger.error("No chat log selected for deletion")        
        return

    selected_chat_log = selected_item.text()

    parts = selected_chat_log.split(": ")
    persona_convo_id, _ = parts[0], parts[1]  
    _, conversation_id = persona_convo_id.rsplit(" (", 1)
    conversation_id = conversation_id.strip(")")
    user = chat_component.user

    persona_name = chat_component.current_persona.get('name') if chat_component.current_persona else 'Unknown'
    logger.info(f"Current persona_name: {persona_name}")

    conversation_manager = ConversationManager(user, persona_name)

    conversation_manager.delete_conversation(user, conversation_id)

    chat_component.chat_log_listbox.takeItem(chat_component.chat_log_listbox.row(selected_item))

    logger.info(f"Chat log deleted: {selected_chat_log}")


async def clear_chat_log(chat_component):
    """Clear the chat log in the chat component.
    
    Parameters:
    - chat_component: The chat component instance.
    """
    logger.info("Clearing chat log in the chat component")
    
    await save_chat_log(chat_component)
    
    chat_component.chat_log.clear()

async def save_chat_log(chat_component):
    """Save the current chat log.
    
    Parameters:
    - chat_component: The chat component instance.
    """
    current_chat_log = chat_component.chat_log.toPlainText().strip()
    if current_chat_log:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        user = chat_component.user
        conversation_id = chat_component.conversation_id 

        persona_name = chat_component.current_persona.get('name') if chat_component.current_persona else 'Unknown'
        logger.info(f"Current persona_name: {persona_name}")

        conversation_manager = ConversationManager(user, persona_name)
    
        await conversation_manager.insert_conversation(user, conversation_id, current_chat_log, timestamp, chat_component.current_persona["name"])

    logger.info(f"Chat log saved")


async def load_chat(chat_component, selected_chat_log=None):
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

    await clear_chat_log(chat_component)

    persona_name = chat_component.current_persona.get('name') if chat_component.current_persona else 'Unknown'
    logger.info(f"Current persona_name: {persona_name}")

    conversation_manager = ConversationManager(user, persona_name)

    actual_chat_log = conversation_manager.get_chat_log(user, conversation_id)

    if actual_chat_log:
        chat_component.chat_log.setPlainText(actual_chat_log)
        chat_component.chat_log.verticalScrollBar().setValue(chat_component.chat_log.verticalScrollBar().maximum())

        font = QtGui.QFont(chat_component.font_family, int(chat_component.font_size), QtGui.QFont.Normal)
        chat_component.chat_log.setFont(font)
        chat_component.chat_log.setStyleSheet(f"background-color: #000000; color: {chat_component.font_color};")
    else:
        logger.error(f"No chat log found for Conversation ID: {conversation_id}")