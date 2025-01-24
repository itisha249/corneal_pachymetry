import cv2
import numpy as np
import streamlit as st
from PIL import Image
import tempfile

def extract_cct_from_epithelial(image):
    def get_hue_range_from_color_bar():
        # Define the hue range based on the color bar
        min_hue = 120  # Hue corresponding to 40 µm (blue region)
        max_hue = 10   # Hue corresponding to 60 µm (red region)
        return min_hue, max_hue

    # Get dynamic hue range from the preloaded color bar
    min_hue, max_hue = get_hue_range_from_color_bar()

    # Define the thickness range based on the color bar
    min_thickness = 40  # Minimum thickness corresponding to min_hue
    max_thickness = 60  # Maximum thickness corresponding to max_hue

    # Crop the central region of the pachymetry map
    central_region = image[145:155, 145:155]  # Adjust coordinates for your image

    if central_region.size == 0:
        raise ValueError("Central region is empty. Check the cropping coordinates.")

    central_hsv = cv2.cvtColor(central_region, cv2.COLOR_BGR2HSV)

    central_hue = np.mean(central_hsv[:, :, 0])

    # Map the central hue to thickness
    cct = min_thickness + (central_hue - min_hue) / (max_hue - min_hue) * (max_thickness - min_thickness)

    return cct

def extract_cct_from_pachymetry(image_path):
    image = cv2.imread(image_path)

    if image is None:
        raise FileNotFoundError(f"Image not found at path: {image_path}")

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

    if central_region.size == 0:
        raise ValueError("Central region is empty. Check the cropping coordinates.")

    central_hsv = cv2.cvtColor(central_region, cv2.COLOR_BGR2HSV)
    central_hue = np.mean(central_hsv[:, :, 0])

    cct = min_thickness + (central_hue - min_hue) / (max_hue - min_hue) * (max_thickness - min_thickness)

    return cct

# Streamlit app
def main():
    st.title("Corneal Thickness Analysis")

    st.write("This app calculates the Central Corneal Thickness (CCT) from a given corneal map.")

    report_type = st.selectbox("Select the type of report:", ["Pachymetry Map", "Epithelial Map"])

    uploaded_file = st.file_uploader("Upload an image of the map:", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        try:
            # Convert uploaded file to OpenCV image
            file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
            image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

            if image is None:
                raise ValueError("Failed to decode the uploaded image. Please upload a valid image file.")

            st.image(image[:, :, ::-1], caption="Uploaded Image", use_column_width=True)  # Convert BGR to RGB for display

            if report_type == "Epithelial Map":
                cct_value = extract_cct_from_pachymetry(image)
            else:
                with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                    temp_file.write(uploaded_file.getvalue())
                    temp_file_path = temp_file.name
                cct_value = extract_cct_from_epithelial(temp_file_path)

            st.success(f"Central Corneal Thickness (CCT): {cct_value:.2f} μm")
        except Exception as e:
            st.error(f"Error: {e}")

if __name__ == "__main__":
    main()
