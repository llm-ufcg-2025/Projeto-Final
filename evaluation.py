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
    "Como podem ser divididas as técnicas de tratamento de TDAH?",
    "Quais as técnicas cognitivas mais utilizadas para tratar TDAH?",
    "Quais as técnicas comportamentais mais utilizadas para tratar TDAH?",
    "O incentivo as famílias a fortalecer as parcerias ajuda o processo de gerenciamento do TDAH?",
    "O que é aconselhável ao profissional de saúde após diagnosticar TDAH?",
    "O que é o TDAH segundo o DSM-5?",
    "Quando os sintomas do TDAH geralmente começam?",
    "Qual a prevalência mundial de TDAH em crianças e adolescentes?",
    "Quais funções cognitivas podem ser afetadas pelo TDAH?",
    "Qual a prevalência de TDAH em crianças e adolescentes no Brasil?",
    "Quem deve realizar o diagnóstico de TDAH?",
    "Que tipo de avaliação deve ser feita em casos de suspeita de TDAH?",
    "O diagnóstico de TDAH pode ser feito tanto em crianças quanto em adultos?",
    "Quantos sintomas indicativos podem confirmar o diagnóstico de TDAH?",
    "Quais os principais grupos de sintomas do TDAH?",
    "Qual é o código do TDAH na CID-10 da OMS?",
    "Qual abordagem é recomendada para o tratamento do TDAH?",
    "Quais intervenções não medicamentosas são citadas para o TDAH?",
    "O que as diretrizes do NICE recomendam no tratamento do TDAH?",
    "Que estratégias muitos adultos com TDAH desenvolvem?"
]

ground_truths = [
    'Técnicas cognitivas e comportamentais', # Pag 18
    'reestruturação cognitiva, solução de problemas, diálogo interno, treinamento de autocontrole, autorreforço e treino de autoinstrução', # Pag 18
    'automonitoramento e autoavaliação, sistema de recompensas, sistema de fichas, custo de resposta, punições, tarefas de casa, modelagem, dramatizações, além de treinamento de comunicação social, planejamento e cronogramas', # Pag 18
    'Sim, ajudam', # Pag 21
    "Proporcionar uma discussão estruturada com o paciente sobre como o TDAH pode afetar sua vida", # Pag 22
    "É um transtorno do neurodesenvolvimento marcado por desatenção, hiperatividade e impulsividade.", # Pag 7
    "Na infância.", # Pag 7
    "Entre 3% e 8%.", # Pag 7
    "Atenção, memória de trabalho, planejamento e resolução de problemas", # Pag 7
    "7,6%.", # Pag 7
    'Médico psiquiatra, pediatra ou outro profissional de saúde qualificado.', # Pag 10
    'Uma avaliação clínica e psicossocial completa.', # Pag 10
    'Sim.', # Pag 10
    'Dezoito sintomas.', # Pag 10
    'Desatenção, hiperatividade e impulsividade.', # Pag 10
    'F90.', # Pag 10
    "Uma intervenção multimodal.", # Pag 17
    "Intervenções cognitivas e comportamentais.", # Pag 17
    "Dieta equilibrada, boa nutrição e exercício físico regular.", # Pag 17
    "Estratégias compensatórias de enfrentamento." # Pag 17
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

scores = evaluate(
    evaluation_dataset,
    metrics=[
        faithfulness,
        answer_relevancy,
        answer_correctness
    ],
    llm=gemini_llm,
    embeddings=gemini_embeddings
)



df1 = scores.to_pandas()
# df1.to_csv('eval/ragas.csv')
df1 = df1.reset_index(drop=True)

df2 = pd.DataFrame(resources_usages)
# df2.to_csv('eval/resources.csv')
df2 = df2.reset_index(drop=True)

df3 = pd.concat([df1, df2], axis=1)
df3.to_csv('eval/metrics.csv')


with open('eval/relatorio.md', mode='w') as f:
    for metrica in ['latencia', 'ram', 'cpu', 'faithfulness', 'answer_relevancy', 'answer_correctness']:
        mean, std, ic = bootstrap(df3[metrica])
        msg = f"{metrica} por query: {df3[metrica]}\n"
        msg += f"Media: {mean:.3f}\nDesvio: {std:.3f}\nIC95%: ({ic[0]:.3f}, {ic[1]:.3f})\n\n"
        f.write(msg)