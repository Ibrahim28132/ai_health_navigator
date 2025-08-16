import streamlit as st
import requests

st.title("🩺 AI Health Navigator")
st.markdown("Enter symptoms and location for advice.")

query = st.text_input("Query (e.g., 'fever and headache in Lagos')")

if st.button("Get Advice"):
    if query:
        with st.spinner("Processing..."):
            try:
                resp = requests.post("http://localhost:8000/navigate", json={"query": query})
                data = resp.json()
                if "error" in data:
                    st.error(data["error"])
                else:
                    st.markdown(data["response"])
            except Exception as e:
                st.error(f"Error: {str(e)}")
    else:
        st.warning("Enter query.")