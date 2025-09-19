from langgraph.graph import StateGraph, START, END

from AgentState import AgentState
from Supervisor import supervisor_node, decide_next_node
from Generator import question_generation_node, self_check_question_generation_node
from Explainer import question_explanation_node, self_check_question_explanation_node


graph = StateGraph(AgentState)

class App():
    def __init__(self):
        self.graph = self.build_graph()
        self.app = graph.compile()


    def build_graph(self):
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

    
    def __repr__(self):
        return self.app.get_graph().draw_mermaid()


app = App()
print(app)