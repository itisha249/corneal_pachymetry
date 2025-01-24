import cv2
import numpy as np

def extract_cct_from_colorbar(image_path):

    image = cv2.imread(image_path)

    if image is None:
        raise FileNotFoundError(f"Image not found at path: {image_path}")


    print(f"Loaded image shape: {image.shape}")

    # Crop the color bar region
    color_bar = image[50:200, 20:50] 

    
    if color_bar.size == 0:
        raise ValueError("Color bar region is empty. Check the cropping coordinates.")

    hsv_bar = cv2.cvtColor(color_bar, cv2.COLOR_BGR2HSV)

    hue_values = hsv_bar[:, :, 0]

    # Get the min and max hue from the color bar
    min_hue = np.min(hue_values)
    max_hue = np.max(hue_values)

    # Define the thickness range based on the color bar
    min_thickness = 300  # Minimum value (blue region)
    max_thickness = 710  # Maximum value (red region)

    # Crop the central region of the pachymetry map
    central_region = image[90:205, 90:150]
    cv2.imshow("central_re",central_region)
    cv2.waitKey(0)  # Wait for a key press
    cv2.destroyAllWindows()   # Adjust coordinates for your image

    
    if central_region.size == 0:
        raise ValueError("Central region is empty. Check the cropping coordinates.")

   
    central_hsv = cv2.cvtColor(central_region, cv2.COLOR_BGR2HSV)

    
    central_hue = np.mean(central_hsv[:, :, 0])

    
    print(f"Min Hue: {min_hue}, Max Hue: {max_hue}")
    print(f"Central Hue: {central_hue}")

    
    cct = min_thickness + (central_hue - min_hue) / (max_hue - min_hue) * (max_thickness - min_thickness)

    return cct

# Example usage
image_path = r"D:\corneal_pachymetry\corneal_pachymetry\images\pac_od.jpeg"
cct_value = extract_cct_from_colorbar(image_path)
print(f"Central Corneal Thickness (CCT): {cct_value:.2f} μm")
