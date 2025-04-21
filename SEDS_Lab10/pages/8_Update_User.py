import streamlit as st
import requests

BASE_URL = "http://localhost:8000"

st.title("Update User")


def send_request():
    try:
        response = requests.put(
            f"{BASE_URL}/users/{user_id}", json={"name": name, "email": email})
        if response.status_code == 200:
            st.success("User successfully updated.")
            st.json(response.json())
        else:
            st.error(f"Error: {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        st.error(f"Request failed: {e}")


user_id = st.number_input("User ID", min_value=1, value=1)
name = st.text_input("New Name")
email = st.text_input("New Email")

if st.button("Send Request"):
    send_request()
