import pytesseract
from PIL import Image
import streamlit as st
import re

# Set Tesseract path (change this path according to your installation)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# OCR configuration for Hindi + English
custom_config = r'-l hin+eng --psm 6'

def ocr_image(image):
    # Extract text from the image
    text = pytesseract.image_to_string(image, config=custom_config)
    return text

def highlight_text(keyword, text):
    # Check if the keyword is in Hindi or English
    if any('\u0900' <= char <= '\u097F' for char in keyword):  # Hindi characters range
        # Highlight the Hindi keyword
        highlighted_text = re.sub(
            f"({re.escape(keyword)})", 
            r'<span style="background-color: yellow;">\1</span>', 
            text, 
            flags=re.IGNORECASE
        )
    else:
        # Highlight the English keyword
        highlighted_text = re.sub(
            f"({re.escape(keyword)})", 
            r'<span style="background-color: yellow;">\1</span>', 
            text, 
            flags=re.IGNORECASE
        )
    
    return highlighted_text

st.title("OCR Web App")
st.subheader("Upload an image containing text in Hindi or English")

# Image uploader
uploaded_image = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_image:
    # Open and display the image
    img = Image.open(uploaded_image)
    st.image(img, caption="Uploaded Image", use_column_width=True)
    
    with st.spinner("Extracting text..."):
        # Extract text using OCR
        extracted_text = ocr_image(img)
        st.write("### Extracted Text")
        st.write(extracted_text)

    st.subheader("Search within the extracted text")

    # Keyword input (supports English and Hindi search)
    keyword = st.text_input("Enter a keyword to search and highlight:")

    if keyword:
        # Highlight based on whether the keyword is Hindi or English
        highlighted_result = highlight_text(keyword, extracted_text)
        st.write("### Search Results")
        
        # Display the highlighted result
        st.markdown(highlighted_result, unsafe_allow_html=True)
