import streamlit as st

st.markdown(f"```mermaid\n{st.session_state.app.get_graph()}\n```")