import streamlit as st

from src.App import App


if 'app' not in st.session_state:
    st.session_state.app = App()

if 'mensagens' not in st.session_state:
    st.session_state.mensagens = []



st.set_page_config(page_title="LLM - Projeto Final", layout="centered")

st.title("📚 FoqueAI", anchor=False)
st.caption("Seu agente de IA sobre TDAH?")


pg = st.navigation([
    st.Page("ui/slides.py", title="Slides", icon="📚"),
    st.Page("ui/tdah.py", title="Demo", icon="📝"),
])

pg.run()