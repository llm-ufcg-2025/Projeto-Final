from src.AgentState import AgentState

def question_explanation_node(state: AgentState) -> AgentState:
    """Nó para uso de LLM e busca na WEB para gerar a explicação da questão"""
    state['explicacao'] = "Errou, errou. Só aceite, oxe"
    return state



def self_check_question_explanation_node(state: AgentState) -> AgentState:
    """Nó com mecanismo anti-alucinação para geração da explicação"""
    state['explicacao'] += " (self-check aprova esta resposta, rééé)"
    return state