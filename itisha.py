# import cv2
# import numpy as np

# def extract_cct(image_path):
#     # Load the image
#     image = cv2.imread(image_path)
    
#     # Resize for consistent processing
#     image = cv2.resize(image, (512, 512))
    
#     # Convert to HSV for better color segmentation
#     hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
#     # Define thresholds for colors (adjust as per your images)
#     blue_lower = np.array([100, 50, 50])
#     blue_upper = np.array([140, 255, 255])
    
#     # Create a mask for blue (thinner areas)
#     blue_mask = cv2.inRange(hsv_image, blue_lower, blue_upper)
    
#     # Detect the center of the cornea
#     h, w = blue_mask.shape
#     center_x, center_y = w // 2, h // 2
    
#     # Extract the central zone (small radius around center)
#     radius = 30
#     mask = np.zeros_like(blue_mask)
#     cv2.circle(mask, (center_x, center_y), radius, 255, -1)
#     central_zone = cv2.bitwise_and(blue_mask, mask)
    
#     # Calculate the average thickness value (mock conversion for example)
#     thickness_values = central_zone[central_zone > 0]
#     if len(thickness_values) > 0:
#         average_thickness = np.mean(thickness_values)
#     else:
#         average_thickness = 0

#     # Simulate a color-to-thickness conversion
#     cct = 500 + (average_thickness / 255) * 50  # Example formula
#     #cct = (average_thickness / 255) * 50  # Example formula
    
#     return cct

# # Example usage
# image_path = "D:\corneal_pachymetry\corneal_pachymetry\Pachymetry  report - Copy.jpeg"  # Replace with your file path
# cct_value = extract_cct(image_path)
# print(f"Central Corneal Thickness (CCT): {cct_value:.2f} μm")


import cv2
import numpy as np

def extract_cct_from_colorbar(image_path):
    # Load the report image
    image = cv2.imread(image_path)

    # Check if the image was loaded successfully
    if image is None:
        raise FileNotFoundError(f"Image not found at path: {image_path}")

    # Debug: Print image dimensions
    print(f"Loaded image shape: {image.shape}")

    # Crop the color bar region
    color_bar = image[50:200, 20:50] 
    # Adjust coordinates for your image

    # Check if the color bar region is empty
    if color_bar.size == 0:
        raise ValueError("Color bar region is empty. Check the cropping coordinates.")

    # Convert the color bar to HSV
    hsv_bar = cv2.cvtColor(color_bar, cv2.COLOR_BGR2HSV)

    # Extract the Hue channel from the color bar
    hue_values = hsv_bar[:, :, 0]

    # Get the min and max hue from the color bar
    min_hue = np.min(hue_values)
    max_hue = np.max(hue_values)

    # Define the thickness range based on the color bar
    min_thickness = 300  # Minimum value (blue region)
    max_thickness = 710  # Maximum value (red region)

    # Crop the central region of the pachymetry map
    central_region = image[90:150, 95:150]
    cv2.imshow("central_re",central_region)
    cv2.waitKey(0)  # Wait for a key press
    cv2.destroyAllWindows()   # Adjust coordinates for your image

    # Check if the central region is empty
    if central_region.size == 0:
        raise ValueError("Central region is empty. Check the cropping coordinates.")

    # Convert the central region to HSV
    central_hsv = cv2.cvtColor(central_region, cv2.COLOR_BGR2HSV)

    # Calculate the average hue in the central region
    central_hue = np.mean(central_hsv[:, :, 0])

    # Debug: Print hues and thickness ranges
    print(f"Min Hue: {min_hue}, Max Hue: {max_hue}")
    print(f"Central Hue: {central_hue}")

    # Map the central hue to thickness using linear interpolation
    cct = min_thickness + (central_hue - min_hue) / (max_hue - min_hue) * (max_thickness - min_thickness)

    return cct

# Example usage
image_path = r"D:\corneal_pachymetry\corneal_pachymetry\pac_od.jpeg"
cct_value = extract_cct_from_colorbar(image_path)
print(f"Central Corneal Thickness (CCT): {cct_value:.2f} μm")
