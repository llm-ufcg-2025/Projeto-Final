# Projeto Final da Disciplina LLM

## Setup
1. pip install -r requirements.txt
2. streamlit run ./app.py

## Arquitetura proposta

---

## Lixo
- métricas: Context Precision/Recall, Faithfulness, latência média, 	footprint (RAM/CPU).

- avaliação: 
    - Conjunto de perguntas de teste rotuladas 	manualmente 		(ou semi-geradas) (20–30) + gabarito (URL/trecho 			“verdadeiro”).

    - RAGAS/Giskard (faithfulness, answer relevancy) + 			relatório eval/report.md.

    - Giskard (opcional) — playbook de testes no caso 			IPCC/clima. docs.giskard.aiLinks to an external site.

    - PaperQA2 como baseline de alta precisão em PDF científico 		(comparação)


- dados, 
- limites éticos
