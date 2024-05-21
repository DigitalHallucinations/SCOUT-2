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


### Imrovements for overall voip app

### Additional Features for the Contacts Part of the App

Based on what I've seen, here are some additional features you might consider adding to the contacts part of the app:

1. **Import/Export Contacts**:
   - Allow users to import contacts from a CSV file or export their contacts to a CSV file.

2. **Profile Pictures**:
   - Show profile picture at top in contacts, phone and messages in current contact frame on left side of frame.

3. **Favorite Contacts**:
   - Add a feature to mark certain contacts as favorites for quick access.

4. **Contact History**:
   - Maintain a history of interactions with each contact (e.g., messages sent, calls made).

5. **Enhanced Validation**:
   - Add more robust validation for contact details (e.g., email format, phone number format).

6. **Backup and Restore**:
   - Implement a backup and restore feature to save and retrieve contacts.

7. **UI Enhancements**:
    - Improve the UI with better styling, animations, and user feedback.




## Upload Profile Picture

1. **Create a New Frame for Uploading Profile Pictures**:
   - This frame will include a slider for zooming/resizing the image and the ability to drag the image within a circular frame.

2. **Integrate the New Frame into the Existing Application**:
   - Replace the `ContactDetailsFrame` with the new upload frame when the user selects an image.
   - Restore the `ContactDetailsFrame` when the user accepts the changes.

3. **Implement the Zoom and Drag Functionality**:
   - Use a slider to adjust the zoom level of the image.
   - Allow the user to drag the image within the circular frame.
