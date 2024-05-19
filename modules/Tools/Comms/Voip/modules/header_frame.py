# modules/Tools/Comms/Voip/modules/header_frame.py
from PySide6 import QtWidgets as qtw
from PySide6 import QtCore as qtc
from PySide6 import QtGui as qtg

def create_header_frame(voip_app, layout):
    header_frame = qtw.QFrame(voip_app)
    header_frame.setStyleSheet("background-color: #2d2d2d ; border-radius: 10px;")
    header_layout = qtw.QHBoxLayout(header_frame)
    header_layout.setContentsMargins(10, 10, 10, 10)
    header_layout.setSpacing(5)  
    layout.addWidget(header_frame)

    icon_size = 32

    contacts_img = qtg.QPixmap("assets/SCOUT/Icons/Voip_icons/contacts_wt.png")
    contacts_img = contacts_img.scaled(icon_size, icon_size)

    contacts_button = qtw.QPushButton(header_frame)
    contacts_button.setIcon(qtg.QIcon(contacts_img))
    contacts_button.setIconSize(qtc.QSize(icon_size, icon_size))
    contacts_button.setStyleSheet("QPushButton { background-color: transparent; border: none; }")
    contacts_button.clicked.connect(voip_app.toggle_contacts) 
    header_layout.addWidget(contacts_button)

    def on_contacts_button_hover(event):
        hover_img = qtg.QPixmap("assets/SCOUT/Icons/Voip_icons/contacts_bl.png")
        hover_img = hover_img.scaled(icon_size, icon_size)
        contacts_button.setIcon(qtg.QIcon(hover_img))

    def on_contacts_button_leave(event):
        contacts_button.setIcon(qtg.QIcon(contacts_img))

    contacts_button.enterEvent = lambda event: on_contacts_button_hover(event)
    contacts_button.leaveEvent = lambda event: on_contacts_button_leave(event)

    keypad_button = qtw.QPushButton(header_frame)
    keypad_button.setIcon(qtg.QIcon("assets/SCOUT/Icons/Voip_icons/keypad_wt.png"))
    keypad_button.setIconSize(qtc.QSize(icon_size, icon_size))
    keypad_button.setStyleSheet("QPushButton { background-color: transparent; border: none; }")
    keypad_button.clicked.connect(voip_app.show_phone_page) 
    header_layout.addWidget(keypad_button)

    def on_keypad_button_hover(event):
        keypad_button.setIcon(qtg.QIcon("assets/SCOUT/Icons/Voip_icons/keypad_bl.png"))

    def on_keypad_button_leave(event):
        keypad_button.setIcon(qtg.QIcon("assets/SCOUT/Icons/Voip_icons/keypad_wt.png"))

    keypad_button.enterEvent = lambda event: on_keypad_button_hover(event)
    keypad_button.leaveEvent = lambda event: on_keypad_button_leave(event)

    messages_button = qtw.QPushButton(header_frame)
    messages_button.setIcon(qtg.QIcon("assets/SCOUT/Icons/Voip_icons/messages_wt.png"))
    messages_button.setIconSize(qtc.QSize(icon_size, icon_size))
    messages_button.setStyleSheet("QPushButton { background-color: transparent; border: none; }")
    messages_button.clicked.connect(voip_app.show_messages_page)  
    header_layout.addWidget(messages_button)

    def on_messages_button_hover(event):
        messages_button.setIcon(qtg.QIcon("assets/SCOUT/Icons/Voip_icons/messages_bl.png"))

    def on_messages_button_leave(event):
        messages_button.setIcon(qtg.QIcon("assets/SCOUT/Icons/Voip_icons/messages_wt.png"))

    messages_button.enterEvent = lambda event: on_messages_button_hover(event)
    messages_button.leaveEvent = lambda event: on_messages_button_leave(event)

    settings_button = qtw.QPushButton(header_frame)
    settings_button.setIcon(qtg.QIcon("assets/SCOUT/Icons/settings_wt.png"))
    settings_button.setIconSize(qtc.QSize(icon_size, icon_size))
    settings_button.setStyleSheet("QPushButton { background-color: transparent; border: none; }")
    #settings_button.clicked.connect()  
    header_layout.addWidget(settings_button)

    def on_settings_button_hover(event):
        settings_button.setIcon(qtg.QIcon("assets/SCOUT/Icons/settings_bl.png"))

    def on_settings_button_leave(event):
        settings_button.setIcon(qtg.QIcon("assets/SCOUT/Icons/settings_wt.png"))

    settings_button.enterEvent = lambda event: on_settings_button_hover(event)
    settings_button.leaveEvent = lambda event: on_settings_button_leave(event)
