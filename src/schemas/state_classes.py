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
    student_level: str
    result: list[MaterialsDto]

# Para agente de Docuemntação e Estruturação da parte Teórica da Aula
class TheoryClass(TypedDict):
    title: str
    content: str
    student_level: str
    duration_minutes: int
    references: list[str]
    result: str

# Para agente de Documentação e Estruturação da parte Prática da Aula
class PraticalClass(TypedDict):
    theory_documentation = str
    language = str
    student_level = str
    
    compelete_code = str
    incomplete_code = str
    pratical_documentation = str
    
class GraphState(TypedDict):
    materials: Materials
    theory_class: TheoryClass
    pratical_class: PraticalClass