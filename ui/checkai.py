import streamlit as st
import time

from src import App

st.badge("Conteúdo gerado por IA", icon=":material/info:", color="yellow")

# INIT ESTADO
estados = {
    'app': App(),
    'etapa': "boas-vindas",
    'question_info': {},
    'user_answer': "",
    'acertou': None,
    'explicacao': ""
}

for chave, valor in estados.items():
    if chave not in st.session_state:
        st.session_state[chave] = valor


# AUX FUNCTIONS
def ir_boas_vindas():
    st.session_state.etapa = "boas-vindas"
    st.session_state.question_info = {}


def proxima_questao():
    """Gerar pergunta e exibir"""
    st.session_state.etapa = "responder-questao"
    st.session_state.question_info = st.session_state.app.generate_question()


def enviar_resposta(user_answer):
    """Responder questao e gerar explicacao se necessario"""
    if user_answer is not None:
        st.session_state.etapa = "correcao"
        st.session_state.user_answer = user_answer

        st.session_state.acertou = st.session_state.question_info['gabarito'] == user_answer
        if not st.session_state.acertou:
            st.session_state.explicacao = st.session_state.app.generate_explanation(user_answer)


def get_index(letra):
    return ['a', 'b', 'c', 'd', 'e'].index(letra)


# SUBTELAS
if st.session_state.etapa == "boas-vindas":
    st.button("Vamos começar? ⚔️", on_click=proxima_questao)
    

elif st.session_state.etapa == "responder-questao":
    st.markdown(f"**Questão:** {st.session_state.question_info['enunciado']}")

    user_answer = st.radio(
        "Selecione sua resposta:", 
        list(st.session_state.question_info['alternativas'].keys()),
        format_func=lambda x: f"{x}) {st.session_state.question_info['alternativas'][x]}",
        index=None)
    
    st.button("Responder", on_click=enviar_resposta, args=[user_answer])


elif st.session_state.etapa == "correcao":
    st.markdown(f"**Questão:** {st.session_state.question_info['enunciado']}")

    st.radio(
        "Selecione sua resposta:", 
        list(st.session_state.question_info['alternativas'].keys()),
        format_func=lambda x: f"{x}) {st.session_state.question_info['alternativas'][x]}",
        index=get_index(st.session_state.user_answer),
        disabled=True)
    
    if st.session_state.acertou:
        st.success("Você é fera demais!")
        st.balloons()
    else:
        st.error("erouuuuu")

        st.subheader("Explicação", anchor=False)

        with st.chat_message('ai'):
            time.sleep(1)
            placeholder = st.empty()
            texto = ""
            for letra in st.session_state.explicacao:
                texto += letra
                placeholder.write(texto)  # ou st.write
                time.sleep(0.05)  # ajuste a velocidade (em segundos)
    


    st.button('Próxima questao', on_click=proxima_questao)
    st.button("Parar", on_click=ir_boas_vindas)