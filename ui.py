import streamlit as st
import requests
import time


base_api = 'http://localhost:8000'

if "messages" not in st.session_state:
    st.session_state.messages = []

if "already_uploaded_files" not in st.session_state:
    st.session_state.already_uploaded_files= []

if "backend_ready" not in st.session_state:
    st.session_state.backend_ready = False

while not st.session_state.backend_ready:
    with st.spinner("Wait for it...", show_time=True):
        try:
            response = requests.get(f"{base_api}/")
            st.session_state.backend_ready = True
        except:
            time.sleep(3)
# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Upload document section
uploaded_files = st.sidebar.file_uploader(
    "Upload a document",
    type=["txt", "pdf", "docx"],
    accept_multiple_files=True
)
for uploaded_file in uploaded_files:
    if uploaded_file.name in st.session_state.already_uploaded_files:
        continue
    files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
    try:
        with st.spinner("Uploading..."):
            response = requests.post(f"{base_api}/upload", files=files)
            if response.status_code == 200:
                st.success("File uploaded successfully!")
                st.session_state.already_uploaded_files.append(uploaded_file.name)
            else:
                st.error(f"Upload failed: {response.text}")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.session_state.messages.append({"role": "assistant", "content": f"⚠️ Error: {str(e)}"})

if prompt := st.chat_input("What is up?"):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    response = requests.post(f"{base_api}/ask", json={"question": prompt})
    print(response.content)
    st.session_state.messages.append(
        {"role": "assistant", "content": response.json().get("results", "No response")}
    )
    st.rerun()
