# Projeto Final da Disciplina LLM

## Setup
1. pip install -r requirements.txt
2. streamlit run ./app.py
3. Ambiente: Colab (GPU não utilizada, CPU e RAM padrão).
4. Biblioteca base: langchain, langgraph, faiss para indexação vetorial.
5. LLM: modelo open-source via pipeline HuggingFace.
6. Dados: PDF oficial do Protocolo Clínico e Diretrizes Terapêuticas (PCDT) para TDAH
7. (https://drive.google.com/file/d/125iNbSXhMir59ebmqRUihftKjTVpTby-/view?usp=sharing)

## Arquitetura proposta
O fluxo de execução segue a lógica clássica de RAG, modelada como grafo de agentes:
1. Consulta do usuário → interpretada como pergunta em linguagem natural.
2. Retriever → busca passagens relevantes no índice vetorial construído a partir do PDF.
3. Context Builder → organiza os trechos recuperados em contexto coerente.
4. LLM Generator → gera a resposta fundamentada no contexto.
   
(Imagem do fluxo: https://drive.google.com/file/d/1zS8ZRJfGCJR5XgF6KAFVnznRdqICssyR/view?usp=sharing)

## Métricas
1. Desempenho:

Latência (s/query): média 37.27 ± 60.67 (IC95%: 18.05 – 68.49).

RAM (MB/query): média 3.57 ± 11.60 (IC95%: 0.62 – 9.13).

CPU (%/query): média 10.01 ± 16.46 (IC95%: 4.49 – 18.50).

2. Qualidade da Resposta:

Faithfulness (aderência ao texto-fonte): 0.878 ± 0.025 (IC95%: 0.868 – 0.889).

Answer Relevancy: 0.929 ± 0.016 (IC95%: 0.922 – 0.936).

Answer Correctness: 0.847 ± 0.028 (IC95%: 0.834 – 0.859).

Context Precision: 0.729 ± 0.023 (IC95%: 0.719 – 0.739).

Context Recall: 0.791 ± 0.024 (IC95%: 0.780 – 0.801).

- avaliação: 
    - Conjunto de perguntas de teste rotuladas 	manualmente 		(ou semi-geradas) (20–30) + gabarito (URL/trecho 			“verdadeiro”).

    - RAGAS/Giskard (faithfulness, answer relevancy) + 			relatório eval/report.md.

## Limites Técnicos:
1. Latência elevada e variável: presença de outliers (ex. query 7 com >280s) indica gargalo em recuperação ou execução do LLM.
2. Uso de recursos: RAM estável, mas uma query inicial consumiu muito mais memória (provavelmente carregamento de embeddings).
3. CPU: média baixa (10%), mas picos (75%) em queries específicas.
4. Robustez: apesar dos limites, a consistência nas métricas de qualidade sugere boa fidelidade às fontes.

## Limites Éticos:
1. Evitar que o modelo fizesse diagnóstico
2. Evitar que o modelo receitasse medicamentos e doses
3. Evitar que o modelo interferisse em tratamentos já iniciados ao dar dados mal informados.
4. Como estamos mexendo no setor da saúde, o disclaimer era de extrema importância.

  
