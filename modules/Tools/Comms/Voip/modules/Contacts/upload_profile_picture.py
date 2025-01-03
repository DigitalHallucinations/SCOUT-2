# modules/Tools/Comms/Voip/modules/Contacts/upload_profile_picture.py


from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QFileDialog, QSlider
from PySide6.QtCore import Qt, QPointF, QByteArray, QBuffer, QIODevice

from PySide6.QtGui import QPixmap, QMouseEvent, QWheelEvent, QPainter, QPainterPath
from modules.logging.logger import setup_logger

logger = setup_logger('upload_profile_picture.py')

class UploadProfilePictureFrame(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setWindowTitle("Upload Profile Picture")
        self.setGeometry(100, 100, 400, 400)
        self.setStyleSheet("background-color: #2d2d2d; color: #ffffff;")

        self.profile_pic_label = QLabel(self)
        self.profile_pic_label.setFixedSize(200, 200)
        self.profile_pic_label.setStyleSheet("border: 1px solid #ffffff; border-radius: 100px;")
        self.profile_pic_label.setAlignment(Qt.AlignCenter)

        self.upload_button = QPushButton("Upload Profile Picture", self)
        self.upload_button.clicked.connect(self.upload_profile_picture)

        self.zoom_slider = QSlider(Qt.Horizontal, self)
        self.zoom_slider.setRange(10, 200)
        self.zoom_slider.setValue(100)
        self.zoom_slider.valueChanged.connect(self.zoom_image)

        self.accept_button = QPushButton("Accept", self)
        self.accept_button.clicked.connect(self.accept_profile_picture)

        layout = QVBoxLayout(self)
        layout.addWidget(self.profile_pic_label, alignment=Qt.AlignCenter)
        layout.addWidget(self.upload_button)
        layout.addWidget(self.zoom_slider)
        layout.addWidget(self.accept_button)

        self.setLayout(layout)

        self.profile_pic_data = None
        self.drag_start_position = QPointF()
        self.current_pixmap = QPixmap()
        self.current_scale = 1.0
        self.image_offset = QPointF(0, 0)

        self.profile_pic_label.installEventFilter(self)

    def upload_profile_picture(self):
        file_dialog = QFileDialog(self)
        file_dialog.setNameFilter("Images (*.png *.xpm *.jpg)")
        if file_dialog.exec():
            file_path = file_dialog.selectedFiles()[0]
            with open(file_path, 'rb') as file:  # Read as bytes
                self.profile_pic_data = file.read()
            self.current_pixmap.loadFromData(self.profile_pic_data)
            self.update_profile_picture()
            logger.info(f"Profile picture uploaded: {file_path}")

    def zoom_image(self, value):
        self.current_scale = value / 100.0
        self.update_profile_picture()

    def update_profile_picture(self):
        if not self.current_pixmap.isNull():
            scaled_pixmap = self.current_pixmap.scaled(
                self.profile_pic_label.size() * self.current_scale,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            self.draw_circular_pixmap(scaled_pixmap)

    def draw_circular_pixmap(self, pixmap):
        size = self.profile_pic_label.size()
        mask = QPixmap(size)
        mask.fill(Qt.transparent)

        painter = QPainter(mask)
        painter.setRenderHint(QPainter.Antialiasing)
        path = QPainterPath()
        path.addEllipse(0, 0, size.width(), size.height())
        painter.setClipPath(path)
        painter.drawPixmap(self.image_offset.toPoint(), pixmap)
        painter.end()

        self.profile_pic_label.setPixmap(mask)

    def accept_profile_picture(self):
        if self.parent:
            final_pixmap = self.profile_pic_label.pixmap()
            if not final_pixmap.isNull():
                byte_array = QByteArray()
                buffer = QBuffer(byte_array)
                buffer.open(QIODevice.WriteOnly)
                final_pixmap.save(buffer, "PNG")
                self.profile_pic_data = byte_array.data()
                self.parent.update_profile_picture(self.profile_pic_data)
                self.parent.toggle_upload_frame()
        self.close()

    def eventFilter(self, source, event):
        if source is self.profile_pic_label:
            if event.type() == QMouseEvent.MouseButtonPress:
                self.drag_start_position = event.position()
            elif event.type() == QMouseEvent.MouseMove:
                if not self.drag_start_position.isNull():
                    delta = event.position() - self.drag_start_position
                    self.drag_start_position = event.position()
                    self.image_offset += delta
                    self.update_profile_picture()
            elif event.type() == QMouseEvent.MouseButtonRelease:
                self.drag_start_position = QPointF()
            elif event.type() == QWheelEvent.Wheel:
                self.zoom_slider.setValue(self.zoom_slider.value() + event.angleDelta().y() / 120)
        return super().eventFilter(source, event)