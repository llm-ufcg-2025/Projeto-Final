from typing import TypedDict

class AgentState(TypedDict):
    """TypedDict contendo o estado do grafo, incluindo:
    enunciado:
    gabarito:
    alternativas:
    explicacao:
    """
    enunciado : str
    alternativas : list[str]
    gabarito : str
    resposta_user: str
    explicacao : str