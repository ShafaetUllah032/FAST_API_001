# streamlit_app.py
import streamlit as st
import requests

st.set_page_config(page_title="User Profile Input", layout="centered")

st.title("🧾 Personal Profile Form")

st.markdown("Please fill in the details below to generate your health and lifestyle insights:")

# Define FastAPI URL
FASTAPI_URL = "http://127.0.0.1:8000"

# Input fields
age = st.number_input("Age", min_value=0, max_value=120, value=34)
height = st.number_input("Height (in meters)", min_value=0.5, max_value=2.5, value=1.5, step=0.01)
weight = st.number_input("Weight (in kg)", min_value=20, max_value=200, value=85)
income_lpa = st.number_input("Annual Income (in LPA)", min_value=0.0, value=15.543, step=0.001)
smoker = st.checkbox("Smoker", value=True)
city = st.text_input("City", value="Mumbai")
occupation = st.selectbox("occupation",
                          ['retired', 'unemployed', 'government_job', 'student', 'freelancer', 'business_owner', 'private_job'], index=3)

# Submit button
if st.button("Submit"):
    # Create a dictionary with the form data
    profile_data = {
        "age": age,
        "height": height,
        "weight": weight,
        "income_lpa": income_lpa,
        "smoker": smoker,
        "city": city,
        "occupation": occupation
    }

    try:
        # Send a POST request to the FastAPI endpoint
        response = requests.post(f"{FASTAPI_URL}/predict", json=profile_data)
        print(profile_data)
        response.raise_for_status() # Raise an error for bad status codes

        # Check for a successful response
        if response.status_code == 200:
            result = response.json()
            st.success(result)
            st.write("### Summary:")
            st.write(f"- **Age:** {result['data']['age']}")
            st.write(f"- **Height:** {result['data']['height']} m")
            st.write(f"- **Weight:** {result['data']['weight']} kg")
            st.write(f"- **Income:** ₹{result['data']['income_lpa']} LPA")
            st.write(f"- **Smoker:** {'Yes' if result['data']['smoker'] else 'No'}")
            st.write(f"- **City:** {result['data']['city']}")
            st.write(f"- **Occupation:** {result['data']['occupation']}")
        else:
            st.error(f"Error from FastAPI: {response.status_code}")
            st.write(response.json())

    except requests.exceptions.RequestException as e:
        st.error(f"Could not connect to FastAPI server. Please ensure it is running: {e}")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")

# A simple GET request to test connection
if st.button("Test API Connection"):
    try:
        response = requests.get(FASTAPI_URL)
        if response.status_code == 200:
            st.info(f"Connected to FastAPI! Message: {response.json().get('message')}")
        else:
            st.warning(f"Connection failed with status code {response.status_code}")
    except requests.exceptions.RequestException:
        st.error("Connection failed. Is the FastAPI server running?")
