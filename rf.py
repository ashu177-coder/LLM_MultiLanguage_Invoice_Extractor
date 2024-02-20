from dotenv import load_dotenv
from PIL import Image
import os
import streamlit as st
import google.generativeai as genai

# Loading the env variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Gemini Function

# input -> Telling the assistant has to do, eg: Like to act as an invoice extractor
# image -> input invoice
# prompt -> Specifically asking questions on the uploaded invoice image


def get_gemini_response(input, image, prompt):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input, image[0], prompt])
    return response.text


def input_image_setup(uploaded_file):
    # This function will take the uploaded file, convert it into bytes and give all the information of the image in bytes
    if uploaded_file is not None:
        # Read the file into bytes:
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No File Uploaded")


# Setting up the streamlit page
st.set_page_config(page_title="LLM Application")
st.header("Multilanguage Invoice Extractor")
input = st.text_input("Input:", key='input')

# Uploading the image file
uploaded_file = st.file_uploader(
    "Choose an invoice image...", type=['jpg', 'png', 'jpeg'])
image = ""
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Invoice", use_column_width=True)

submit = st.button("Ask the question")

input_prompt = "You are an expert in understanding invoices. We will upload an image of invoice and you will have to answer any questions based on the uploaded invoice image."

if submit:
    image_data = input_image_setup(uploaded_file)
    response = get_gemini_response(input_prompt, image_data, input)
    st.subheader("The Response is -> ")
    st.write(response)
