import os, getpass

from langchain import hub
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.documents import Document
from langchain_community.tools import DuckDuckGoSearchResults
from langchain_community.vectorstores import FAISS

from src.State import State



def _set_env(var) -> None:
        if not os.environ.get(var):
            os.environ[var] = getpass.getpass(var)

_set_env("GOOGLE_API_KEY")




embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vectorstore = FAISS.load_local("dataset/faiss_index", embeddings, allow_dangerous_deserialization=True)

web_search = DuckDuckGoSearchResults(num_results=3)

prompt = hub.pull("rlm/rag-prompt")
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)




def retrieve(state: State) -> State:
    # Primeiro, verifica se a pergunta é sobre TDAH ou temas relacionados
    topic_keywords = ["TDAH", "ADHD", "déficit de atenção", "hiperatividade",
                     "transtorno atenção", "neurodesenvolvimento", "psiquiatria",
                     "mental health", "saúde mental", "neurodivergência", "autismo", "tdah", "ritalina", "venvanse"]

    question_lower = state["question"].lower()
    is_about_tdah = any(keyword.lower() in question_lower for keyword in topic_keywords)

    if not is_about_tdah:
        return {"context": [], "used_web": False, "is_off_topic": True}

    # Se for sobre TDAH, busca no vectorstore
    retrieved_docs = vectorstore.similarity_search(state["question"])

    if not retrieved_docs:
        web_results = web_search.run(state["question"])

        web_docs = []
        for i, res in enumerate(web_results.split("\n")):
            if res.strip():
                parts = res.split(" - ")
                content = res
                metadata = {"source": "web", "search_result": f"result_{i+1}"}

                if len(parts) >= 2:
                    content = parts[0]
                    metadata["url"] = parts[-1]

                web_docs.append(Document(page_content=content, metadata=metadata))

        return {"context": web_docs, "used_web": True, "is_off_topic": False}
    else:
        return {"context": retrieved_docs, "used_web": False, "is_off_topic": False}






def generate(state: State) -> State:
    if state.get("is_off_topic", False):
        # Para perguntas fora do escopo, resposta simples sem fontes
        messages = [
            SystemMessage(
                content="""Você é um assistente especializado em TDAH. Para 
                perguntas fora deste escopo, responda de forma geral sem citar
                fontes específicas."""),
            HumanMessage(
                content=f"""Pergunta: {state['question']}\n\nPor favor, responda
                de forma geral, já que esta pergunta não está relacionada ao TDAH.""")
        ]
        response = llm.invoke(messages)
        return {"answer": response.content}

    # Prepara o contexto com fontes (apenas para perguntas sobre TDAH)
    context_with_sources = []
    for i, doc in enumerate(state["context"]):
        source_info = ""
        if "url" in doc.metadata:
            source_info = f" [Fonte: {doc.metadata['url']}]"
        elif "source" in doc.metadata and doc.metadata["source"] == "web":
            source_info = f" [Fonte: Resultado de busca {i+1}]"
        elif "page" in doc.metadata:
            source_info = f" [Fonte: PDF p.{doc.metadata.get('page', 'N/A')}]"

        context_with_sources.append(f"{doc.page_content}{source_info}")

    docs_content = "\n\n".join(context_with_sources)
    messages = prompt.invoke({"question": state["question"], "context": docs_content})
    response = llm.invoke(messages)
    return {"answer": response.content}



def self_check(state: State) -> State:
    # Se for off-topic, não faz verificação de fontes
    if state.get("is_off_topic", False):
        return state

    answer = state["answer"]

    # Verifica se já contém informações de fonte
    has_sources = any(keyword in answer for keyword in
                     ["Fonte:", "http://", "https://", "p.", "página", "fonte:", "source:"])

    if has_sources:
        return state
    else:
        # Busca específica para fontes confiáveis sobre TDAH
        search_query = f"{state['question']} site:.edu OR site:.gov OR site:.org OR site:.research OR site:.scielo.br"
        web_results = web_search.run(search_query)

        web_docs = []
        for i, res in enumerate(web_results.split("\n")):
            if res.strip():
                parts = res.split(" - ")
                content = res
                metadata = {"source": "web_verification", "result_type": "source_validation"}

                if len(parts) >= 2:
                    content = f"Informação de validação: {parts[0]}"
                    metadata["validation_url"] = parts[-1]
                    metadata["source_number"] = i + 1

                web_docs.append(Document(page_content=content, metadata=metadata))

        # Prepara contexto com ênfase em fontes
        verification_context = "\n\n".join(
            f"{doc.page_content} [Fonte de verificação: {doc.metadata.get('validation_url', 'Busca web')}]"
            for doc in web_docs
        )

        # Prompt específico para incluir fontes
        source_prompt = """
        Você forneceu uma resposta sobre TDAH, mas precisa incluir fontes confiáveis.
        Use as informações abaixo para adicionar referências à sua resposta.

        Pergunta original: {question}

        Sua resposta inicial: {initial_answer}

        Informações para citação:
        {context}

        Por favor, revise sua resposta incluindo fontes confiáveis (URLs quando disponível).
        Use formato: [Fonte: URL ou descrição da fonte]
        """

        messages = [
            SystemMessage(content="Você é um assistente especializado em TDAH que sempre cita fontes confiáveis."),
            HumanMessage(content=source_prompt.format(
                question=state["question"],
                initial_answer=state["answer"],
                context=verification_context
            ))
        ]

        response = llm.invoke(messages)
        return {"answer": response.content, "context": state["context"] + web_docs}
