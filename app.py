import streamlit as st


st.set_page_config(page_title="LLM - Projeto Final", layout="centered")

st.title("📚 FoqueAI", anchor=False)
st.caption("Seu agente de IA sobre TDAH?")


pg = st.navigation([
    st.Page("ui/slides.py", title="Slides", icon="📚"),
    st.Page("ui/tdah.py", title="Demo", icon="📝"),
])

pg.run()