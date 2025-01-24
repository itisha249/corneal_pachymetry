import cv2
import numpy as np
from scipy.stats import trim_mean
import streamlit as st


def get_image(image_path):
    img = cv2.imread(image_path)
    return img


def find_graph(img):
    crop_pc_od = img[215:435, 75:325]
    crop_pc_od = cv2.resize(crop_pc_od, (240, 240))

    crop_pc_os = img[215:435, 410:670]
    crop_pc_os = cv2.resize(crop_pc_os, (240, 240))

    crop_epithial_od = img[510:770, 60:325]
    crop_epithial_od = cv2.resize(crop_epithial_od, (250, 250))

    crop_epithial_os = img[510:770, 410:670]
    crop_epithial_os = cv2.resize(crop_epithial_os, (280, 280))

    return crop_pc_od, crop_pc_os, crop_epithial_od, crop_epithial_os


def extract_cct_from_colorbar(image):
    if image is None:
        raise ValueError("Input image is None.")

    print(f"Loaded image shape: {image.shape}")

    # Crop the color bar region
    color_bar = image[50:200, 20:50]
    if color_bar.size == 0:
        raise ValueError("Color bar region is empty. Check the cropping coordinates.")

    hsv_bar = cv2.cvtColor(color_bar, cv2.COLOR_BGR2HSV)
    hue_values = hsv_bar[:, :, 0]

    min_hue = np.min(hue_values)
    max_hue = np.max(hue_values)

    min_thickness = 300
    max_thickness = 710

    # Crop the central region of the pachymetry map
    central_region = image[90:200, 90:150]
    if central_region.size == 0:
        raise ValueError("Central region is empty. Check the cropping coordinates.")

    central_hsv = cv2.cvtColor(central_region, cv2.COLOR_BGR2HSV)
    central_hue = np.mean(central_hsv[:, :, 0])

    print(f"Min Hue: {min_hue}, Max Hue: {max_hue}")
    print(f"Central Hue: {central_hue}")

    cct = min_thickness + (central_hue - min_hue) / (max_hue - min_hue) * (max_thickness - min_thickness)

    return cct


def extract_of_epithelialreport_central_cct_from_image(image):
    if image is None:
        raise ValueError("Input image is None. Please provide a valid image.")

    hue_to_thickness_mapping = [
        (120, 40),
        (95, 48),
        (50, 55),
        (10, 60)
    ]

    def hue_to_thickness(hue):
        for i in range(len(hue_to_thickness_mapping) - 1):
            h1, t1 = hue_to_thickness_mapping[i]
            h2, t2 = hue_to_thickness_mapping[i + 1]
            if h1 >= hue >= h2:
                return t1 + (t2 - t1) * (hue - h1) / (h2 - h1)
        return 0

    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    hsv_image_blurred = cv2.GaussianBlur(hsv_image, (5, 5), 0)

    central_region = hsv_image_blurred[145:155, 145:155]
    if central_region.size == 0:
        raise ValueError("Central region is empty. Check the cropping coordinates.")

    central_hue_values = central_region[:, :, 0]
    trimmed_hue = trim_mean(central_hue_values.flatten(), 0.05)

    cct = hue_to_thickness(trimmed_hue)
    cct = cct - 2.5

    return cct


# Streamlit App
st.title("Pachymetry Report Analyzer")
uploaded_file = st.file_uploader("Upload Pachymetry Report Image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    if img is None:
        st.error("Failed to read the uploaded image. Please upload a valid image.")
    else:
        st.image(img, caption="Uploaded Pachymetry Report", use_column_width=True)

        try:
            crop_pc_od, crop_pc_os, crop_epithial_od, crop_epithial_os = find_graph(img)

            cct_of_od = extract_cct_from_colorbar(crop_pc_od)
            cct_of_os = extract_cct_from_colorbar(crop_pc_os)
            cct_epithial_od = extract_of_epithelialreport_central_cct_from_image(crop_epithial_od)
            cct_epithial_os = extract_of_epithelialreport_central_cct_from_image(crop_epithial_os)

            st.success(f"Central Corneal Thickness (CCT) for OD: {cct_of_od:.2f} μm")
            st.success(f"Central Corneal Thickness (CCT) for OS: {cct_of_os:.2f} μm")
            st.success(f"Epithelial Thickness for OD: {cct_epithial_od:.2f} μm")
            st.success(f"Epithelial Thickness for OS: {cct_epithial_os:.2f} μm")
        except Exception as e:
            st.error(f"Error: {e}")


