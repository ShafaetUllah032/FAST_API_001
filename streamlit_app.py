import streamlit as st
import requests

# FastAPI endpoint (update if deployed)
FASTAPI_URL = "http://127.0.0.1:8000/predict"

st.set_page_config(page_title="Insurance Type Predictor", page_icon="🩺", layout="centered")

st.title("🩺 Insurance Type Prediction App")
st.write("Provide client details below to predict the type of insurance recommended.")

# ---- Input fields ----
age = st.number_input("Age of the client", min_value=1, max_value=112, value=30)
height = st.number_input("Height (in meters)", min_value=0.5, max_value=2.5, value=1.70, step=0.01)
weight = st.number_input("Weight (in kg)", min_value=1.0, max_value=250.0, value=70.0, step=0.1)
income_lpa = st.number_input("Income (in Lakh Per Annum)", min_value=0.1, value=6.0, step=0.1)

smoker = st.radio("Is the client a smoker?", ["Yes", "No"])
smoker_bool = True if smoker == "Yes" else False

city = st.text_input("City of the client", value="Dhaka")

occupation = st.selectbox(
    "Occupation",
    [
        "retired",
        "unemployed",
        "government_job",
        "student",
        "freelancer",
        "business_owner",
        "private_job",
    ],
)

# ---- Predict button ----
if st.button("🔮 Predict Insurance Type"):
    # Prepare request body
    data = {
        "age": age,
        "height": height,
        "weight": weight,
        "income_lpa": income_lpa,
        "smoker": smoker_bool,
        "city": city,
        "occupation": occupation,
    }

    st.write("Sending data to FastAPI backend...")
    try:
        response = requests.post(FASTAPI_URL, json=data)
        if response.status_code == 200:
            st.success(response.json())
        else:
            st.error(f"Error {response.status_code}: {response.text}")
    except requests.exceptions.RequestException as e:
        st.error(f"Request failed: {e}")

# ---- Extra info ----
st.markdown("---")
st.caption("Built with ❤️ using Streamlit + FastAPI")
