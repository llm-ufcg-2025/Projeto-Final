import time
import streamlit as st
from src.StateGraph import App

st.badge("Respostas geradas por IA", icon=":material/info:", color="yellow")


# INIT ESTADO DO STREAMLIT
estado = {
    'app': App(),
    'mensagens': [] # Histório de mensagens
}

for key, value in estado.items():    
    if key not in st.session_state:
        st.session_state[key] = value


def load_historico():
    for msg in st.session_state.mensagens:
        with st.chat_message(msg["role"]):
            if msg['role'] == 'assistant':
                st.markdown(msg["content"])
            else:
                st.text(msg['content'])


load_historico()

if prompt := st.chat_input("Digite sua mensagem..."):
    st.session_state.mensagens.append({"role": "user", "content": prompt})
    with st.chat_message("user", ):
        st.text(prompt)

    resposta = f"{prompt}"

    # adiciona resposta do bot
    st.session_state.mensagens.append({"role": "assistant", "content": resposta})
    with st.chat_message("assistant"):
        time.sleep(1)
        placeholder = st.empty()
        texto = ""
        for letra in resposta:
            texto += letra
            placeholder.markdown(texto)  # ou st.write
            time.sleep(0.04)  # ajuste a velocidade (em segundos)