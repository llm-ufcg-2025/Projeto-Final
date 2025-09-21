from langgraph.graph import StateGraph, START, END

from src.State import State
from src.tools import retrieve, generate, self_check




class App():
    def __init__(self):
        self.app = self.build()


    def build(self):
        """Constrói e compila o langgraph.StateGraph"""
        # Configuração do grafo
        graph = StateGraph(State)

        graph.add_node("Retriever", retrieve)
        graph.add_node("Generator", generate)
        graph.add_node("SelfChecker", self_check)

        graph.add_edge(START, "Retriever")
        graph.add_edge("Retriever", "Generator")
        graph.add_edge("Generator", "SelfChecker")
        graph.add_edge("SelfChecker", END)

        return graph.compile()

    
    def get_graph(self):
        """Retorna o mermaid txt da arquitetura do grafo."""
        return self.app.get_graph().draw_mermaid()
    

    def run(self, question):
        return self.app.invoke({'question': question})