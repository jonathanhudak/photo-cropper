from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QScrollArea, QVBoxLayout
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, pyqtSignal

class ThumbnailGallery(QScrollArea):
    thumbnail_selected = pyqtSignal(str)  # Signal to emit the path of the selected image

    def __init__(self):
        super().__init__()
        self.setWidgetResizable(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.container = QWidget()
        self.layout = QHBoxLayout(self.container)
        self.setWidget(self.container)

    def add_thumbnail(self, image_path, label_text):
        thumbnail_widget = QWidget()
        thumbnail_layout = QVBoxLayout(thumbnail_widget)

        thumbnail = QLabel()
        pixmap = QPixmap(image_path).scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        thumbnail.setPixmap(pixmap)
        thumbnail.setToolTip(image_path)
        thumbnail.mousePressEvent = lambda event, path=image_path: self.thumbnail_selected.emit(path)

        label = QLabel(label_text)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        thumbnail_layout.addWidget(thumbnail)
        thumbnail_layout.addWidget(label)

        self.layout.addWidget(thumbnail_widget)

    def clear_thumbnails(self):
        for i in reversed(range(self.layout.count())): 
            self.layout.itemAt(i).widget().setParent(None)
