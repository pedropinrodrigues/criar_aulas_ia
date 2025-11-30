import os
import json
import dotenv

from langchain.tools import tool
from langchain_tavily import TavilySearch
from langchain_core.messages import HumanMessage, ToolMessage
from schemas.state_classes import MaterialsDto, create_tool_calling_agent
from typing import Dict, Any
from langchain_core.prompts import ChatPromptTemplate

#Tavily Tool
@tool
def tavily_search_tool(query: str) -> str:
    """Perform a search using the Tavily search API."""
    tavily = TavilySearch()
    results = tavily.run(query)
    return json.dumps(results)

def search_agent(graph_state: Dict[str, Any]) -> Dict[str, Any]:
    agent = create_tool_calling_agent([tavily_search_tool])
    materials = graph_state["materials"]
    
    prompt_template = ChatPromptTemplate.from_messages([
        (
            "system",
            """You are an expert search agent specialized in finding educational materials.
            The public type is {public_type}.
            The learning module title is "{title}".
            The current topic is "{topic}".

            Use the Tavily search tool when helpful to discover concrete resources.
            Return ONLY valid JSON in the following format (no comments, no extra keys):
            [
                {{
                    "type": "<article|video|course>",
                    "why": "<concise reason this resource helps>",
                    "link": "<direct URL>"
                }}
            ]
            You may return one or two objects depending on resource quality. Ensure URLs are real and explanations stay short.""",
        )
    ])
    
    for topic in materials["topics"]:
        prompt = prompt_template.format_messages(
            public_type=materials["public_type"],
            title=materials["title"],
            topic=topic
        )
        

        response = agent.invoke(prompt)
        print(response)
        final_msg = response[-1]
        
        json_text = final_msg.content.strip()

        try:
            search_results = json.loads(json_text)
        except Exception as e:
            raise ValueError(
                f"Expected valid JSON from LLM, but got:\n{json_text}"
            ) from e

        for result in search_results:
            material_dto = MaterialsDto(
                link=result.get("link", "").strip(),
                type=result.get("type", "article").strip(),
                why=result.get("why", "").strip(),
                topic=topic
            )
            materials["result"].append(material_dto)
    
    return graph_state
        
if __name__ == "__main__":
    dotenv.load_dotenv()
    os.environ["OPENAI_API_KEY"] = dotenv.get_key(dotenv.find_dotenv(), "OPENAI_API_KEY")

    graph_state = {
        "materials": {
            "title": "Introduction to Python Programming",
            "public_type": "beginners",
            "topics": ["Variables and Data Types", "Control Structures", "Functions"],
            "result": [],
        }
    }

    updated_state = search_agent(graph_state)
    print(updated_state)
