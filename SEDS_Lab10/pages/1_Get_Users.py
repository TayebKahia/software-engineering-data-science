import streamlit as st
import requests

BASE_URL = "http://localhost:8000"

st.title("Get Users")


def send_request():
    try:
        response = requests.get(
            f"{BASE_URL}/users/", params={"skip": skip, "limit": limit})
        if response.status_code == 200:
            st.json(response.json())
        else:
            st.error(f"Error: {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        st.error(f"Request failed: {e}")


skip = st.number_input("Skip", min_value=0, value=0)
limit = st.number_input("Limit", min_value=1, value=10)

if st.button("Send Request"):
    send_request()
