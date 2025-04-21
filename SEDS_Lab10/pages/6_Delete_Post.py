import streamlit as st
import requests

BASE_URL = "http://localhost:8000"

st.title("Delete Post")


def send_request():
    try:
        response = requests.delete(
            f"{BASE_URL}/users/{user_id}/delete_post/{post_id}")
        if response.status_code == 200:
            st.success("Post successfully deleted.")
        else:
            st.error(f"Error: {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        st.error(f"Request failed: {e}")


user_id = st.number_input("User ID", min_value=1, value=1)
post_id = st.number_input("Post ID", min_value=1, value=1)

if st.button("Send Request"):
    send_request()
