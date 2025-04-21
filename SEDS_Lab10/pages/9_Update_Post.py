import streamlit as st
import requests

BASE_URL = "http://localhost:8000"

st.title("Update Post")


def send_request():
    try:
        response = requests.put(
            f"{BASE_URL}/posts/{post_id}", json={"title": title, "content": content})
        if response.status_code == 200:
            st.success("Post successfully updated.")
            st.json(response.json())
        else:
            st.error(f"Error: {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        st.error(f"Request failed: {e}")


post_id = st.number_input("Post ID", min_value=1, value=1)
title = st.text_input("New Title")
content = st.text_area("New Content")

if st.button("Send Request"):
    send_request()
