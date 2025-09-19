import streamlit as st

st.set_page_config(page_title="LLM - Projeto Final", layout="centered")

st.title("📚 CheckAI", anchor=False)
st.caption("Pronto para gabaritar a prova do mestrado?")


pg = st.navigation([
    st.Page("app/slides.py", title="Slides", icon="📚"),
    st.Page("app/app.py", title="App", icon="📝"),
])

pg.run()