from AgentState import AgentState

def supervisor_node(state: AgentState) -> AgentState:
    """Nó para gerenciar interações com usuário"""
    return state

def decide_next_node(state: AgentState) -> str:
    """Função para rotear entre os agentes de geração e explicação de questões
    
    Presume-se que enunciado ficará vazio quando for hora de gerar questão"""
    if not state["enunciado"]:
        return "generate_question"
    
    elif not state['explicacao']:
        return "generate_explanation"
    
    elif not state['continue']:
        return "stop"