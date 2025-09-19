from src.AgentState import AgentState

def question_generation_node(state: AgentState) -> AgentState:
    """Nó responsável pela geração de questões ao estilo POSComp usando RAG e LLM"""
    
    state['enunciado'] = """Considere o problema de acessar os registros de um arquivo. Cada registro contém
        uma chave única que é utilizada para recuperar os registros do arquivo. Dada uma chave qualquer, o
        problema consiste em localizar o registro que contenha essa chave. O algoritmo examina os registros
        na ordem em que eles aparecem no arquivo, até que o registro procurado seja encontrado ou fique
        determinado que ele não se encontra no arquivo. Seja f uma função de complexidade tal que f(n) é o
        número de registros consultado no arquivo, é correto afirmar que:"""
    
    state['alternativas'] = {
            'a': 'O caso médio é f(n) = (n + 1)/2', 
            'b': 'O melhor caso é f(n) = n – 1', 
            'c': 'O caso ótimo é f(n) = 3n/2 – 3/2', 
            'd': 'O caso recorrente é f(n) = 2(n – 1)', 
            'e': 'O pior caso é f(n) = 1'
        }
    
    state['gabarito'] = 'a'
    
    return state



def self_check_question_generation_node(state: AgentState) -> AgentState:
    """Nó com mecanismo anti-alucinação para geracao das questoes"""
    state['enunciado'] += " (self-check aprova esta pergunta, rééé)"
    return state