import cv2 
import numpy as np
from scipy.stats import trim_mean


def get_image(image_path):
    img = cv2.imread(image_path)
    #img = cv2.resize(img,(500,500))

    return img

def find_graph(img):


    crop_pc_od =img[215:435, 75:325]
    crop_pc_od = cv2.resize(crop_pc_od,(240,240))

    crop_pc_os = img[215:435, 410:670]
    crop_pc_os = cv2.resize(crop_pc_os,(240,240))
    

    crop_epithial_od =img[510:770, 60:325]
    crop_epithial_od = cv2.resize(crop_epithial_od,(250,250))
    
    crop_epithial_os =img[510:770, 410:670]
    crop_epithial_os = cv2.resize(crop_epithial_os,(280,280))
   

    return crop_pc_od,crop_pc_os,crop_epithial_od,crop_epithial_os


def extract_cct_from_colorbar(image):

    #image = cv2.imread(image_path)

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
    max_thickness = 710 #710  # Maximum value (red region)

    # Crop the central region of the pachymetry map
    central_region = image[90:200, 90:150]
    # cv2.imshow("central_re",central_region)
    # cv2.waitKey(0)  # Wait for a key press
    # cv2.destroyAllWindows()   # Adjust coordinates for your image

    
    if central_region.size == 0:
        raise ValueError("Central region is empty. Check the cropping coordinates.")

   
    central_hsv = cv2.cvtColor(central_region, cv2.COLOR_BGR2HSV)

    
    central_hue = np.mean(central_hsv[:, :, 0])

    
    print(f"Min Hue: {min_hue}, Max Hue: {max_hue}")
    print(f"Central Hue: {central_hue}")

    
    cct = min_thickness + (central_hue - min_hue) / (max_hue - min_hue) * (max_thickness - min_thickness)

    return cct



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


img = get_image(r"D:\corneal_pachymetry\corneal_pachymetry\images\Pachymetry  report.jpeg")

crop_pc_od,crop_pc_os,crop_epithial_od,crop_epithial_os=find_graph(img)
cct_of_od = extract_cct_from_colorbar(crop_pc_od)
cct_of_os = extract_cct_from_colorbar(crop_pc_os)
cct_epithial_od = extract_of_epithelialreport_central_cct_from_image(crop_epithial_od)
cct_epithial_os = extract_of_epithelialreport_central_cct_from_image(crop_epithial_os)
print(f"Central Corneal Thickness (CCT): {cct_of_od:.2f} μm")
print(f"Central Corneal Thickness (CCT): {cct_of_os:.2f} μm")
print(f"Central Corneal Thickness (CCT): {cct_epithial_od:.2f} μm")
print(f"Central Corneal Thickness (CCT): {cct_epithial_os:.2f} μm")
