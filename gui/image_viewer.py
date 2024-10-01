from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import Qt

class ImageViewer(QLabel):
    def __init__(self):
        super().__init__()
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setMinimumSize(400, 300)
