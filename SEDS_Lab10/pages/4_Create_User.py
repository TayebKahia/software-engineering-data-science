import streamlit as st
import requests

BASE_URL = "http://localhost:8000"

st.title("Create User")


def send_request():
    try:
        response = requests.post(
            f"{BASE_URL}/users/new", json={"email": email, "name": name})
        if response.status_code in [200, 201]:
            st.json(response.json())
        else:
            st.error(f"Error: {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        st.error(f"Request failed: {e}")


email = st.text_input("Email")
name = st.text_input("Name")

if st.button("Send Request"):
    send_request()
