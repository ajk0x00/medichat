import streamlit as st
import requests

st.title("Echo Bot")

base_api = 'http://localhost:8000'

if "messages" not in st.session_state:
    st.session_state.messages = []

if "uploaded_file_name" not in st.session_state:
    st.session_state.uploaded_file_name = None


# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Upload document section
uploaded_file = st.sidebar.file_uploader("Upload a document", type=["txt", "pdf", "docx"])
if uploaded_file is not None and uploaded_file.name != st.session_state.uploaded_file_name:
    files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
    try:
        with st.spinner("Uploading..."):
            response = requests.post(f"{base_api}/upload", files=files)
            if response.status_code == 200:
                st.success("File uploaded successfully!")
                st.session_state.uploaded_file_name = uploaded_file.name
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
