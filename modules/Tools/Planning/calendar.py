# modules/Tools/Planning/calendar.py

import json
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QCalendarWidget, QListWidget, QPushButton, QHBoxLayout, QLineEdit, QLabel, QMessageBox, QMenu, QInputDialog
from PySide6.QtCore import QDate
from modules.logging.logger import setup_logger

logger = setup_logger('calendar.py')

class Calendar(QMainWindow):
    def __init__(self):
        super().__init__()
        logger.info("Initializing calendar")

        self.dark_mode = False

        # Create central widget and layout
        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)
        self.setCentralWidget(central_widget)

        # Dark mode toggle button
        self.dark_mode_button = QPushButton("Toggle Dark Mode")
        self.dark_mode_button.clicked.connect(self.toggle_dark_mode)
        main_layout.addWidget(self.dark_mode_button)

        # Create calendar widget
        self.calendar_widget = QCalendarWidget()
        self.calendar_widget.setGridVisible(True)
        self.calendar_widget.clicked.connect(self.date_selected)
        main_layout.addWidget(self.calendar_widget)

        # Create appointments list
        self.appointments_list = QListWidget()
        self.appointments_list.itemDoubleClicked.connect(self.edit_appointment)
        main_layout.addWidget(self.appointments_list)

        # Create input fields for new appointments
        input_layout = QHBoxLayout()
        self.appointment_input = QLineEdit()
        self.appointment_input.setPlaceholderText("Enter appointment details")
        self.add_appointment_button = QPushButton("Add Appointment")
        self.add_appointment_button.clicked.connect(self.add_appointment)
        input_layout.addWidget(self.appointment_input)
        input_layout.addWidget(self.add_appointment_button)
        main_layout.addLayout(input_layout)

        # Label to show selected date
        self.selected_date_label = QLabel("Selected Date: None")
        main_layout.addWidget(self.selected_date_label)

        # Load appointments from file
        self.appointments = self.load_appointments_from_file()

        # Apply initial styles
        self.apply_styles()

    def apply_styles(self):
        if self.dark_mode:
            self.setStyleSheet("""
                QMainWindow {
                    background-color: #121212;
                    color: #ffffff;
                }
                QCalendarWidget QAbstractItemView {
                    background-color: #333333;
                    color: #ffffff;
                }
                QCalendarWidget QWidget {
                    background-color: #333333;
                    color: #ffffff;
                }
                QCalendarWidget QHeaderView {
                    background-color: #333333;
                    color: #ffffff;
                }
                QCalendarWidget QToolButton {
                    background-color: #444444;
                    color: #ffffff;
                }
                QCalendarWidget QSpinBox {
                    background-color: #444444;
                    color: #ffffff;
                }
                QListWidget {
                    background-color: #333333;
                    color: #ffffff;
                }
                QLineEdit {
                    background-color: #333333;
                    color: #ffffff;
                }
                QPushButton {
                    background-color: #444444;
                    color: #ffffff;
                }
                QLabel {
                    color: #ffffff;
                }
            """)
            self.dark_mode_button.setText("Toggle Light Mode")
        else:
            self.setStyleSheet("""
                QMainWindow {
                    background-color: #000000;
                    color: #ffffff;
                }
                QCalendarWidget QAbstractItemView {
                    background-color: #ffffff;
                    color: #000000;
                }
                QCalendarWidget QWidget {
                    background-color: #ffffff;
                    color: #000000;
                }
                QCalendarWidget QHeaderView {
                    background-color: #ffffff;
                    color: #000000;
                }
                QCalendarWidget QToolButton {
                    background-color: #ffffff;
                    color: #000000;
                }
                QCalendarWidget QSpinBox {
                    background-color: #ffffff;
                    color: #000000;
                }
                QListWidget {
                    background-color: #ffffff;
                    color: #000000;
                }
                QLineEdit {
                    background-color: #ffffff;
                    color: #000000;
                }
                QPushButton {
                    background-color: #ffffff;
                    color: #000000;
                }
                QLabel {
                    color: #ffffff;
                }
            """)
            self.dark_mode_button.setText("Toggle Dark Mode")

    def date_selected(self, date: QDate):
        self.selected_date_label.setText(f"Selected Date: {date.toString('yyyy-MM-dd')}")
        self.load_appointments(date)

    def add_appointment(self):
        date = self.calendar_widget.selectedDate()
        appointment_text = self.appointment_input.text()
        if appointment_text:
            self.appointments_list.addItem(f"{date.toString('yyyy-MM-dd')}: {appointment_text}")
            self.save_appointment(date, appointment_text)
            self.appointment_input.clear()
            logger.info(f"Added appointment: {appointment_text} on {date.toString('yyyy-MM-dd')}")

    def edit_appointment(self, item):
        appointment_text = item.text()
        date_str, old_text = appointment_text.split(": ", 1)
        date = QDate.fromString(date_str, 'yyyy-MM-dd')

        new_text, ok = QInputDialog.getText(self, "Edit Appointment", "Edit appointment details:", QLineEdit.Normal, old_text)
        if ok and new_text:
            item.setText(f"{date.toString('yyyy-MM-dd')}: {new_text}")
            self.update_appointment(date, old_text, new_text)
            logger.info(f"Edited appointment: {old_text} to {new_text} on {date.toString('yyyy-MM-dd')}")

    def load_appointments(self, date: QDate):
        logger.info(f"Loading appointments for {date.toString('yyyy-MM-dd')}")
        self.appointments_list.clear()
        date_str = date.toString('yyyy-MM-dd')
        if date_str in self.appointments:
            for appointment in self.appointments[date_str]:
                self.appointments_list.addItem(f"{date_str}: {appointment}")

    def save_appointment(self, date: QDate, appointment_text: str):
        date_str = date.toString('yyyy-MM-dd')
        if date_str not in self.appointments:
            self.appointments[date_str] = []
        self.appointments[date_str].append(appointment_text)
        self.save_appointments_to_file()

    def update_appointment(self, date: QDate, old_text: str, new_text: str):
        date_str = date.toString('yyyy-MM-dd')
        if date_str in self.appointments:
            try:
                index = self.appointments[date_str].index(old_text)
                self.appointments[date_str][index] = new_text
                self.save_appointments_to_file()
            except ValueError:
                pass

    def load_appointments_from_file(self):
        try:
            with open('appointments.json', 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def save_appointments_to_file(self):
        with open('appointments.json', 'w') as file:
            json.dump(self.appointments, file)

    def delete_appointment(self, item):
        appointment_text = item.text()
        date_str, text = appointment_text.split(": ", 1)
        date = QDate.fromString(date_str, 'yyyy-MM-dd')

        reply = QMessageBox.question(self, 'Delete Appointment', f"Are you sure you want to delete the appointment: {text}?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.appointments[date_str].remove(text)
            self.appointments_list.takeItem(self.appointments_list.row(item))
            self.save_appointments_to_file()
            logger.info(f"Deleted appointment: {text} on {date.toString('yyyy-MM-dd')}")

    def contextMenuEvent(self, event):
        context_menu = QMenu(self)
        edit_action = context_menu.addAction("Edit")
        delete_action = context_menu.addAction("Delete")
        action = context_menu.exec_(self.mapToGlobal(event.pos()))

        if action == edit_action:
            self.edit_appointment(self.appointments_list.currentItem())
        elif action == delete_action:
            self.delete_appointment(self.appointments_list.currentItem())

    QListWidget.contextMenuEvent = contextMenuEvent

    def toggle_dark_mode(self):
        self.dark_mode = not self.dark_mode
        self.apply_styles()