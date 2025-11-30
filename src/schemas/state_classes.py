from typing_extensions import TypedDict
from langchain_openai import ChatOpenAI

def create_tool_calling_agent(tools: list) -> ChatOpenAI:
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    agent_with_tools = llm.bind_tools(tools)
    return agent_with_tools

# Para o Agente de Busca de Materiais
class MaterialsDto(TypedDict):
    link: str
    type: str
    why: str
    topic: str

class Materials(TypedDict):
    title: str
    topics: list[str]
    public_type: str
    result: list[MaterialsDto]

class GraphState(TypedDict):
    materials: Materials