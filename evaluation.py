"""Este módulo visa avaliar via RAGAS a performance do sistema desenvolvido."""

import os
import time
import psutil
import numpy as np
import pandas as pd


from ragas import evaluate
from datasets import Dataset
from ragas.metrics import faithfulness, answer_relevancy, answer_correctness
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from src import App




def bootstrap(values, n_bootstrap=10000):
    values = np.array(values)
    mean = values.mean()
    std = values.std()
    boot_means = [np.random.choice(values, size=len(values), replace=True).mean() for _ in range(n_bootstrap)]
    ic95 = np.percentile(boot_means, [2.5, 97.5])
    return mean, std, ic95


APP = App()

gemini_embeddings = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

gemini_llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0
)


questions = [
    'Qual a capital da França?',
    'Quem escreveu Orgulho e Preconceito?',
]

ground_truths = [
    "Paris",
    'Jane Austen'
]


resources_usages = {
    'latencia': [],
    'ram': [],
    'cpu': []
}

rows = []

for question, gt in zip(questions, ground_truths):
    process = psutil.Process()

    mem_before = process.memory_info().rss / (1024 ** 2)  # MB
    cpu_before = psutil.cpu_percent(interval=None)
    time_before = time.time()

    res_state = APP.run(question) # Chamada ao modelo
    
    time_after = time.time()
    mem_after = process.memory_info().rss / (1024 ** 2)  # MB
    cpu_after = psutil.cpu_percent(interval=None)

    resources_usages['latencia'].append(time_after - time_before)
    resources_usages['ram'].append(mem_after - mem_before)
    resources_usages['cpu'].append(cpu_after - cpu_before)



    rows.append({
        'user_input': question,
        'retrieved_contexts': res_state["context"],
        'response': res_state['answer'],
        'reference': gt
    })

evaluation_dataset = Dataset.from_list(rows)


# scores = evaluate(
#     evaluation_dataset,
#     metrics=[
#         faithfulness,
#         answer_relevancy,
#         answer_correctness
#     ],
#     llm=gemini_llm,
#     embeddings=gemini_embeddings
# )


print(rows)
# print(scores)

with open('eval/relatorio.md', mode='w') as f:
    for metrica in ['latencia', 'ram', 'cpu']:
        mean, std, ic = bootstrap(resources_usages[metrica])
        msg = f"{metrica} por query: {resources_usages[metrica]}\n"
        msg += f"Media: {mean:.3f}\nDesvio: {std:.3f}\nIC95%: ({ic[0]:.3f}, {ic[1]:.3f})\n\n"
        f.write(msg)



