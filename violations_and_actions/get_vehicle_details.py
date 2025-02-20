import streamlit as st
import requests
import json
def read_vehicle_number_from_file():
    try:
        with open('ocr_result.txt', 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        return ""

# Function to get vehicle owner details from the API
def get_vehicle_details(vehicle_number):
    url = 'https://rto-vehicle-information-verification-india.p.rapidapi.com/api/v1/rc/vehicleinfo'
    headers = {
        'content-type': 'application/json',
        'X-RapidAPI-Key': '8a9220d8edmsh92b05eceef83bb1p18d0d7jsnf203ba559be0',
        'X-RapidAPI-Host': 'rto-vehicle-information-verification-india.p.rapidapi.com'
    }
    data = {
        'reg_no': vehicle_number,
        'consent': 'Y',
        'consent_text': 'I hereby declare my consent agreement for fetching my information via AITAN Labs API'
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response.json()

# Function to display challan report
def display_challan_report(details):
    st.markdown("### Challan Report")
    for key, value in details.items():
        st.text(f"{key}: {value}")

# Streamlit app for Challan Report
st.title("Vehicle Challan Report Generator")
# Pre-populated vehicle number
default_vehicle_number = read_vehicle_number_from_file()
vehicle_number = st.text_input("Enter Vehicle Number", value=default_vehicle_number)
generate_button = st.button("Generate Challan Report")

if generate_button and vehicle_number:
    try:
        vehicle_details = get_vehicle_details(vehicle_number)
        if vehicle_details["status"] == "success":
            display_challan_report(vehicle_details["result"])
            st.header('CHALLAN AMOUNT')
            st.subheader("RS 2000/-")
        else:
            st.error("Vehicle not found or error in fetching details.")
    except Exception as e:
        st.error(f"An error occurred: {e}")
