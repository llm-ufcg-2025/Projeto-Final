# Projeto Final da Disciplina LLM

## Setup
1. pip install -r requirements.txt
2. streamlit run ./app/app.py

## Arquitetura proposta
```mermaid
    U[Usuário] -->|Pede questão| GQ[Agente Gerador de Questões]
    GQ -->|Busca provas antigas| RAG[RAG Local DB]
    GQ -->|Se insuficiente| WEB[Agente de Pesquisa Online]

    GQ -->|Retorna questão+alternativas| U

    U -->|Envia resposta escolhida| COR[Agente de Correção]
    COR --> RAG
    COR --> WEB
    COR -->|Explicação + Correção| U

    COR -->|Resultado certo/errado| PONT[Agente de Pontuação]
    PONT --> DB[(Banco de Pontos/Histórico)]
    PONT -->|Placar parcial| U
```


## Lixo
- métricas: Context Precision/Recall, Faithfulness, latência média, 	footprint (RAM/CPU).

- avaliação: 
    - Conjunto de perguntas de teste rotuladas 	manualmente 		(ou semi-geradas) (20–30) + gabarito (URL/trecho 			“verdadeiro”).

    - RAGAS/Giskard (faithfulness, answer relevancy) + 			relatório eval/report.md.

    - Giskard (opcional) — playbook de testes no caso 			IPCC/clima. docs.giskard.aiLinks to an external site.

    - PaperQA2 como baseline de alta precisão em PDF científico 		(comparação)

- setup, 
- arquitetura do grafo, 
- dados, 
- limites éticos
