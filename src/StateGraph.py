from langgraph.graph import StateGraph, START, END

from src.AgentState import AgentState
from src.Supervisor import supervisor_node, decide_next_node
from src.Generator import question_generation_node, self_check_question_generation_node
from src.Explainer import question_explanation_node, self_check_question_explanation_node



class App():
    def __init__(self):
        self.app = self.build()
        self.state = {
            "enunciado": "",
            "alternativas": {},
            "gabarito": "",
            "explicacao": "",
            "resposta_user": ""
        }


    def build(self):
        """Constrói e compila o langgraph.StateGraph"""
        graph = StateGraph(AgentState)

        graph.add_node("Supervisor", lambda state:state)

        graph.add_node("Generator", question_generation_node)
        graph.add_node("Generation Self-checker", self_check_question_generation_node)

        graph.add_node("Explainer", question_explanation_node)
        graph.add_node("Explanation Self-checker", self_check_question_explanation_node)

        graph.add_edge(START, "Supervisor")

        graph.add_conditional_edges(
            "Supervisor",
            decide_next_node,
            {
                "generate_question": "Generator",
                "generate_explanation": "Explainer",
                "stop": END
            }
        )

        graph.add_edge("Generator", "Generation Self-checker")
        graph.add_edge("Generation Self-checker", "Supervisor")

        graph.add_edge("Explainer", "Explanation Self-checker")
        graph.add_edge("Explanation Self-checker", "Supervisor")

        return graph.compile()

    
    def get_graph(self):
        """Retorna o mermaid txt da arquitetura do grafo."""
        return self.app.get_graph().draw_mermaid()
    

    def run(self, action: str, resposta_user=None):
        """
        Encapsula chamadas para o grafo, retornando um dicionário
        á ser usado na UI.
        """
        if action == "generate_question":
            return self.generate_question()

        elif (action == "generate_explanation") and (resposta_user is not None):
            return self.generate_explanation(resposta_user)

        else:
            raise ValueError(f"Ação desconhecida={action}, res_user={resposta_user}")
    

    def generate_question(self):
        """Retorna um dicionario com as chaves 'enunciado', 'alternativas' e 'gabarito'."""
        # Limpa explicação para forçar caminho do grafo
        self.state["enunciado"] = ""
        self.state["explicacao"] = ""
        self.state["alternativas"] = {}
        
        self.state = self.app.invoke(self.state)

        return {
            "enunciado": self.state["enunciado"],
            "alternativas": self.state["alternativas"],
            "gabarito": self.state["gabarito"],
        }
    

    def generate_explanation(self, resposta_user) -> str:
        """Retorna a explicação da questão para dada resposta"""
        
        self.state["explicacao"] = ""
        self.state["resposta_user"] = resposta_user

        self.state = self.app.invoke(self.state)

        return self.state["explicacao"]