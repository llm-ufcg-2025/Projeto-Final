"""Este módulo visa avaliar via RAGAS a performance do sistema desenvolvido."""

from datasets import Dataset
from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    answer_correctness
)

from src import App

# DOCUMENTOS QUE O AGENTE VAI USAR NO RAG
docs = [
    'Paris é a capital da França',
    'Jane Austen escreveu Orgulho e Preconceito',

]

APP = App()


questions = [
    'Qual a capital da França?',
    'Quem escreveu Orgulho e Preconceito?',
]

ground_truths = [
    "Paris",
    'Jane Austen'
]

rows = []

for question, gt in zip(questions, ground_truths):
    context = ["None"] #retrieve(question, k=2) # lógica de RAG para obter o conteudo do livro
    answer = "Não sei" # APP.run(question, context) # Lógica de geração de resposta do agente
    rows.append({
        'user_input': question,
        'retrieved_contexts': context,
        'response': answer,
        'reference': gt
    })

evaluation_dataset = Dataset.from_list(rows)
print(evaluation_dataset)

scores = evaluate(
    evaluation_dataset,
    metrics=[
        faithfulness,
        answer_relevancy,
        answer_correctness
    ]
)

print(rows)
print(scores)