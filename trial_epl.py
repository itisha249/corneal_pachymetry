# import cv2
# import numpy as np
# from scipy.stats import trim_mean

# def process_color_bar(image_path):
#     # Load the color bar image
#     image = cv2.imread(image_path)
#     if image is None:
#         raise FileNotFoundError(f"Image not found: {image_path}")

#     # Crop the color bar region
#     color_bar = image[10:290, 5:25]
    
#     # Convert to HSV
#     hsv_bar = cv2.cvtColor(color_bar, cv2.COLOR_BGR2HSV)

#     # Hue-to-thickness mapping
#     hue_to_thickness_mapping = [
#         (120, 40),  # Blue region: 40 μm
#         (95, 48),   # Green region: 48 μm (adjusted for this image)
#         (50, 55),   # Yellow region: 55 μm
#         (10, 60)    # Red region: 60 μm
#     ]

#     # Function to map Hue to thickness
#     def hue_to_thickness(hue):
#         for i in range(len(hue_to_thickness_mapping) - 1):
#             h1, t1 = hue_to_thickness_mapping[i]
#             h2, t2 = hue_to_thickness_mapping[i + 1]
#             if h1 >= hue >= h2:
#                 return t1 + (t2 - t1) * (hue - h1) / (h2 - h1)
#         return 0  # Return 0 if Hue is out of range

#     return hue_to_thickness

# def extract_central_cct(image_path, hue_to_thickness_func):
#     # Load the pachymetry map image
#     image = cv2.imread(image_path)
#     if image is None:
#         raise FileNotFoundError(f"Image not found: {image_path}")

#     # Convert to HSV and apply Gaussian blur
#     hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
#     hsv_image_blurred = cv2.GaussianBlur(hsv_image, (5, 5), 0)

#     # Extract the central region and display it resized
#     #central_region = hsv_image_blurred[145:155, 145:155]
#     central_region = hsv_image_blurred[145:155, 145:155]
#     #resized_region = cv2.resize(central_region, (300, 300), interpolation=cv2.INTER_LINEAR)
#     #cv2.imshow("Central Region", resized_region)
#     #cv2.waitKey(0)
#     #cv2.destroyAllWindows()

#     # Extract Hue values from the central region
#     central_hue_values = central_region[:, :, 0]

#     # Compute trimmed mean of the Hue values
#     trimmed_hue = trim_mean(central_hue_values.flatten(), 0.05)

#     # Map the trimmed Hue to thickness
#     cct = hue_to_thickness_func(trimmed_hue)

#     # Apply a fine-tuning offset
#     cct = cct - 2.5  # Adjust offset to improve accuracy

#     return cct

# # Example usage
# color_bar_path = "D:\\corneal_pachymetry\\corneal_pachymetry\\color_2.jpeg"
# map_image_path = "D:\\corneal_pachymetry\\corneal_pachymetry\\epl2.jpeg"

# try:
#     # Process the color bar to create the Hue-to-Thickness mapping function
#     hue_to_thickness = process_color_bar(color_bar_path)

#     # Use the mapping function to calculate the CCT from the pachymetry map
#     cct_value = extract_central_cct(map_image_path, hue_to_thickness)
#     print(f"Central Corneal Thickness (CCT): {cct_value:.2f} μm")
# except FileNotFoundError as e:
#     print(e)



import cv2
import numpy as np
from scipy.stats import trim_mean

def extract_of_epithelialreport_central_cct_from_image(image):
    """
    Extracts the Central Corneal Thickness (CCT) from the central region of the given cropped pachymetry map image.

    Parameters:
        image (numpy.ndarray): Cropped epithelial or pachymetry map image.
        
    Returns:
        float: Calculated CCT value.
    """
    if image is None:
        raise ValueError("Input image is None. Please provide a valid image.")

    # Predefined hue-to-thickness mapping
    hue_to_thickness_mapping = [
        (120, 40),  # Blue region: 40 μm
        (95, 48),   # Green region: 48 μm
        (50, 55),   # Yellow region: 55 μm
        (10, 60)    # Red region: 60 μm
    ]

    # Function to map Hue to thickness
    def hue_to_thickness(hue):
        for i in range(len(hue_to_thickness_mapping) - 1):
            h1, t1 = hue_to_thickness_mapping[i]
            h2, t2 = hue_to_thickness_mapping[i + 1]
            if h1 >= hue >= h2:
                # Interpolate between two thicknesses
                return t1 + (t2 - t1) * (hue - h1) / (h2 - h1)
        return 0  # Return 0 if Hue is out of range

    # Convert the image to HSV and apply Gaussian blur
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    hsv_image_blurred = cv2.GaussianBlur(hsv_image, (5, 5), 0)

    # Extract the central region (coordinates may need adjustment)
    central_region = hsv_image_blurred[145:155, 145:155]

    if central_region.size == 0:
        raise ValueError("Central region is empty. Check the cropping coordinates.")

    # Extract Hue values from the central region
    central_hue_values = central_region[:, :, 0]

    # Compute trimmed mean of the Hue values
    trimmed_hue = trim_mean(central_hue_values.flatten(), 0.05)

    # Map the trimmed Hue to thickness
    cct = hue_to_thickness(trimmed_hue)

    # Apply a fine-tuning offset
    cct = cct - 2.5  # Adjust offset if needed

    return cct


crop_epithial_od = cv2.imread("D:\corneal_pachymetry\corneal_pachymetry\images\epl-1.jpeg")
cct_value = extract_of_epithelialreport_central_cct_from_image(crop_epithial_od)
print(f"Central Corneal Thickness (CCT): {cct_value:.2f} μm")