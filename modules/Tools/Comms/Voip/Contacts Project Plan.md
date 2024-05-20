##  SCOUT VoIP Contacts Project Plan

**Goal:** Build an SQLite database to store contacts and integrate it with the `ContactsFrame` of your VoIP app.

**Phase 1: Database Setup**

-   [*] Create `contacts.db` database file.
-   [*] Create `contacts` table with columns: `id`, `name`, `numbers`, `email`, `address`, `company`, `position`.

**Phase 2: Database Interaction Functions**

-   [*] Write a function to create the database and table if they don't exist.
-   [*] Write a function to add new contacts to the database.
-   [*] Write a function to retrieve contacts from the database.
-   [*] Write a function to update existing contacts in the database.
-   [*] Write a function to delete contacts from the database.

**Phase 3: GUI Integration**

-   [ ] Modify `ContactsFrame` to connect to `contacts.db`.
-   [ ] Load contacts from the database into the `QListWidget` on app startup.
-   [ ] Add GUI functionality to add new contacts.
-   [ ] Add GUI functionality to edit existing contacts.
-   [ ] Add GUI functionality to delete contacts.

**Phase 4: Importing Contacts (Future)**

-   [ ] Research and implement importing from Google Contacts.
-   [ ] Research and implement importing from Apple Contacts.



### **Phase 1: Database Setup**
- **Create `contacts.db` database file:** ✅ Done
- **Create `contacts` table with columns: `id`, `name`, `numbers`, `email`, `address`, `company`, `position`:** ✅ Done

### **Phase 2: Database Interaction Functions**
- **Write a function to create the database and table if they don't exist:** ✅ Done
- **Write a function to add new contacts to the database:** ✅ Done
- **Write a function to retrieve contacts from the database:** ✅ Done
- **Write a function to update existing contacts in the database:** ✅ Done
- **Write a function to delete contacts from the database:** ✅ Done

### **Phase 3: GUI Integration**
- **Modify `ContactsFrame` to connect to `contacts.db`:** ✅ Done
- **Load contacts from the database into the `QListWidget` on app startup:** ✅ Done
- **Add GUI functionality to add new contacts:** ✅ Done
- **Add GUI functionality to edit existing contacts:** ✅ Done
- **Add GUI functionality to delete contacts:** ✅ Done

### **Phase 4: Importing Contacts (Future)**
- **Research and implement importing from Google Contacts:** ⬜ Not started
- **Research and implement importing from Apple Contacts:** ⬜ Not started

### **Next Steps:**
**Plan for Phase 4** by researching APIs for Google Contacts and Apple Contacts.




### Additional Features for the Contacts Part of the App

Based on what I've seen, here are some additional features you might consider adding to the contacts part of the app:

1. **Search Functionality**:
   - Add a search bar to filter contacts by name, number, or other fields.

2. **Import/Export Contacts**:
   - Allow users to import contacts from a CSV file or export their contacts to a CSV file.

3. **Contact Groups**:
   - Implement functionality to categorize contacts into groups (e.g., Family, Friends, Work).

4. **Profile Pictures**:
   - Allow users to add profile pictures to contacts.

5. **Favorite Contacts**:
   - Add a feature to mark certain contacts as favorites for quick access.

6. **Contact History**:
   - Maintain a history of interactions with each contact (e.g., messages sent, calls made).

7. **Enhanced Validation**:
   - Add more robust validation for contact details (e.g., email format, phone number format).

8. **Backup and Restore**:
   - Implement a backup and restore feature to save and retrieve contacts.

9. **Contact Notes**:
   - Allow users to add detailed notes for each contact.

10. **UI Enhancements**:
    - Improve the UI with better styling, animations, and user feedback.

### Example: Adding a Search Functionality

Here's a quick example of how you might add a search bar to filter contacts:

```python
class ContactsFrame(qtw.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setStyleSheet("background-color: transparent;")
        layout = qtw.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Search Bar
        self.search_bar = qtw.QLineEdit()
        self.search_bar.setPlaceholderText("Search contacts...")
        self.search_bar.textChanged.connect(self.filter_contacts)
        layout.addWidget(self.search_bar)

        # Create a frame for the buttons and add it to the layout
        button_frame = qtw.QFrame()
        button_layout = qtw.QHBoxLayout(button_frame)
        button_layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(button_frame)

        icon_size = 24

        self.add_button = qtw.QPushButton(button_frame)
        self.add_button.setIcon(qtg.QIcon("assets/SCOUT/Icons/Voip_icons/add_wt.png"))
        self.add_button.setIconSize(qtc.QSize(icon_size, icon_size))
        self.add_button.setStyleSheet("QPushButton { background-color: transparent; border: none; }")
        self.add_button.clicked.connect(self.show_contact_details)
        button_layout.addWidget(self.add_button)

        self.edit_button = qtw.QPushButton(button_frame)
        self.edit_button.setIcon(qtg.QIcon("assets/SCOUT/Icons/Voip_icons/edit_wt.png"))
        self.edit_button.setIconSize(qtc.QSize(icon_size, icon_size))
        self.edit_button.setStyleSheet("QPushButton { background-color: transparent; border: none; }")
        self.edit_button.clicked.connect(self.edit_contact)
        button_layout.addWidget(self.edit_button)

        # Create the contact list and add it to the layout
        self.contact_list = qtw.QListWidget()
        self.contact_list.setStyleSheet("""
            QListWidget {
                background-color: #2d2d2d;
                color: #ffffff;
                border: none;
                border-radius: 10px;
                padding: 2px 0 0 2px;
            }
            QListWidgetItem {
                padding-left: 2px;
            }
        """)
        layout.addWidget(self.contact_list)

        self.contact_list.setContextMenuPolicy(qtc.Qt.CustomContextMenu)
        self.contact_list.customContextMenuRequested.connect(self.show_context_menu)
        self.contact_list.itemClicked.connect(self.display_selected_contact)

        self.db = ContactsDatabase()
        self.load_contacts()

    def filter_contacts(self):
        search_text = self.search_bar.text().lower()
        for i in range(self.contact_list.count()):
            item = self.contact_list.item(i)
            item.setHidden(search_text not in item.text().lower())
