# -*- coding: utf-8 -*-
"""App_Pan.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1HPyXy-zAcNVuSYiK9J3JlziLt5tB0R0B
"""


import streamlit as st
import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim

# Load and preprocess images
def preprocess_image(image):
    image = cv2.imdecode(np.frombuffer(image.read(), np.uint8), cv2.IMREAD_GRAYSCALE)
    image = cv2.resize(image, (400, 200))
    return image

# Compare two images using SSIM
def compare_images(image1, image2):
    score, diff = ssim(image1, image2, full=True)
    diff = (diff * 255).astype("uint8")
    return score, diff

# Detect fake PAN
def detect_fake_pan(diff):
    _, thresh = cv2.threshold(diff, 50, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return len(contours) > 10

# Streamlit UI
st.title("PAN Card Tampering Detection App")
st.write("Upload an original PAN card image and test images to check for tampering.")

# Upload Reference PAN Card
reference_file = st.file_uploader("Upload Original PAN Card", type=["png", "jpg", "jpeg"])
test_files = st.file_uploader("Upload Test PAN Cards", type=["png", "jpg", "jpeg"], accept_multiple_files=True)

if reference_file and test_files:
    reference_image = preprocess_image(reference_file)

    for test_file in test_files:
        test_image = preprocess_image(test_file)
        score, diff = compare_images(reference_image, test_image)
        is_fake = detect_fake_pan(diff)

        result = "✅ Valid PAN Card" if score > 0.75 and not is_fake else "❌ Fake PAN Card"
        reason = (
            "✅ High similarity score and minimal structural differences."
            if result == "✅ Valid PAN Card"
            else "❌ Major structural differences detected. Possible fake document."
        )

        st.image(test_file, caption=f"🖼 {test_file.name}", use_column_width=True)
        st.write(f"📊 **SSIM Score:** {score:.4f}")
        st.write(f"🔍 **Result:** {result}")
        st.write(f"📌 **Reason:** {reason}")
        st.write("---")

