import os
import json
import dotenv

from langchain.tools import tool
from langchain_tavily import TavilySearch
from schemas.state_classes import MaterialsDto, GraphState
from langchain_openai import ChatOpenAI
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate

#Tavily Tool
@tool
def tavily_search_tool(query: str) -> str:
    """Perform a search using the Tavily search API."""
    tavily = TavilySearch()
    results = tavily.run(query)
    return json.dumps(results)

def search_agent(graph_state: GraphState) -> GraphState:
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    tools = [tavily_search_tool]
    
    materials = graph_state["materials"]
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are an expert at finding educational materials for "{title}" aimed at {public_type}.

        Current topic: "{topic}"

        Your task:
        1. Use the tavily_search_tool to find at max 2 high-quality resources for this specific topic
        2. Prioritize recent, reputable sources (official docs, established educational platforms)
        3. After getting search results, return ONLY valid JSON (no markdown, no comments):

        [
            {{
                "type": "article|video|course|book -> choose the most appropriate, but give preference to articles and videos",
                "link": "exact_url",
                "why": "Brief explanation (max 15 words)"
            }}
        ]

        Requirements:
        - URLs must be real and accessible
        - Each resource must be distinct
        - Focus on resources that match the public_type level"""),
        ("placeholder", "{agent_scratchpad}")
    ])
    
    agent = create_tool_calling_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    
    for topic in materials["topics"]:
        result = agent_executor.invoke({
            "public_type": materials["public_type"],
            "title": materials["title"],
            "topic": topic
        })
        
        json_text = result['output'].strip()
        
        try:
            search_results = json.loads(json_text)
        except Exception as e:
            raise ValueError(
                f"Expected valid JSON from LLM, but got:\n{json_text}"
            ) from e

        for res in search_results:
            material_dto = MaterialsDto(
                link=res.get("link", "").strip(),
                type=res.get("type", "article").strip(),
                why=res.get("why", "").strip(),
                topic=topic
            )
            materials["result"].append(material_dto)
            
        graph_state["theory_class"]["student_level"] = materials["public_type"]
    
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
    print(json.dumps(updated_state, indent=2, ensure_ascii=False))