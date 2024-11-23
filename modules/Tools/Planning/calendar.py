# modules/Tools/Planning/calendar.py

import asyncio
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QCalendarWidget, QListWidget, QPushButton, QHBoxLayout, QLineEdit, QLabel, QMessageBox, QMenu, QInputDialog
from PySide6.QtCore import QDate, Qt
from modules.logging.logger import setup_logger
from modules.Tools.Planning.CalDatabase import Database

logger = setup_logger('calendar.py')

class Calendar(QMainWindow):
    def __init__(self):
        super().__init__()
        logger.info("Initializing calendar")

        self.db = Database()  # Create an instance of the Database class
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
        asyncio.create_task(self.load_appointments(date))

    def add_appointment(self):
        date = self.calendar_widget.selectedDate()
        appointment_text = self.appointment_input.text()
        if appointment_text:
            self.appointments_list.addItem(f"{date.toString('yyyy-MM-dd')}: {appointment_text}")
            asyncio.create_task(self.save_appointment(date, appointment_text))
            self.appointment_input.clear()
            logger.info(f"Added appointment: {appointment_text} on {date.toString('yyyy-MM-dd')}")
            asyncio.create_task(self.load_appointments(date))  # Refresh the appointments list

    def edit_appointment(self, item):
        appointment_text = item.text()
        date_str, old_text = appointment_text.split(": ", 1)
        date = QDate.fromString(date_str, 'yyyy-MM-dd')

        new_text, ok = QInputDialog.getText(self, "Edit Appointment", "Edit appointment details:", QLineEdit.Normal, old_text)
        if ok and new_text:
            item.setText(f"{date.toString('yyyy-MM-dd')}: {new_text}")
            asyncio.create_task(self.update_appointment(date, old_text, new_text))
            logger.info(f"Edited appointment: {old_text} to {new_text} on {date.toString('yyyy-MM-dd')}")
            asyncio.create_task(self.load_appointments(date))  # Refresh the appointments list

    async def load_appointments(self, date: QDate):
        logger.info(f"Loading appointments for {date.toString('yyyy-MM-dd')}")
        self.appointments_list.clear()
        date_str = date.toString('yyyy-MM-dd')
        appointments = self.db.get_appointments(date_str)
        for appointment in appointments:
            self.appointments_list.addItem(f"{date_str}: {appointment}")

    async def load_appointments_by_week(self, date: QDate):
        logger.info(f"Loading appointments for the week of {date.toString('yyyy-MM-dd')}")
        self.appointments_list.clear()
        start_of_week = date.addDays(-(date.dayOfWeek() - 1))
        end_of_week = start_of_week.addDays(6)
        appointments = self.db.get_appointments_by_week(start_of_week.toString('yyyy-MM-dd'), end_of_week.toString('yyyy-MM-dd'))
        for date_str, appointment in appointments:
            self.appointments_list.addItem(f"{date_str}: {appointment}")

    async def load_appointments_by_month(self, date: QDate):
        logger.info(f"Loading appointments for the month of {date.toString('yyyy-MM')}")
        self.appointments_list.clear()
        year = date.toString('yyyy')
        month = date.toString('MM')
        appointments = self.db.get_appointments_by_month(year, month)
        for date_str, appointment in appointments:
            self.appointments_list.addItem(f"{date_str}: {appointment}")

    async def load_appointments_by_year(self, date: QDate):
        logger.info(f"Loading appointments for the year of {date.year()}")
        self.appointments_list.clear()
        year = date.toString('yyyy')
        appointments = self.db.get_appointments_by_year(year)
        for date_str, appointment in appointments:
            self.appointments_list.addItem(f"{date_str}: {appointment}")

    async def save_appointment(self, date: QDate, appointment_text: str):
        date_str = date.toString('yyyy-MM-dd')
        await self.db.add_appointment(date_str, appointment_text)

    async def update_appointment(self, date: QDate, old_text: str, new_text: str):
        date_str = date.toString('yyyy-MM-dd')
        await self.db.update_appointment(date_str, old_text, new_text)

    async def delete_appointment(self, item):
        appointment_text = item.text()
        date_str, text = appointment_text.split(": ", 1)
        date = QDate.fromString(date_str, 'yyyy-MM-dd')

        reply = QMessageBox.question(self, 'Delete Appointment', f"Are you sure you want to delete the appointment: {text}?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            await self.db.delete_appointment(date_str, text)
            self.appointments_list.takeItem(self.appointments_list.row(item))
            logger.info(f"Deleted appointment: {text} on {date.toString('yyyy-MM-dd')}")
            asyncio.create_task(self.load_appointments(date))  # Refresh the appointments list

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

    async def handle_action(self, action, date, details=None):
        date_obj = QDate.fromString(date, 'yyyy-MM-dd')
        if action == 'add' and details:
            await self.save_appointment(date_obj, details)
            await self.load_appointments(date_obj)
            return {"status": "success", "message": f"Appointment added for {date}"}
        elif action == 'edit' and details:
            old_text, new_text = details.split('|', 1)
            await self.update_appointment(date_obj, old_text, new_text)
            await self.load_appointments(date_obj)
            return {"status": "success", "message": f"Appointment updated for {date}"}
        elif action == 'delete' and details:
            await self.delete_appointment_by_text(date_obj, details)
            await self.load_appointments(date_obj)
            return {"status": "success", "message": f"Appointment deleted for {date}"}
        elif action == 'load':
            await self.load_appointments(date_obj)
            return {"status": "success", "appointments": self.db.get_appointments(date)}
        elif action == 'load_week':
            await self.load_appointments_by_week(date_obj)
            return {"status": "success", "appointments": self.db.get_appointments_by_week(date_obj)}
        elif action == 'load_month':
            await self.load_appointments_by_month(date_obj)
            return {"status": "success", "appointments": self.db.get_appointments_by_month(date_obj)}
        elif action == 'load_year':
            await self.load_appointments_by_year(date_obj)
            return {"status": "success", "appointments": self.db.get_appointments_by_year(date_obj)}
        else:
            return {"status": "error", "message": "Invalid action"}

    async def delete_appointment_by_text(self, date, text):
        date_str = date.toString('yyyy-MM-dd')
        await self.db.delete_appointment(date_str, text)