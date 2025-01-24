# import matplotlib.pyplot as plt
# import cv2

# def show_central_region(image_path, crop_size=50):
#     image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
#     h, w = image.shape[:2]
#     center_x, center_y = w // 2, h // 2
#     x1, y1 = center_x - crop_size // 2, center_y - crop_size // 2
#     x2, y2 = center_x + crop_size // 2, center_y + crop_size // 2
#     central_region = image[y1:y2, x1:x2]
    
#     # Show the cropped central region
#     plt.imshow(central_region, cmap='gray')
#     plt.title("Central Region")
#     plt.show()


# image_path = r"D:\corneal_pachymetry\corneal_pachymetry\Pachymetry  report - Copy.jpeg"
# show_central_region(image_path, crop_size=50)


import cv2
import numpy as np
from sklearn.neighbors import KNeighborsClassifier

def map_color_to_thickness(color_map, thickness_values):
    # Train a KNN model to map RGB colors to thickness values
    knn = KNeighborsClassifier(n_neighbors=3)  # Use k=3 for better generalization
    normalized_colors = np.array(color_map) / 255.0  # Normalize RGB values
    knn.fit(normalized_colors, thickness_values)
    return knn

def approximate_cct_with_color(image_path, crop_size=50):
    # Load the image in RGB
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"Image not found: {image_path}")
    
    # Get image dimensions
    h, w = image.shape[:2]

    # Calculate crop coordinates for the center
    center_x, center_y = w // 2, h // 2
    x1, y1 = center_x - crop_size // 2, center_y - crop_size // 2
    x2, y2 = center_x + crop_size // 2, center_y + crop_size // 2

    # Crop the central region
    central_region = image[y1:y2, x1:x2]

    # Flatten the central region for color mapping
    central_pixels = central_region.reshape(-1, 3) / 255.0  # Normalize RGB values

    # Predict thickness for each pixel using the color-to-thickness model
    predicted_thickness = knn_model.predict(central_pixels)

    # Use the median thickness value to reduce outliers
    median_thickness = np.median(predicted_thickness)
    return median_thickness


# Define the color-to-thickness mapping from the legend
color_map = [
    [0, 0, 255],  # Blue
    [0, 255, 255],  # Cyan
    [0, 255, 0],  # Green
    [255, 255, 0],  # Yellow
    [255, 0, 0]  # Red
]
thickness_values = [40, 45, 50, 55, 60]  # Corresponding thickness values in micrometers

# Train the KNN model
knn_model = map_color_to_thickness(color_map, thickness_values)

# Estimate CCT using the updated approach
image_path = "D:\corneal_pachymetry\corneal_pachymetry\Pachymetry  report - Copy.jpeg"
try:
    cct_value = approximate_cct_with_color(image_path, crop_size=50)
    print(f"Approximated Central Corneal Thickness (CCT): {cct_value:.2f} µm")
except FileNotFoundError as e:
    print(e)
