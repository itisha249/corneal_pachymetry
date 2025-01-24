import cv2
import numpy as np
import streamlit as st

def extract_cct(image):
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

# Streamlit app
st.title("Central Corneal Thickness (CCT) Calculator")

uploaded_file = st.file_uploader("Upload Pachymetry Map Image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    if image is None:
        st.error("Failed to read the uploaded image. Please try again.")
    else:
        st.image(image, caption="Uploaded Pachymetry Map", use_column_width=True)

        try:
            cct_value = extract_cct(image)
            st.success(f"Central Corneal Thickness (CCT): {cct_value:.2f} μm")
        except Exception as e:
            st.error(f"Error: {e}")
