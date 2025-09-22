import time
import streamlit as st
from src.App import App

if 'app' not in st.session_state:
    st.session_state.app = App()

if 'mensagens' not in st.session_state:
    st.session_state.mensagens = []

st.set_page_config(page_title="LLM - Projeto Final", layout="centered")

st.title("📚 FoqueAI", anchor=False)
st.caption("Seu agente de IA sobre TDAH?")


def load_historico():
    for msg in st.session_state.mensagens:
        with st.chat_message(msg["role"]):
            if msg['role'] == 'assistant':
                st.markdown(msg["content"])
            else:
                st.text(msg['content'])

def load_prompt():
    if prompt := st.chat_input("Digite sua mensagem..."):
        st.session_state.mensagens.append({"role": "user", "content": prompt})
        with st.chat_message("user", ):
            st.text(prompt)

        resposta = st.session_state.app.run(prompt)['answer']

        # adiciona resposta do bot
        st.session_state.mensagens.append({"role": "assistant", "content": resposta})
        with st.chat_message("assistant"):
            time.sleep(1)
            placeholder = st.empty()
            texto = ""
            for letra in resposta:
                texto += letra
                placeholder.markdown(texto)  # ou st.write
                time.sleep(0.02)  # ajuste a velocidade (em segundos)

def load_disclaimer():
    st.badge("Respostas geradas por IA", icon=":material/info:", color="yellow")


load_historico()
load_prompt()
load_disclaimer()



