from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai
from PIL import Image


load_dotenv()  # Loading all the environment variables from .env
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

# input -> This is what I want the bot assistant to do
# image -> Invoice input image
# prompt -> Getting details of the image input


def get_gemini_response(input, image, prompt):
    # Function to load gemini pro vision model
    model = genai.GenerativeModel("gemini-pro-vision")
    response = model.generate_content([input, image[0], prompt])
    return response.text


def input_image_details(uploaded_file):
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the mime type of the uploaded image
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")


st.set_page_config("Gemini Application")
st.header("MultiLanguage Invoice Extractor")
input = st.text_input("Input Prompt:", key='input')
uploaded_file = st.file_uploader(
    "Upload the Invoice image...", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

submit = st.button("Tell me about the invoice")

input_prompt = """
You are an expert in understanding invoices. We will upload images as invoices and you have to answer any questions based on the uploaded invoice image.
"""

if submit:
    image_data = input_image_details(uploaded_file)
    response = get_gemini_response(input_prompt, image_data, input)
    st.subheader("Generated Response ->")
    st.write(response)
