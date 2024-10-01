from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
from PyQt6.QtGui import QPixmap, QPainter, QColor
from PyQt6.QtCore import pyqtSignal, Qt
import os

class CropSelector(QWidget):
    crop_selected = pyqtSignal(str, tuple)  # Signal to emit when a crop is selected (path, coordinates)

    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.crops = []

        self.info_label = QLabel("No crops available")
        self.layout.addWidget(self.info_label)

    def set_crops(self, crops):
        # Clear previous crops
        for i in reversed(range(self.layout.count())): 
            widget = self.layout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)

        self.crops = crops
        if not crops:
            self.info_label = QLabel("No crops available")
            self.layout.addWidget(self.info_label)
        else:
            for i, crop_info in enumerate(crops):
                crop_button = self.create_crop_button(i, crop_info)
                self.layout.addWidget(crop_button)

    def create_crop_button(self, index, crop_info):
        crop_path, (x, y, w, h) = crop_info
        button = QPushButton()
        button.clicked.connect(lambda _, c=crop_info: self.select_crop(c))

        # Create a QHBoxLayout for the button content
        button_layout = QHBoxLayout()

        # Create and add the shape preview
        shape_preview = self.create_shape_preview(w, h)
        button_layout.addWidget(shape_preview)

        # Add the crop dimensions text
        button_layout.addWidget(QLabel(f"Crop {index+1}: {w}x{h} at ({x},{y})"))

        # Set the layout for the button
        button.setLayout(button_layout)

        return button

    def create_shape_preview(self, width, height):
        preview = QLabel()
        pixmap = QPixmap(50, 50)
        pixmap.fill(Qt.GlobalColor.white)

        painter = QPainter(pixmap)
        painter.setPen(QColor(0, 0, 0))
        painter.setBrush(QColor(0, 0, 0))

        # Calculate the rectangle size while maintaining aspect ratio
        if width > height:
            rect_width = 40
            rect_height = int(40 * (height / width))
        else:
            rect_height = 40
            rect_width = int(40 * (width / height))

        # Center the rectangle
        x = (50 - rect_width) // 2
        y = (50 - rect_height) // 2

        painter.drawRect(x, y, rect_width, rect_height)
        painter.end()

        preview.setPixmap(pixmap)
        return preview

    def select_crop(self, crop_info):
        crop_path, crop_coords = crop_info
        print(f"Debug: Crop selected: {crop_path}, coordinates: {crop_coords}")
        self.crop_selected.emit(crop_path, crop_coords)
