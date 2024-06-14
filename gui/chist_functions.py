# gui/chist_functions.py

import asyncio
from PySide6 import QtWidgets, QtGui
from datetime import datetime
from modules.logging.logger import setup_logger

logger = setup_logger('chist_functions.py')

def load_chat_history(chat_component, provider_manager):
    logger.info("Opening chat history")
    chat_component.popup = QtWidgets.QDialog(chat_component)
    chat_component.popup.setWindowTitle("Chat History")
    chat_component.popup.setStyleSheet(f"background-color: {chat_component.appearance_settings_instance.history_frame_bg}; color: {chat_component.appearance_settings_instance.history_font_color};")

    font = QtGui.QFont(chat_component.appearance_settings_instance.history_font_family, int(chat_component.appearance_settings_instance.history_font_size), QtGui.QFont.Normal)
    chat_component.popup.setFont(font)

    user = chat_component.user
    persona_name = chat_component.current_persona.get('name') if chat_component.current_persona else 'Unknown'
    logger.info(f"Current persona_name: {persona_name}")

    # Use chat_component.conversation_manager directly
    conversation_manager = chat_component.conversation_manager

    chat_logs = conversation_manager.get_conversations(user, persona=persona_name)
    logger.debug(f"Chat logs fetched for {persona_name}: {chat_logs}")
    logger.info(f"Chat logs fetched for {persona_name}")
    chat_component.chat_log_listbox = QtWidgets.QListWidget(chat_component.popup)
    chat_component.chat_log_listbox.setFont(font)
    chat_component.chat_log_listbox.setStyleSheet(f"background-color: {chat_component.appearance_settings_instance.history_frame_bg}; color: {chat_component.appearance_settings_instance.history_font_color};")

    for chat_log_tuple in chat_logs:
        _, timestamp, persona, conversation_id, name = chat_log_tuple
        display_name = name if name else persona
        formatted_timestamp = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S").strftime("%b %d, %Y")
        entry = f"{display_name}: {formatted_timestamp}@@{conversation_id}"  # Include conversation_id
        chat_component.chat_log_listbox.addItem(entry)

    layout = QtWidgets.QVBoxLayout(chat_component.popup)
    layout.addWidget(chat_component.chat_log_listbox)

    save_chat_button = QtWidgets.QPushButton("Save Current Chat", chat_component.popup)
    save_chat_button.setFont(font)
    save_chat_button.setStyleSheet(f"background-color: #7289da; color: {chat_component.appearance_settings_instance.history_font_color};")
    save_chat_button.clicked.connect(lambda: asyncio.create_task(save_and_start_new_conversation(chat_component, chat_component.provider_manager, chat_component.cognitive_services)))
    layout.addWidget(save_chat_button)

    load_chat_button = QtWidgets.QPushButton("Load Selected Chat", chat_component.popup)
    load_chat_button.setFont(font)
    load_chat_button.setStyleSheet(f"background-color: #7289da; color: {chat_component.appearance_settings_instance.history_font_color};")
    load_chat_button.clicked.connect(lambda: asyncio.create_task(load_chat(chat_component, chat_component.chat_log_listbox.currentItem().text(), chat_component.provider_manager, chat_component.cognitive_services)))
    layout.addWidget(load_chat_button)   

    delete_button = QtWidgets.QPushButton("Delete", chat_component.popup)
    delete_button.setFont(font)
    delete_button.setStyleSheet(f"background-color: #7289da; color: {chat_component.appearance_settings_instance.history_font_color};")
    delete_button.clicked.connect(lambda: delete_conversation(chat_component, chat_component.provider_manager))
    layout.addWidget(delete_button)

    chat_component.popup.setModal(False)  
    chat_component.popup.show() 

async def save_and_start_new_conversation(chat_component, provider_manager, cognitive_services):
    await clear_chat_log(chat_component, provider_manager, cognitive_services)
    chat_component.conversation_id = chat_component.conversation_manager.init_conversation_id()
    logger.info(f"Started a new conversation with ID: {chat_component.conversation_id}")
    chat_component.show_message("system", chat_component.current_persona["message"])

async def load_chat(chat_component, selected_chat_log=None, provider_manager=None, cognitive_services=None):
    if not selected_chat_log:
        logger.warning("No chat log entry selected.")
        return

    _, conversation_id = selected_chat_log.split("@@", 1)  

    user = chat_component.user

    chat_component.conversation_id = conversation_id  

    logger.info(f"Updated conversation_id in ChatComponent: {conversation_id}")

    await clear_chat_log(chat_component, provider_manager, cognitive_services)

    persona_name = chat_component.current_persona.get('name') if chat_component.current_persona else 'Unknown'
    logger.info(f"Current persona_name: {persona_name}")

    # Use chat_component.conversation_manager directly
    conversation_manager = chat_component.conversation_manager

    actual_chat_log = conversation_manager.get_chat_log(user, conversation_id)

    if actual_chat_log:
        chat_component.chat_log.setPlainText(actual_chat_log)
        chat_component.chat_log.verticalScrollBar().setValue(chat_component.chat_log.verticalScrollBar().maximum())
        chat_component.apply_font_settings()
    else:
        logger.error(f"No chat log found for Conversation ID: {conversation_id}")

def delete_conversation(chat_component, provider_manager):
    selected_item = chat_component.chat_log_listbox.currentItem()
    if not selected_item:
        logger.error("No chat log selected for deletion")        
        return

    selected_chat_log = selected_item.text()

    parts = selected_chat_log.split("@@")
    conversation_id = parts[0], parts[1]  
    user = chat_component.user

    persona_name = chat_component.current_persona.get('name') if chat_component.current_persona else 'Unknown'
    logger.info(f"Current persona_name: {persona_name}")

    # Use chat_component.conversation_manager directly
    conversation_manager = chat_component.conversation_manager

    conversation_manager.delete_conversation(user, conversation_id)

    chat_component.chat_log_listbox.takeItem(chat_component.chat_log_listbox.row(selected_item))

    logger.info(f"Chat log deleted: {selected_chat_log}")

    chat_component.chat_log_listbox.clear()
    chat_logs = conversation_manager.get_conversations(user, persona=persona_name)
    for chat_log_tuple in chat_logs:
        _, timestamp, persona, conversation_id, name = chat_log_tuple
        display_name = name if name else persona
        formatted_timestamp = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S").strftime("%b %d, %Y")
        entry = f"{display_name}: {formatted_timestamp}@@{conversation_id}"
        chat_component.chat_log_listbox.addItem(entry)

async def clear_chat_log(chat_component, provider_manager, cognitive_services):
    logger.info("Clearing chat log in the chat component")
    
    await save_chat_log(chat_component, provider_manager, cognitive_services, chat_component.conversation_manager)
    
    chat_component.chat_log.clear()

async def save_chat_log(chat_component, provider_manager, cognitive_services, conversation_manager):
    current_chat_log = chat_component.chat_log.toPlainText().strip()
    if current_chat_log:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        user = chat_component.user
        conversation_id = chat_component.conversation_id 

        persona_name = chat_component.current_persona.get('name') if chat_component.current_persona else 'Unknown'
        logger.info(f"Current persona_name: {persona_name}")

        await conversation_manager.insert_conversation(user, conversation_id, current_chat_log, timestamp, chat_component.current_persona["name"])

    logger.info(f"Chat log saved")