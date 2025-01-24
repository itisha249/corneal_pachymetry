import streamlit as st
import cv2
import numpy as np
from PIL import Image
import tempfile

def extract_cct_from_colorbar(image_path):
    image = cv2.imread(image_path)

    if image is None:
        raise FileNotFoundError(f"Image not found at path: {image_path}")

    st.write(f"Loaded image shape: {image.shape}")

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

    # Display the central region
    st.image(cv2.cvtColor(central_region, cv2.COLOR_BGR2RGB), caption="Central Region")

    central_hsv = cv2.cvtColor(central_region, cv2.COLOR_BGR2HSV)
    central_hue = np.mean(central_hsv[:, :, 0])

    st.write(f"Min Hue: {min_hue}, Max Hue: {max_hue}")
    st.write(f"Central Hue: {central_hue}")

    cct = min_thickness + (central_hue - min_hue) / (max_hue - min_hue) * (max_thickness - min_thickness)

    return cct

# Streamlit app
def main():
    st.title("Pachymetry CCT Analysis")

    st.write("This app calculates the Central Corneal Thickness (CCT) from a given corneal pachymetry image.")

    uploaded_file = st.file_uploader("Upload an image of the corneal pachymetry map:", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(uploaded_file.read())
            temp_file_path = temp_file.name

        st.image(Image.open(uploaded_file), caption="Uploaded Image", use_column_width=True)

        try:
            cct_value = extract_cct_from_colorbar(temp_file_path)
            st.success(f"Central Corneal Thickness (CCT): {cct_value:.2f} μm")
        except Exception as e:
            st.error(f"Error: {e}")

if __name__ == "__main__":
    main()
