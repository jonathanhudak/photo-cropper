import cv2
import numpy as np
import os
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtCore import pyqtSignal, QObject
import time

class ImageProcessor(QObject):
    saliency_map_ready = pyqtSignal(str)
    progress_update = pyqtSignal(int, int)
    crops_ready = pyqtSignal(list)  # New signal to emit when crops are saved

    def __init__(self):
        super().__init__()
        self.model_path = "objectness_trained_model"  # Path to BING model files
        if os.path.exists(self.model_path):
            self.saliency = cv2.saliency.ObjectnessBING_create()
            self.saliency.setTrainingPath(self.model_path)
            print("BING objectness saliency model loaded successfully.")
        else:
            print("BING model files not found. Using fallback saliency method.")
            self.saliency = None

    def generate_crops(self, image_path):
        print(f"Starting to process image: {image_path}")
        start_time = time.time()
        
        image = cv2.imread(image_path)
        if image is None:
            print(f"Error: Unable to read image at {image_path}")
            return None, []

        print(f"Image loaded. Shape: {image.shape}")
        
        saliency_map = self.generate_saliency_map(image)
        saliency_map_path = self.save_saliency_map(saliency_map, image_path)
        self.saliency_map_ready.emit(saliency_map_path)
        
        height, width = image.shape[:2]
        crops = self.find_optimal_crops(saliency_map, width, height)
        
        saved_crops = self.save_crops(image, crops, image_path)
        
        end_time = time.time()
        print(f"Image processing completed in {end_time - start_time:.2f} seconds")
        
        return saliency_map_path, saved_crops

    def generate_saliency_map(self, image):
        print("Generating saliency map...")
        start_time = time.time()
        
        if self.saliency is not None:
            (success, saliencyMap) = self.saliency.computeSaliency(image)
            if success:
                heatmap = np.zeros((image.shape[0], image.shape[1]), dtype=np.uint8)
                for detection in saliencyMap[:10]:
                    (startX, startY, endX, endY) = detection.flatten().astype(int)
                    heatmap[startY:endY, startX:endX] += 50
                print(f"BING saliency map generated in {time.time() - start_time:.2f} seconds")
                return heatmap
        
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        gx = cv2.Sobel(blur, cv2.CV_64F, 1, 0, ksize=3)
        gy = cv2.Sobel(blur, cv2.CV_64F, 0, 1, ksize=3)
        magnitude = np.sqrt(gx**2 + gy**2)
        saliency_map = cv2.normalize(magnitude, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
        print(f"Fallback saliency map generated in {time.time() - start_time:.2f} seconds")
        return saliency_map

    def save_saliency_map(self, saliency_map, original_image_path):
        directory = os.path.dirname(original_image_path)
        filename = os.path.basename(original_image_path)
        name, ext = os.path.splitext(filename)
        saliency_map_path = os.path.join(directory, f"{name}_saliency_map{ext}")
        cv2.imwrite(saliency_map_path, saliency_map)
        print(f"Saliency map saved as {saliency_map_path}")
        return saliency_map_path

    def save_crops(self, image, crops, original_image_path):
        saved_crops = []
        base_name = os.path.splitext(os.path.basename(original_image_path))[0]
        directory = os.path.dirname(original_image_path)
        
        for i, (x, y, w, h) in enumerate(crops):
            crop_img = image[y:y+h, x:x+w]
            crop_filename = f"{base_name}_crop_{i+1}_{x}_{y}_{w}x{h}.jpg"
            crop_path = os.path.join(directory, crop_filename)
            cv2.imwrite(crop_path, crop_img)
            saved_crops.append((crop_path, (x, y, w, h)))
            print(f"Saved crop {i+1} to {crop_path}")
        
        return saved_crops

    def find_optimal_crops(self, saliency_map, width, height):
        print("Finding optimal crops...")
        start_time = time.time()
        crops = []
        aspect_ratios = [(1, 1), (4, 5), (16, 9), (9, 16)]

        for i, aspect_ratio in enumerate(aspect_ratios):
            print(f"Processing aspect ratio {aspect_ratio}...")
            crop = self.find_best_crop(saliency_map, width, height, aspect_ratio, i, len(aspect_ratios))
            crops.append(crop)

        print(f"Optimal crops found in {time.time() - start_time:.2f} seconds")
        return crops

    def find_best_crop(self, saliency_map, width, height, aspect_ratio, current_ratio, total_ratios):
        target_ratio = aspect_ratio[0] / aspect_ratio[1]
        best_score = -1
        best_crop = None

        # Use integral image for faster sum calculations
        integral = cv2.integral(saliency_map)

        scales = np.linspace(0.5, 1.0, 6)  # Reduced number of scales
        total_steps = len(scales) * ((height // 40) + 1) * ((width // 40) + 1)  # Increased step size
        current_step = 0

        for scale in scales:
            crop_width = int(width * scale)
            crop_height = int(crop_width / target_ratio)

            if crop_height > height:
                crop_height = height
                crop_width = int(crop_height * target_ratio)

            for y in range(0, height - crop_height + 1, 40):  # Increased step size
                for x in range(0, width - crop_width + 1, 40):  # Increased step size
                    # Calculate sum using integral image
                    crop_sum = (integral[y+crop_height][x+crop_width] + integral[y][x] - 
                                integral[y][x+crop_width] - integral[y+crop_height][x])
                    score = crop_sum / (crop_width * crop_height)

                    if score > best_score:
                        best_score = score
                        best_crop = (x, y, crop_width, crop_height)

                    current_step += 1
                    if current_step % 100 == 0:  # Update progress every 100 steps
                        progress = (current_ratio * total_steps + current_step) / (total_ratios * total_steps) * 100
                        self.progress_update.emit(int(progress), 100)
                        print(f"Progress: {progress:.2f}% - Best score: {best_score:.2f}")

        print(f"Best crop for aspect ratio {aspect_ratio}: {best_crop} with score {best_score:.2f}")
        return best_crop

    def calculate_score(self, saliency_map, x, y, width, height):
        # Simple score calculation based on saliency map
        score = np.mean(saliency_map[y:y+height, x:x+width])
        return score

    def apply_crop(self, image_path, crop):
        image = cv2.imread(image_path)
        if image is None:
            print(f"Error: Unable to read image at {image_path}")
            return None
        x, y, w, h = crop
        cropped_image = image[y:y+h, x:x+w]
        return self.cv2_to_qpixmap(cropped_image)

    def cv2_to_qpixmap(self, cv_img):
        height, width, channel = cv_img.shape
        bytes_per_line = 3 * width
        cv_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        q_img = QImage(cv_img.data, width, height, bytes_per_line, QImage.Format.Format_RGB888)
        return QPixmap.fromImage(q_img)

    # Add other methods as needed
