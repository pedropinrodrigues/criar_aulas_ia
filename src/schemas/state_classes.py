from typing_extensions import TypedDict

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