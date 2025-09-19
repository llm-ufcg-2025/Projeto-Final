import streamlit as st

from src import App
st.badge("Conteúdo gerado por IA", icon=":material/info:", color="yellow")


# INIT ESTADO
estados = {
    'app': App(),
    'etapa': "boas-vindas",
    'question_info': {},
    'user_answer': None
}

for chave, valor in estados.items():
    if chave not in st.session_state:
        st.session_state[chave] = valor


# AUX FUNCTIONS
def ir_boas_vindas():
    st.session_state.etapa = "boas-vindas"
    st.session_state.question_info = {}
    st.session_state.user_answer = None


def proxima_questao():
    """Gerar pergunta e exibir"""
    st.session_state.etapa = "responder-questao"
    st.session_state.question_info = st.session_state.app.generate_question()


def enviar_resposta(user_answer):
    """Responder questao e gerar explicacao se necessario"""
    st.session_state.etapa = "correcao"
    st.session_state.user_answer = user_answer



# SUBTELAS
if st.session_state.etapa == "boas-vindas":
    st.button("Vamos começar? ", on_click=proxima_questao)
    

elif st.session_state.etapa == "responder-questao":
    st.markdown(f"**Questão:** {st.session_state.question_info['enunciado']}")

    user_answer = st.radio(
        "Selecione sua resposta:", 
        list(st.session_state.question_info['alternativas'].keys()), 
        format_func=lambda x: f"{x}) {st.session_state.question_info['alternativas'][x]}")
    
    st.button("Responder", on_click=enviar_resposta(user_answer))


elif st.session_state.etapa == "correcao":
    if st.session_state.question_info['gabarito'] == st.session_state.user_answer:
        st.success("Você é fera demais!")
        st.balloons()
    else:
        st.error("erouuuuu")
    
    st.button('Próxima questao', on_click=proxima_questao)
    st.button("Parar", on_click=ir_boas_vindas)
