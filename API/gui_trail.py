import tkinter as tk
from tkinter import filedialog, Label
from PIL import Image, ImageTk
import cv2
import numpy as np
from tensorflow.keras.models import load_model

# Load the trained model
MODEL_PATH = "D:\corneal_pachymetry\corneal_pachymetry\central_corneal_thickness_model.h5"  # Replace with your model's path
model = load_model(MODEL_PATH)

# Function to preprocess the image
def preprocess_image(image_path, target_size=(256, 256)):
    """ Preprocess corneal pachymetry images for input to the model """
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"Image not found at path: {image_path}")
    image = cv2.resize(image, target_size)
    image = image / 255.0
    return np.expand_dims(image, axis=0)  # Add batch dimension

# GUI Application
class CCTApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Central Corneal Thickness Prediction")
        self.image_path = None

        # Title Label
        self.title_label = Label(root, text="Central Corneal Thickness Prediction", font=("Arial", 16))
        self.title_label.pack(pady=10)

        # Image Display Area
        self.image_label = Label(root, text="No Image Selected", font=("Arial", 12), width=50, height=15)
        self.image_label.pack(pady=10)

        # Upload Button
        self.upload_button = tk.Button(root, text="Upload Image", command=self.upload_image, width=20)
        self.upload_button.pack(pady=5)

        # Predict Button
        self.predict_button = tk.Button(root, text="Predict Thickness", command=self.predict_thickness, width=20)
        self.predict_button.pack(pady=5)

        # Result Label
        self.result_label = Label(root, text="", font=("Arial", 14))
        self.result_label.pack(pady=10)

    def upload_image(self):
        """ Function to upload and display the image """
        self.image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.png;*.jpeg")])
        if self.image_path:
            # Load and display the image
            img = Image.open(self.image_path)
            img = img.resize((256, 256))  # Resize for display
            img = ImageTk.PhotoImage(img)
            self.image_label.configure(image=img, text="")
            self.image_label.image = img

    def predict_thickness(self):
        """ Function to predict the central corneal thickness """
        if not self.image_path:
            self.result_label.config(text="Please upload an image first!", fg="red")
            return

        try:
            # Preprocess the image
            preprocessed_image = preprocess_image(self.image_path)

            # Predict using the model
            prediction = model.predict(preprocessed_image)
            cct_value = prediction[0][0]

            # Display the result
            self.result_label.config(text=f"Predicted Central Corneal Thickness: {cct_value:.2f} µm", fg="green")
        except Exception as e:
            self.result_label.config(text=f"Error: {str(e)}", fg="red")


# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = CCTApp(root)
    root.mainloop()
