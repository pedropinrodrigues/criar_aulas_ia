import os
import dotenv

from langgraph.graph import StateGraph
from schemas.simple_llm import SimpleLLM
from schemas.state_classes import MaterialsDto
from langchain_tavily import TavilySearch


def create_search_agent() -> SimpleLLM:
    return SimpleLLM(model_name="gpt-4o", temperature=0.5)

def search_tool(query: str) -> str:
    search = TavilySearch()
    results = search.run(query)
    return results

def search_agent(StateGraph: StateGraph) -> StateGraph:
    llm = create_search_agent()
    prompt_template = """
    You are a search agent. Use the information given by the orquestrator agent to perform a search on each topic that will be covered in the class.
    The title of the class is: {title}.
    The public type is: {public_type}.
    This is a topic that will be covered in a class: {topic}.
    You should return at least one and at most two materials related to the topic with the following structure:
    {{
        "topic": "{topic}" # The topic you are addressing, should match the input topic,
        "type": "Type of the material (articles or videos). Choose based on quality and relevance for the topic.",
        "why": "Why this material is relevant for the topic",
        "link": "Link to the material",
    }}
    Make sure to return the materials in a JSON array format.
    Only return the JSON array, do not add any other text.
    Without ```json, and without ``` at the beginning or end.
    """
    
    for topic in StateGraph["materials"]["topics"]:
        prompt = prompt_template.format(
            title=StateGraph["materials"]["title"],
            public_type=StateGraph["materials"]["public_type"],
            topic=topic,
        )
        response = llm.generate(prompt)

        response = eval(response)
        for el in response:

            if not isinstance(el, dict):
                raise ValueError(f"Each item in the response must be a dict, got {type(el)}")
            
            required_keys = {"link", "type", "why", "topic"}
            if not all(key in el for key in required_keys):
                raise ValueError(f"Response item missing required keys: {required_keys - el.keys()}")
            
            material = MaterialsDto(**el)
            StateGraph["materials"]["result"].append(material)        

    return StateGraph

# Make a test for the agent using the GraphState structure
if __name__ == "__main__":
    dotenv.load_dotenv()
    os.environ["OPENAI_API_KEY"] = dotenv.get_key(dotenv.find_dotenv(), "OPENAI_API_KEY")

    graph_state: StateGraph = {
        "materials": {
            "title": "Introduction to Python Programming",
            "topics": ["Variables and Data Types", "Control Structures", "Functions"],
            "result": [],
        }
    }
    updated_state = search_agent(graph_state)
    print(updated_state)
