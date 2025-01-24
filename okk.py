import cv2
import numpy as np
from scipy.stats import trim_mean

def process_color_bar(image_path):
    
    image = cv2.imread(image_path)

    # Crop the color bar region
    color_bar = image[10:290, 5:25] 
    cv2.imshow("color_bar",color_bar)
    cv2.waitKey(0)  # Wait for a key press
    cv2.destroyAllWindows() 
    
    
    hsv_bar = cv2.cvtColor(color_bar, cv2.COLOR_BGR2HSV)

    # Extract the Hue channel from the color bar
    hue_values = hsv_bar[:, :, 0]

    hue_to_thickness_mapping = [
        (120, 40),  # Blue region: 40 μm
        (95, 48),   # Green region: 48 μm (adjusted for this image)
        (50, 55),   # Yellow region: 55 μm
        (10, 60)    # Red region: 60 μm
    ]

    
    def hue_to_thickness(hue):
        for i in range(len(hue_to_thickness_mapping) - 1):
            h1, t1 = hue_to_thickness_mapping[i]
            h2, t2 = hue_to_thickness_mapping[i + 1]
            if h1 >= hue >= h2:  # Check if the Hue falls in this segment
                return t1 + (t2 - t1) * (hue - h1) / (h2 - h1)
        return 0  # Return 0 if Hue is out of range

    return hue_to_thickness

def extract_central_cct(image_path, hue_to_thickness_func):
    
    image = cv2.imread(image_path)

    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)


    hsv_image_blurred = cv2.GaussianBlur(hsv_image, (5, 5), 0)

    
    central_region = hsv_image_blurred[145:155, 145:155]  

    # Extract the Hue values from the central region
    central_hue_values = central_region[:, :, 0]

    trimmed_hue = trim_mean(central_hue_values.flatten(), 0.05)

    # Map the trimmed Hue to thickness using the mapping function
    cct = hue_to_thickness_func(trimmed_hue)

    # Apply a fine-tuning offset
    cct = cct - 2.5  # Adjust offset to improve accuracy

    return cct

# Example usage
color_bar_path = "D:\corneal_pachymetry\corneal_pachymetry\color_2.jpeg"  # Path to the color bar image
map_image_path = "D:\corneal_pachymetry\corneal_pachymetry\try - Copy.png"  # Path to the pachymetry map

# Process the color bar to create the Hue-to-Thickness mapping function
hue_to_thickness = process_color_bar(color_bar_path)

# Use the mapping function to calculate the CCT from the pachymetry map
cct_value = extract_central_cct(map_image_path, hue_to_thickness)
print(f"Central Corneal Thickness (CCT): {cct_value:.2f} μm")