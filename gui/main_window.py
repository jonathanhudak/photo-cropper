from PyQt6.QtWidgets import (
    QMainWindow, QVBoxLayout, QPushButton, QWidget, QFileDialog, 
    QApplication, QMessageBox, QHBoxLayout, QLabel, QProgressBar
)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from .image_viewer import ImageViewer
from .thumbnail_gallery import ThumbnailGallery
from processing.image_processor import ImageProcessor

class ImageProcessingThread(QThread):
    finished = pyqtSignal(str, list)

    def __init__(self, image_processor, image_path):
        super().__init__()
        self.image_processor = image_processor
        self.image_path = image_path

    def run(self):
        saliency_map_path, crops = self.image_processor.generate_crops(self.image_path)
        self.finished.emit(saliency_map_path, crops)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Cropping App")
        self.setGeometry(100, 100, 1200, 800)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.top_layout = QHBoxLayout()
        self.bottom_layout = QHBoxLayout()

        self.image_viewer = ImageViewer()
        self.thumbnail_gallery = ThumbnailGallery()
        self.image_processor = ImageProcessor()

        self.upload_button = QPushButton("Upload Image")
        self.upload_button.clicked.connect(self.upload_image)

        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)

        self.top_layout.addWidget(self.upload_button)
        self.top_layout.addWidget(self.progress_bar)

        self.bottom_layout.addWidget(self.image_viewer)

        self.layout.addLayout(self.top_layout)
        self.layout.addLayout(self.bottom_layout)
        self.layout.addWidget(self.thumbnail_gallery)

        self.image_processor.progress_update.connect(self.update_progress)
        self.thumbnail_gallery.thumbnail_selected.connect(self.display_selected_image)

        self.current_image = None
        self.saliency_map_path = None

    def upload_image(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Image Files (*.png *.jpg *.bmp)")
        if file_name:
            self.current_image = file_name
            self.display_selected_image(file_name)
            self.process_image(file_name)

    def process_image(self, image_path):
        print(f"Debug: Processing image: {image_path}")
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.processing_thread = ImageProcessingThread(self.image_processor, image_path)
        self.processing_thread.finished.connect(self.on_processing_finished)
        self.processing_thread.start()

    def update_progress(self, current, total):
        self.progress_bar.setValue(int(current / total * 100))

    def on_processing_finished(self, saliency_map_path, crops):
        print("Image processing finished")
        self.progress_bar.setVisible(False)
        self.saliency_map_path = saliency_map_path
        self.thumbnail_gallery.clear_thumbnails()
        self.thumbnail_gallery.add_thumbnail(self.current_image, "Original")
        self.thumbnail_gallery.add_thumbnail(saliency_map_path, "Saliency Map")
        for i, (crop_path, _) in enumerate(crops, 1):
            self.thumbnail_gallery.add_thumbnail(crop_path, f"Crop {i}")

    def display_selected_image(self, image_path):
        pixmap = QPixmap(image_path)
        if not pixmap.isNull():
            self.image_viewer.setPixmap(pixmap.scaled(800, 600, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        else:
            print(f"Error: Failed to load image from {image_path}")
