import streamlit as st

st.set_page_config(page_title="LLM - Projeto Final", layout="centered")

st.title("📚 CheckAI", anchor=False)
st.caption("Pronto para gabaritar a prova do mestrado?")


pg = st.navigation([
    st.Page("ui/slides.py", title="Slides", icon="📚"),
    st.Page("ui/checkai.py", title="CheckAI", icon="📝"),
])

pg.run()