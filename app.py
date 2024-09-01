import streamlit as st
from PIL import Image
from pathlib import Path
import google.generativeai as genai
import os
import io
import re

# Configure Google Gemini API with the API key
API_KEY = 'AIzaSyBhDvhO1z_j-977fOuRJixhqLqnG4yyCsc'
genai.configure(api_key=API_KEY)

# Setup the model
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

# Setting page configuration
st.set_page_config(page_title="Image Analysists Med", page_icon=":robot:")

# Set logo
st.image("doctor_img.png", width=200)

# Set title and subtitle
st.title("This is an AI Doctor of Nepal🧑‍⚕️")
st.subheader("This is a web app made to assist village people with medical diagnosis")

# Provide user with options to choose between writing symptoms or uploading an image
option = st.selectbox(
    "How would you like to provide your symptoms?",
    ("Write Symptoms", "Upload an Image")
)

def extract_conditions(text):
    # Define a pattern to match common condition phrases
    pattern = re.compile(r'\b(common cold|allergies|sinusitis|flu|hay fever|other infections|irritants)\b', re.IGNORECASE)
    matches = pattern.findall(text)
    return ', '.join(set(matches))  # Remove duplicates and join the results

def analyze_symptoms(symptoms):
    try:
        # Refine the prompt for clarity
        prompt = f"Based on the following symptoms, what are the possible medical conditions? I am using this for my own chatbot please give short response Symptoms: {symptoms}"
        response = model.generate_content(prompt)
        result = response.text
        
        # Print the raw result for debugging
        st.write(f"Raw API Response: {result}")
        
        # Extract conditions
        conditions = extract_conditions(result)
        
        # Limit response to one paragraph and add warning
        if conditions:
            result = f"Based on your symptoms, the AI suggests the following conditions: {conditions}."
        else:
            result = "No specific conditions could be identified based on the symptoms provided."
        
        result += "\n\n**For further inquiry, find a doctor by clicking the button below.**"
        return result
    except Exception as e:
        return f"Error: {e}"

def analyze_image(image):
    try:
        # Convert the image to bytes for processing
        image_bytes = io.BytesIO()
        image.save(image_bytes, format=image.format)
        image_bytes = image_bytes.getvalue()

        # Call Google Gemini for image analysis
        response = model.generate_content("Summarize the possible conditions based on the image. I am using this for my own chatbot please give short response")
        result = response.text
        
        # Print the raw result for debugging
        st.write(f"Raw API Response: {result}")
        
        # Extract conditions
        conditions = extract_conditions(result)
        
        # Limit response to one paragraph and add warning
        if conditions:
            result = f"Based on the image, the AI suggests the following conditions: {conditions}."
        else:
            result = "No specific conditions could be identified based on the image provided."
        
        result += "\n\n**For further inquiry, find a doctor by clicking the button below.**"
        return result
    except Exception as e:
        return f"Error: {e}"

if option == "Write Symptoms":
    # Text input for symptoms
    symptoms = st.text_area("Enter your symptoms:", placeholder="Describe your symptoms here...")

    if st.button("Analyze Symptoms"):
        if symptoms:
            result = analyze_symptoms(symptoms)
            st.write("AI Analysis Results:")
            st.write(result)
            st.button("Find a Doctor", on_click=lambda: st.write("[Find a Doctor](https://www.google.com/maps/search/doctors+near+me)"))
        else:
            st.error("Please enter your symptoms for analysis.")

elif option == "Upload an Image":
    # File uploader for image
    uploaded_file = st.file_uploader("Upload an image showing symptoms", type=["jpg", "png", "jpeg"])

    if st.button("Analyze Image"):
        if uploaded_file is not None:
            # Display the uploaded image
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", use_column_width=True)
            
            # Analyze the image
            result = analyze_image(image)
            st.success(result)
            st.button("Find a Doctor", on_click=lambda: st.write("[Find a Doctor](https://www.google.com/maps/search/doctors+near+me)"))
        else:
            st.error("Please upload an image for analysis.")

# Developer Section
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; font-size: 18px;">
        <h4 style="color: #6c63ff;">Meet the Developer: Peshal Parajuli</h4>
        <p style="font-style: italic;">"Technology should serve humanity, and every project is an opportunity to make lives better."</p>
        <p>Follow the journey, reach out for collaborations, or simply say hello at: <a href="mailto:peshalparajuli2006@gmail.com" style="color: #FF6F61;">peshalparajuli2006@gmail.com</a></p>
    </div>
    """,
    unsafe_allow_html=True
)
