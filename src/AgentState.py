from typing import TypedDict

class AgentState(TypedDict):
    """TypedDict contendo o estado do grafo, incluindo:
    enunciado:
    gabarito:
    alternativas:
    explicacao:
    """
    enunciado : str
    gabarito : str
    alternativas : list[str]
    explicacao : str