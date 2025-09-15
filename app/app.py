import streamlit as st

n_questao = 1
pontuacao = 0

def start_quiz():
    st.session_state.started = True

def send_answer(resposta):
    st.write(f"Voce escolheu a alternativa {resposta}")
    

def get_questao():
    return {
        'enunciado': """Considere o problema de acessar os registros de um arquivo. Cada registro contém
uma chave única que é utilizada para recuperar os registros do arquivo. Dada uma chave qualquer, o
problema consiste em localizar o registro que contenha essa chave. O algoritmo examina os registros
na ordem em que eles aparecem no arquivo, até que o registro procurado seja encontrado ou fique
determinado que ele não se encontra no arquivo. Seja f uma função de complexidade tal que f(n) é o
número de registros consultado no arquivo, é correto afirmar que:""",
        'alternativas': [
            'O caso médio é f(n) = (n + 1)/2', 
            'O melhor caso é f(n) = n – 1', 
            'O caso ótimo é f(n) = 3n/2 – 3/2', 
            'O caso recorrente é f(n) = 2(n – 1)', 
            'O pior caso é f(n) = 1']
    }

if "started" not in st.session_state:
    st.session_state.started = False

if not st.session_state.started:
    st.title("📚💡POSCOMP Simulator")
    st.write("Pronto para gabaritar o exame de admissão no mestrado?")
    st.button("Vamos começar! ⚔️", on_click=start_quiz)

else:
    questao = get_questao()
    st.title("📚💡POSCOMP Simulator", anchor=False)

    st.header(f"Questão {n_questao}")
    st.write(questao['enunciado'])
    resposta = st.radio("Escolha a resposta:", questao['alternativas'])
    st.button("Enviar resposta", on_click=send_answer, args=[resposta])

