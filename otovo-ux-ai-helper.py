import streamlit as st
import os
import requests
import base64
    
# Function to encode the image
def to_base64(uploaded_file):
    file_buffer = uploaded_file.read()
    b64 = base64.b64encode(file_buffer).decode()
    return f"data:image/png;base64,{b64}"

# Path to your image
api_key = st.sidebar.text_input("OPENAI API Key", type="password")

st.title('Otovo UX AI Helper')

st.write('This is a tool to help you generate the right data for the Otovo UX AI model.')

uploaded_file = st.file_uploader("Upload an image", type="png")

if uploaded_file:
    if st.sidebar.button("Show image"):
        st.image(uploaded_file, caption='Uploaded Image.', use_column_width=True)

    base64_image = to_base64(uploaded_file)

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
        {
            "role": "system", 
            "content": f"""
            You are a UX designer for a solar panel company 
            selling panels online to middle-aged European 
            customers. Analyse this UI sketch for selecting 
            hardware and suggest UI changes on the desktop. 
            The desired outcome is UI with a clear comparison 
            of products and clear interaction. Keep to the 
            same brand language.
            """,
            "role": "user",
            "content": [
            {
                "type": "text",
                "text": f"""
                
                """
            },
            {
                "type": "image_url",
                "image_url": {
                "url": base64_image
                }
            }
            ]
        }
        ],
        "max_tokens": 2500
    }
    st.write(payload)
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    output = response.json()
    output_text = output['choices'][0]['message']['content']
    
    st.write("AI Output:")
    st.write(output_text)
    