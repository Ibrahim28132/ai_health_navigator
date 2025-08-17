import streamlit as st
import requests

st.title("🩺 AI Health Navigator")
st.markdown("Ask health questions and follow up for more info.")

# Session state for chat history
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

user_input = st.text_input("Type your question or follow-up...")

if st.button("Send"):
    if user_input:
        with st.spinner("Thinking..."):
            try:
                # Use a fixed user_id for demo; in production, use login/session
                resp = requests.post("http://backend:8000/chat", json={"user_id": "demo", "message": user_input})
                data = resp.json()
                if "error" in data:
                    st.error(data["error"])
                else:
                    st.session_state["chat_history"].append(("You", user_input))
                    st.session_state["chat_history"].append(("Agent", data["response"]))
            except Exception as e:
                st.error(f"Error: {str(e)}")
    else:
        st.warning("Enter your question.")

# Display chat history
st.markdown("---")
st.subheader("Conversation")
for sender, msg in st.session_state["chat_history"]:
    if sender == "You":
        st.markdown(f"**You:** {msg}")
    else:
        st.markdown(f"**Agent:** {msg}")