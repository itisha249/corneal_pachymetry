import cv2
import numpy as np
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QPushButton, QFileDialog, QVBoxLayout, QWidget, QMessageBox
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

# Function to extract CCT (unchanged real logic)
def extract_cct_from_colorbar(image_path):
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"Image not found at path: {image_path}")

    
    print(f"Loaded image shape: {image.shape}")

   
    color_bar = image[50:200, 20:50] 
    if color_bar.size == 0:
        raise ValueError("Color bar region is empty. Check the cropping coordinates.")

    
    hsv_bar = cv2.cvtColor(color_bar, cv2.COLOR_BGR2HSV)
    hue_values = hsv_bar[:, :, 0]

    
    min_hue = np.min(hue_values)
    max_hue = np.max(hue_values)

    
    min_thickness = 300  # Minimum value (blue region)
    max_thickness = 710  # Maximum value (red region)

    
    central_region = image[90:205, 90:150] 
    if central_region.size == 0:
        raise ValueError("Central region is empty. Check the cropping coordinates.")

    
    central_hsv = cv2.cvtColor(central_region, cv2.COLOR_BGR2HSV)
    central_hue = np.mean(central_hsv[:, :, 0])

   
    print(f"Min Hue: {min_hue}, Max Hue: {max_hue}")
    print(f"Central Hue: {central_hue}")

    # Map the central hue to thickness using linear interpolation
    cct = min_thickness + (central_hue - min_hue) / (max_hue - min_hue) * (max_thickness - min_thickness)
    return cct

# PyQt5 GUI
class CCTCalculatorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CCT Calculator Nexuslink")
        self.setGeometry(100, 100, 600, 400)

        self.layout = QVBoxLayout()

        # Widgets
        self.label = QLabel("Central Corneal Thickness (CCT) Calculator", self)
        self.label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.label)

        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setText("No Image Selected")
        self.layout.addWidget(self.image_label)

        self.upload_button = QPushButton("Upload Image", self)
        self.upload_button.clicked.connect(self.upload_image)
        self.layout.addWidget(self.upload_button)

        self.result_label = QLabel("", self)
        self.result_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.result_label)

        # Container
        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

    def upload_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Image Files (*.jpeg *.jpg *.png)")
        if file_path:
            try:
                # Display the selected image
                pixmap = QPixmap(file_path)
                pixmap = pixmap.scaled(400, 300, Qt.KeepAspectRatio)
                self.image_label.setPixmap(pixmap)

                # Call the CCT extraction function
                cct_value = extract_cct_from_colorbar(file_path)
                self.result_label.setText(f"Central Corneal Thickness (CCT): {cct_value:.2f} µm")
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))

# Main Application
def main():
    app = QApplication([])
    window = CCTCalculatorApp()
    window.show()
    app.exec_()

if __name__ == "__main__":
    main()
