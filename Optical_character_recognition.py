import streamlit as st
import cv2
import numpy as np
import easyocr
import streamlit as st
import os
import glob
import cv2
import numpy as np
from PIL import Image
import re
def save_text_to_file(text, file_name='ocr_result.txt'):
    with open(file_name, 'w') as file:
        file.write(text)
    return file_name
# Function to process image using EasyOCR and clean the text
def process_with_easyocr(image):
    reader = easyocr.Reader(['en'])
    results = reader.readtext(image)
    text = " ".join([result[1] for result in results])
    # Keep only alphanumeric characters, spaces and dashes
    cleaned_text = re.sub(r'[^A-Za-z0-9 -]', '', text)
    return cleaned_text
# Function to find the latest exp folder
def get_latest_exp_folder(base_path):
    exp_folders = glob.glob(os.path.join(base_path, "exp*"+'/license_plates'))
    latest_folder = max(exp_folders, key=os.path.getmtime, default=None)
    return latest_folder

# Function to load images from the latest exp folder, every 10th image
def load_images_from_folder(folder_path):
    st.write(folder_path)
    images = []
    for i, img_path in enumerate(sorted(glob.glob(os.path.join(folder_path, "*.jpg")), key=os.path.getmtime)):
        if i % 1 == 0:  # Select every 10th image
            img = cv2.imread(img_path)
            if img is not None:
                images.append(img)
            else:
                st.error(f"Failed to load image: {img_path}")
    return images

# Streamlit app
st.title("Traffic Management System")

# Path to the detect folder
detect_folder_path = "C:/Users/varunkumar.v/Desktop/Traffic Management/yolov5/runs/detect"

latest_exp_folder = get_latest_exp_folder(detect_folder_path)
if latest_exp_folder:
    images = load_images_from_folder(latest_exp_folder)
    if images:
        # Display images in a 3-column layout
        cols = st.columns(3)
        col_index = 0
        image_selection = {}

        for i, img in enumerate(images):
            # Convert OpenCV image to PIL format for Streamlit
            try:
                img_pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
            except Exception as e:
                st.error(f"Error converting image: {e}")
                continue

            # Display each image in a column
            with cols[col_index]:
                st.image(img_pil, caption=f"Image {i+1}", width=100)
                image_selection[f"Image {i+1}"] = img
            
            # Move to the next column
            col_index = (col_index + 1) % 3

        # Select the clearest image
        selected_image_name = st.selectbox("Select the clearest image", options=list(image_selection.keys()))
        selected_image = image_selection[selected_image_name]


    if st.button('Process Image'):
        with st.spinner('Processing with EasyOCR...'):
            easyocr_text = process_with_easyocr(selected_image)
            st.subheader("EasyOCR Results")
            st.write(easyocr_text)
             # Save the text to a file
            file_path = save_text_to_file(easyocr_text)
            # Provide a download link to the file
    if st.button('GENERATE CHALLAN'):
        import os
        os.system('streamlit run app2.py')
