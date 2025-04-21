import streamlit as st
import requests

BASE_URL = "http://localhost:8000"

st.title("Create Post for User")


def send_request():
    try:
        response = requests.post(
            f"{BASE_URL}/users/{user_id}/posts/new", json={"title": title, "content": content})
        if response.status_code in [200, 201]:
            st.json(response.json())
        else:
            st.error(f"Error: {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        st.error(f"Request failed: {e}")


user_id = st.number_input("User ID", min_value=1, value=1)
title = st.text_input("Post Title")
content = st.text_area("Post Content")

if st.button("Send Request"):
    send_request()
