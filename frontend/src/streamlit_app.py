import os
import requests

import streamlit as st

BACKEND_HOST = os.getenv("BACKEND_HOST", "localhost")
BACKEND_HOST_PORT = os.getenv("BACKEND_HOST_PORT", "5000")
BACKEND_URL = f"http://{BACKEND_HOST}:{BACKEND_HOST_PORT}"

def get_data_from_backend():
    # Define the URL of the dummy route in the backend
    backend_url = f"{BACKEND_URL}/dummy"
    # Make a GET request to the backend to get the data
    response = requests.get(backend_url)
    if response.status_code == 200:
        data = response.text
        return data
    else:
        return None

def main():
    st.title("Dummy Streamlit App")

    # Add a button to trigger the data retrieval from the backend
    if st.button("Get Data"):
        data = get_data_from_backend()
        if data is not None:
            st.write("Data received from backend:")
            st.write(data)
        else:
            st.write("Failed to retrieve data from backend.")

if __name__ == "__main__":
    main()