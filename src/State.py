from typing import TypedDict, List
from langchain.schema import Document

class State(TypedDict):
    question: str
    context: List[Document]
    answer: str
    used_web: bool
    is_off_topic: bool
