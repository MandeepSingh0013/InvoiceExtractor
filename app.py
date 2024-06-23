from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
print("all set")

model=genai.GenerativeModel("gemini-pro-vision")

def get_gemini_response(input,image,promt):
    repsonse=model.generate_content([input,image[0],promt])
    return repsonse.text

def input_image_details(uploaded_file):
    if uploaded_file is not None:
        #Read the file into bytes
        bytes_data= uploaded_file.getvalue()
        image_parts=[
            {
                "mime_type":uploaded_file.type,
                "data":bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")
    

#Initializ our streamlit app
st.set_page_config(page_title="Multilanguage Invoice Extractor")
st.header("Gemini Application")
input=st.text_input("Input Promt:",key="input")
uploaded_file=st.file_uploader("Choose an image...",type=["jpg","jpeg","png"])
image=""
if uploaded_file is not None:
    image=Image.open(uploaded_file)
    st.image(image,caption="Uploaded Image.",use_column_width=True)

submit=st.button("Invoice Details")

input_promt="""
You are an expert in understanding invoices. We will upload a image 
as invoice and you will have to answer any qustions based on the uploaded
invoice image
"""

if submit:
    image_data=input_image_details(uploaded_file)
    response=get_gemini_response(input_promt,image_data,input)
    st.subheader("The Response is")
    st.write(response)