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

# Para agente de Docuemntação e Estruturação da parte Teórica da Aula
class TheoryClass(TypedDict):
    title: str
    content: str
    duration_minutes: int
    references: list[str]

class GraphState(TypedDict):
    materials: Materials
    theory_class: TheoryClass