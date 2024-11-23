# modules/Tools/Comms/Voip/modules/emoji_picker.py

from PySide6.QtWidgets import QDialog, QGridLayout, QPushButton
from modules.logging.logger import setup_logger

logger = setup_logger('emoji_picker.py')

class EmojiPicker(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Select Emoji")
        self.setFixedSize(400, 400)
        layout = QGridLayout(self)

        emojis = [
            "😊", "😂", "😍", "😢", "😎", "😡", "👍", "👎", "🙏", "👏", "💪", "🎉", "❤️", "🔥", "🌟",
            "😃", "😆", "😉", "😋", "😜", "😝", "😒", "😏", "😔", "😖", "😫", "😩", "😤", "😠", "😪",
            "😷", "🤒", "🤕", "🤢", "🤧", "😇", "🤠", "🤡", "🤥", "🤓", "😈", "👿", "👹", "👺", "💀",
            "👻", "👽", "🤖", "💩", "😺", "😸", "😹", "😻", "😼", "😽", "🙀", "😿", "😾", "🙈", "🙉",
            "🧑‍🦼", "👨‍🦼", "👩‍🦼", "🧑‍🦽", "👨‍🦽", "👩‍🦽", "🏃", "🏃‍♂️"
        ]
        positions = [(i, j) for i in range(5) for j in range(3)]

        for position, emoji in zip(positions, emojis):
            try:
                button = QPushButton(emoji)
                button.setFixedSize(50, 50)
                button.clicked.connect(lambda _, e=emoji: self.select_emoji(e))
                layout.addWidget(button, *position)
            except Exception as e:
                logger.error(f"Error adding emoji button {emoji} at position {position}: {e}")

    def select_emoji(self, emoji):
        try:
            self.selected_emoji = emoji
            self.accept()
            logger.info(f"Emoji selected: {emoji}")
        except Exception as e:
            logger.error(f"Error selecting emoji {emoji}: {e}")