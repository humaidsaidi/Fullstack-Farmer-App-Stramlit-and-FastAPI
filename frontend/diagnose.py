import streamlit as st
import os
import requests
from PIL import Image
import login



upload_folder = "./frontend/images"
def diagnose():
    st.title("Diagnose Page")
    st.write("Upload your plant image below and diagnose it desease")

    uploaded_file = st.file_uploader("Choose an image", type=['jpg', 'jpeg', 'png'])

    if st.button("Upload the image"):   
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            img_path = os.path.join(upload_folder, uploaded_file.name)
            image.save(img_path)  # Save the uploaded image
            st.image(image, use_column_width=True)

            token = login.cookies["jwt-token"]
            headers = {"Authorization": f'Bearer {token}'}
            files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "image/jpeg")}  # "file" is the key
            res = requests.post("http://127.0.0.1:8000/diagnose/", files=files, headers=headers)
            os.remove(img_path)

            if res.status_code == 401:
                st.error('You should login to diagnose the plant!!', icon="🚨")

            if res.status_code == 200:
                # Parse the JSON response
                response_json = res.json()
                prediction = response_json["prediction"]
                st.write(f'## Your plant diagnosis is: {prediction}')

        else:
            st.error('You did not upload an image yet', icon="🚨")

    